#!/usr/bin/env python3
import csv, json, sys, argparse, io
from urllib.parse import urlparse
from urllib.request import urlopen

def clean_cell(v):
    if v is None:
        return None
    s = v.replace("\r", "").strip()
    return s if s != "" else None

def convert_value(v):
    if v is None:
        return None
    try:
        if v.isdigit() or (v.startswith("-") and v[1:].isdigit()):
            return int(v)
        f = float(v)
        if f.is_integer():
            return int(f)
        return f
    except:
        return v

def row_is_empty(row):
    return all(clean_cell(v) is None for v in row)

def main(fin, skip_blocks, verbose):
    reader = csv.reader(fin)
    out = []

    # --- 1) Skip unwanted blocks ---
    skipped = 0
    while skipped < skip_blocks:
        try:
            row = next(reader)
        except StopIteration:
            return []  # empty output
        if verbose:
            print(f"[skip] bloc {skipped+1}: {row}", file=sys.stderr)
        skipped += 1

    # --- 2) Next block is considered as the header ---
    try:
        header_row = next(reader)
    except StopIteration:
        return []

    headers = [h.strip() for h in header_row]
    if verbose:
        print(f"[header] {headers}", file=sys.stderr)

    # --- 3) Process next blocks until empty block or EOF ---
    for row in reader:
        if row_is_empty(row):
            if verbose:
                print("[stop] empty block encountered", file=sys.stderr)
            break

        # Adjust row to match exactly the header columns
        if len(row) < len(headers):
            row = row + [""] * (len(headers) - len(row))
        if len(row) > len(headers):
            row = row[:len(headers)]

        obj = {}
        for key, val in zip(headers, row):
            cleaned = clean_cell(val)
            if cleaned is None:
                continue
            obj[key] = convert_value(cleaned)

        out.append(obj)

    return out


def open_input(source):
    """Return a text file-like object for:
       - "-" (stdin)
       - local file path
       - http(s) URL
    """
    parsed = urlparse(source)
    if parsed.scheme in ("http", "https"):
        resp = urlopen(source)
        return io.TextIOWrapper(resp, encoding="utf-8", newline="")

    if source == "-":
        return io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", newline="")

    return open(source, "r", encoding="utf-8", newline="")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip", "-s", type=int, default=0,
                    help="Number of CSV blocks to skip before header")
    ap.add_argument("infile", help="CSV file, URL, or '-' for stdin")
    ap.add_argument("--output", "-o", required=True,
                    help="Output JSON file path")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    fin = open_input(args.infile)
    try:
        json_data = main(fin, args.skip, args.verbose)
    finally:
        if hasattr(fin, "close") and args.infile not in ("-",):
            fin.close()

    # --- Write JSON output to file ---
    with open(args.output, "w", encoding="utf-8") as fout:
        fout.write(json.dumps(json_data, ensure_ascii=False, indent=2))
