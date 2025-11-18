#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from jsonschema import validate, ValidationError
except ImportError:
    validate = None


# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
def log(level, msg):
    print(f"[{level.upper():7}] {msg}")


# ------------------------------------------------------------
# Repo root detection: walk upward until a .git file or folder
# ------------------------------------------------------------
def find_repo_root(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None  # filesystem root reached
        current = parent


# ------------------------------------------------------------
# Robust fetch: in-memory cache + retries for remote URLs
# ------------------------------------------------------------
_FETCH_CACHE = {}

def fetch_with_retry(url, retries=4, backoff=1.7, timeout=10):
    """Fetch remote JSON with retry logic and caching."""
    # Return cached value
    if url in _FETCH_CACHE:
        return _FETCH_CACHE[url]

    last_exc = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "projectmeta-fetcher"})
            with urlopen(req, timeout=timeout) as resp:
                data = resp.read().decode()
            # Validate JSON
            json.loads(data)
            _FETCH_CACHE[url] = data
            return data
        except Exception as e:
            last_exc = e
            wait = backoff ** attempt
            log("warn", f"Fetch failed for {url}: {e}; retrying in {wait:.1f}s...")
            time.sleep(wait)

    log("error", f"Permanent failure fetching {url}: {last_exc}")
    return None

# ------------------------------------------------------------
# Fetch JSON from remote or local file
# ------------------------------------------------------------
def fetch(source: str, repo_root: str, strict=False):
    """
    Retrieve JSON from:
      - HTTP(S) URL   → via GET
      - local:...     → repo-local JSON file
    """
    # ---- LOCAL MODE -----------------------------------------------------
    if source.startswith("local:"):
        rel_path = source[len("local:"):]
        local_path = os.path.normpath(os.path.join(repo_root, rel_path))

        # Security check: stay inside repo
        if not local_path.startswith(repo_root):
            log("error", f"Forbidden local path outside repo: {rel_path}")
            if strict:
                sys.exit(1)
            return None

        if not os.path.isfile(local_path):
            log("warn", f"Local source not found: {local_path}")
            if strict:
                sys.exit(1)
            return None

        try:
            with open(local_path, "r") as f:
                data = f.read()
            json.loads(data)  # validation
            return data
        except Exception as e:
            log("warn", f"Failed to read local file {local_path}: {e}")
            if strict:
                sys.exit(1)
            return None

    # ---- REMOTE MODE -----------------------------------------------------
    try:
        log("info", f"Fetching {source}")
        return fetch_with_retry(source)
    except (HTTPError, URLError) as e:
        log("warn", f"Failed to fetch {source}: {e}")
    except json.JSONDecodeError:
        log("warn", f"Invalid JSON at {source}")
    except Exception as e:
        log("warn", f"Unexpected error while fetching {source}: {e}")

    if strict:
        sys.exit(1)
    return None


# ------------------------------------------------------------
# jq utilities
# ------------------------------------------------------------
def run_jq(expr, json_data):
    """Run jq expression on given JSON data."""
    try:
        proc = subprocess.run(
            ["jq", "-er", expr],
            input=json_data.encode(),
            capture_output=True,
            check=False
        )
        if proc.returncode == 0:
            val = proc.stdout.decode().strip()
            if val.lower() not in ("null", ""):
                return val
        else:
            msg = proc.stderr.decode().strip() or proc.stdout.decode().strip()
            log("warn", f"jq {expr} failed: {msg}")
    except FileNotFoundError:
        log("error", "jq not found. Please install jq or use pyjq.")
        sys.exit(1)
    except Exception as e:
        log("warn", f"jq exception: {e}")
    return None


def extract_fields(json_data, fields, fail_on_missing=False):
    """Extract fields using jq expressions."""
    result = {}
    for target, jq_expr in fields.items():
        if jq_expr in (None, "null", ""):
            continue
        val = run_jq(jq_expr, json_data)
        if val is not None:
            result[target] = val
        elif fail_on_missing:
            log("error", f"Missing required field: {target}")
            sys.exit(1)
    return result


# ------------------------------------------------------------
# Project lookup and update logic
# ------------------------------------------------------------
def find_project(existing_projects, name):
    for proj in existing_projects:
        if proj.get("name") == name:
            return proj
    return None


def update_project(existing, updates):
    for k, v in updates.items():
        if k == "name":
            continue
        if k in existing:
            if existing[k] != v:
                log("info", f"Updating {k} for {existing['name']}: '{existing[k]}' → '{v}'")
                existing[k] = v
        else:
            log("info", f"Adding {k} to {existing['name']}: '{v}'")
            existing[k] = v


def load_mapping_fields(mapping_ref, strict=False):
    """Load external mapping definition."""
    log("info", f"Loading mappingRef from {mapping_ref}")
    if not (mapping_ref.startswith("http://") or mapping_ref.startswith("https://")):
        log("error", f"mappingRef must be an HTTP(S) URL, got: {mapping_ref}")
        if strict:
            sys.exit(1)
        return None

    data = fetch(mapping_ref, repo_root="", strict=strict)
    if not data:
        return None

    try:
        mapping = json.loads(data)
        return {k: v for k, v in mapping.items() if isinstance(v, str)}
    except json.JSONDecodeError as e:
        log("warn", f"Invalid JSON in mappingRef {mapping_ref}: {e}")
        if strict:
            sys.exit(1)
    return None


