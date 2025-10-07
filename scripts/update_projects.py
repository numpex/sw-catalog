#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from jsonschema import validate, ValidationError
except ImportError:
    validate = None


def log(level, msg):
    print(f"[{level.upper():7}] {msg}")


def fetch(url: str, strict=False):
    """Download a JSON file from the given URL."""
    log("info", f"Fetching {url}")
    try:
        req = Request(url, headers={"User-Agent": "projectmeta-fetcher"})
        with urlopen(req, timeout=10) as resp:
            data = resp.read().decode()
        json.loads(data)  # validate JSON
        return data
    except (HTTPError, URLError) as e:
        log("warn", f"Failed to fetch {url}: {e}")
    except json.JSONDecodeError:
        log("warn", f"Invalid JSON at {url}")
    except Exception as e:
        log("warn", f"Unexpected error while fetching {url}: {e}")

    if strict:
        sys.exit(1)
    return None


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


def find_project(existing_projects, name):
    """Return reference to project dict if exists, else None."""
    for proj in existing_projects:
        if proj.get("name") == name:
            return proj
    return None


def update_project(existing, updates):
    """Merge new fields into existing project entry."""
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


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing projects.json file using external JSON file (e.g. Codemeta) defined in a mapping file."
    )
    parser.add_argument("mapping", help="Path to mapping JSON file")
    parser.add_argument("projects", help="Path to existing projects.json file to update")
    parser.add_argument("--schema", help="Optional schema file for validation")
    parser.add_argument("--strict", action="store_true", help="Fail on fetch or JSON errors")
    parser.add_argument("--fail-on-missing", action="store_true", help="Fail if a jq field is missing")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the existing projects.json in place")
    parser.add_argument("-o", "--output", help="Write to this file instead of overwriting projects.json")
    args = parser.parse_args()

    # Load files
    try:
        with open(args.mapping) as f:
            mapping = json.load(f)
    except json.JSONDecodeError as e:
        log("error", f"Invalid JSON in mapping file {args.mapping}: {e}")
        sys.exit(1)
    
    try:
        with open(args.projects) as f:
            projects_data = json.load(f)
    except json.JSONDecodeError as e:
        log("error", f"Invalid JSON in projects file {args.projects}: {e}")
        sys.exit(1)

    existing_projects = projects_data.get("projects", [])
    projects_cfg = mapping.get("projects", [])

    # Apply updates
    for proj_cfg in projects_cfg:
        name = proj_cfg.get("name")
        source = proj_cfg.get("source")
        fields = proj_cfg.get("fields", {})

        if not name or not source:
            log("warn", f"Skipping invalid mapping entry: {proj_cfg}")
            continue

        json_data = fetch(source, strict=args.strict)
        if not json_data:
            continue

        log("info", f"Start updating fields for project {name} from source {source}")
        extracted = extract_fields(json_data, fields, fail_on_missing=args.fail_on_missing)
        if not extracted:
            continue

        existing_entry = find_project(existing_projects, name)
        if existing_entry:
            update_project(existing_entry, extracted)
        else:
            log("info", f"Adding new project {name}")
            new_entry = {"name": name, **extracted}
            existing_projects.append(new_entry)

    # Validate (optional)
    if args.schema:
        if not validate:
            log("warn", "jsonschema not installed, skipping validation.")
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

    # Write result
    output_path = args.projects if args.inplace or not args.output else args.output
    with open(output_path, "w") as f:
        json.dump(projects_data, f, indent=2)
        f.write("\n")

    log("info", f"Updated {output_path} with {len(projects_data.get('projects', []))} projects.")


if __name__ == "__main__":
    main()
