#!/usr/bin/env python3
import csv, json, sys, argparse, io

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
            print("[]")
            return
        if verbose:
            print(f"[skip] bloc {skipped+1}: {row}", file=sys.stderr)
        skipped += 1

    # --- 2) Next block is considered as the header ---
    try:
        header_row = next(reader)
    except StopIteration:
        print("[]")
        return

    headers = [h.strip() for h in header_row]
    if verbose:
        print(f"[header] {headers}", file=sys.stderr)

    # --- 3) Process next blocks until empty block or end of file ---
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

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--skip", "-s", type=int, default=0,
        help="Number of CSV blocks to be skipped before header (default: 0)"
    )
    ap.add_argument("infile", help="CSV file, or '-' for stdin")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    if args.infile == "-":
        fin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", newline="")
    else:
        fin = open(args.infile, "r", encoding="utf-8", newline="")

    try:
        main(fin, args.skip, args.verbose)
    finally:
        if args.infile != "-":
            fin.close()