# ------------------------------------------------------------
# Process one mapping item (may produce multiple projects)
# ------------------------------------------------------------
def process_project_mapping(proj_cfg, existing_projects, args, repo_root):
    source = proj_cfg.get("source")
    fields = proj_cfg.get("fields", {})
    mapping_ref = proj_cfg.get("mappingRef")
    allow = proj_cfg.get("allow", "update")  # default = update

    if not source:
        log("warn", f"Skipping mapping entry without source: {proj_cfg}")
        return

    # fields / mappingRef handling
    if mapping_ref and fields:
        log("warn", f"Mapping defines both 'mappingRef' and 'fields'; using 'fields'.")
    elif mapping_ref:
        fields = load_mapping_fields(mapping_ref, strict=args.strict)
        if not fields:
            log("warn", f"Could not load mappingRef for {source}; skipping.")
            return
    elif not fields:
        log("warn", f"Mapping for source {source} has neither 'fields' nor 'mappingRef'; skipping.")
        return

    json_data = fetch(source, repo_root, strict=args.strict)
    if not json_data:
        return

    try:
        parsed = json.loads(json_data)
    except json.JSONDecodeError as e:
        log("error", f"Invalid JSON from source {source}: {e}")
        if args.strict:
            sys.exit(1)
        return

    # Always treat as list
    items = parsed if isinstance(parsed, list) else [parsed]

    for idx, item in enumerate(items):
        extracted = extract_fields(json.dumps(item), fields, fail_on_missing=args.fail_on_missing)
        if not extracted:
            continue

        # Optional name
        name = proj_cfg.get("name") or extracted.get("name")
        if not name:
            log("error", f"No 'name' for item #{idx} in source {source}")
            if args.strict:
                sys.exit(1)
            continue

        existing_entry = find_project(existing_projects, name)
        exists = existing_entry is not None

        # Allow policy
        if exists and allow not in ("both", "update"):
            log("error", f"Project '{name}' exists but allow={allow} forbids update.")
            if args.strict:
                sys.exit(1)
            continue
        if not exists and allow not in ("both", "create"):
            log("error", f"Project '{name}' does not exist but allow={allow} forbids creation.")
            if args.strict:
                sys.exit(1)
            continue

        # Update or create
        if exists:
            log("info", f"Updating project {name}")
            update_project(existing_entry, extracted)
        else:
            log("info", f"Adding new project {name}")
            if "name" in extracted:
                extracted.pop("name")
            new_entry = {"name": name, **extracted}
            existing_projects.append(new_entry)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Update an existing projects.json from external sources using a mapping file."
    )
    parser.add_argument("mapping", help="Path to mapping JSON file")
    parser.add_argument("projects", help="Path to existing projects.json file")
    parser.add_argument("--schema", help="Optional validation schema")
    parser.add_argument("--strict", action="store_true", help="Exit on fetch/JSON errors")
    parser.add_argument("--fail-on-missing", action="store_true", help="Fail if jq field is missing")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the projects.json file")
    parser.add_argument("-o", "--output", help="Output file instead of overwriting")
    args = parser.parse_args()

    # Load mapping
    try:
        with open(args.mapping) as f:
            mapping = json.load(f)
    except json.JSONDecodeError as e:
        log("error", f"Invalid mapping JSON: {e}")
        sys.exit(1)

    # Detect repo root
    repo_root = find_repo_root(os.path.dirname(os.path.abspath(args.mapping)))
    if not repo_root:
        repo_root = os.path.dirname(os.path.abspath(args.mapping))
    log("info", f"Repo root: {repo_root}")

    # Load existing projects
    try:
        with open(args.projects) as f:
            projects_data = json.load(f)
    except json.JSONDecodeError as e:
        log("error", f"Invalid projects JSON: {e}")
        sys.exit(1)

    existing_projects = projects_data.get("projects", [])
    projects_cfg = mapping.get("projects", [])

    # Apply updates
    for proj_cfg in projects_cfg:
        process_project_mapping(proj_cfg, existing_projects, args, repo_root)

    # Schema validation
    if args.schema:
        if not validate:
            log("warn", "jsonschema not installed")
        else:
            with open(args.schema) as f:
                schema = json.load(f)
            try:
                validate(instance=projects_data, schema=schema)
                log("info", "Schema validation OK.")
            except ValidationError as e:
                log("error", f"Schema validation failed: {e.message}")
                if args.strict:
                    sys.exit(1)

    # Output
    if args.output:
        output_path = args.output
    elif args.inplace:
        output_path = args.projects
    else:
        log("error", "No output generated. You must provide either --inplace or --output.")
        sys.exit(1)
        
    with open(output_path, "w") as f:
        json.dump(projects_data, f, indent=2)
        f.write("\n")

    log("info", f"Updated {output_path} with {len(existing_projects)} projects.")


if __name__ == "__main__":
    main()
