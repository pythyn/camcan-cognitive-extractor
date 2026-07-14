#!/usr/bin/env python3
"""
CamCog.py — CamCAN Cognitive Score Extractor
Extracts and merges cognitive metrics from BIDS-formatted CamCAN summary files.
"""

import argparse
import csv
import os
import re
import sys

__version__ = "1.0.0"

# --- Constants ---
DASHES = re.compile(r"^-{5,}")
IGNORE_PREFIXES = ("Dir:", "Date:", "Output File:", "Output:", "N:")

# --- Helpers ---


def split_line(line: str) -> list:
    """Split a line using tabs or multiple spaces."""
    if "\t" in line:
        return [x.strip() for x in line.split("\t")]
    return re.split(r" {2,}", line.strip())


def is_section(text: str) -> bool:
    """Check if a line is a valid subsection header."""
    if not text or DASHES.match(text) or text.startswith("="):
        return False
    return not any(text.startswith(p) for p in IGNORE_PREFIXES)


def get_section(lines: list, hdr_idx: int):
    """Scan upwards to find the subsection name for a given header."""
    sep_low = None
    for i in range(hdr_idx - 1, -1, -1):
        if DASHES.match(lines[i].strip()):
            sep_low = i
            break

    if sep_low is None:
        return None

    for i in range(sep_low + 1, hdr_idx):
        line = lines[i].strip()
        if is_section(line):
            return line

    sep_high = None
    for i in range(sep_low - 1, -1, -1):
        if DASHES.match(lines[i].strip()):
            sep_high = i
            break

    if sep_high is None:
        return None

    for i in range(sep_high + 1, sep_low):
        line = lines[i].strip()
        if is_section(line):
            return line

    return None


# --- Core Logic ---


def extract_scores(base: str, test: str, cols: list):
    """Parse a single summary file and extract target columns."""
    path = os.path.join(base, test, "release001", "summary", f"{test}_summary.txt")
    data, col_map = {}, {}

    if not os.path.isfile(path):
        print(f"[WARNING] File not found: {path}", file=sys.stderr)
        return data, col_map

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = [L.rstrip("\n") for L in f]

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        row = split_line(line)

        # Detect table headers
        if row and row[0] in ("CCID", "Subject"):
            id_col = row[0]
            found_cols = [c for c in cols if c in row and c not in col_map]

            if found_cols:
                sec = get_section(lines, i)

                # Generate unique column names
                for c in found_cols:
                    col_map[c] = f"{test}_{sec}_{c}" if sec else f"{test}_{c}"

                id_idx = row.index(id_col)
                col_idx = {c: row.index(c) for c in found_cols}

                # Extract data rows
                i += 1
                while i < len(lines):
                    d_line = lines[i].strip()
                    if not d_line:
                        i += 1
                        continue

                    if d_line.startswith("=") or DASHES.match(d_line):
                        break

                    vals = split_line(d_line)
                    if len(vals) > id_idx:
                        subj = vals[id_idx]
                        if subj and subj != id_col:
                            if subj not in data:
                                data[subj] = {}
                            for c in found_cols:
                                idx = col_idx[c]
                                val = vals[idx] if idx < len(vals) else ""
                                data[subj][col_map[c]] = val if val != "" else "NaN"
                    i += 1
                continue
        i += 1

    missing = [c for c in cols if c not in col_map]
    if missing:
        print(f"[WARNING] {test}: Missing columns -> {missing}", file=sys.stderr)

    return data, col_map


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(
        description="Extract CamCAN cognitive metrics into a unified CSV."
    )
    parser.add_argument("--base", required=True, help="Path to base dataset directory.")
    parser.add_argument(
        "--test",
        action="append",
        required=True,
        help="Task directory name (repeatable).",
    )
    parser.add_argument(
        "--cols",
        action="append",
        required=True,
        help="Comma-separated columns (1:1 with --test).",
    )
    parser.add_argument(
        "--sub", help="Optional path to a whitelist of Subject IDs (.txt)."
    )
    parser.add_argument("--output", default="merged.csv", help="Output CSV path.")

    args = parser.parse_args()

    if len(args.test) != len(args.cols):
        parser.error(
            "Mismatch: Each --test must have exactly one corresponding --cols argument."
        )

    base = os.path.abspath(args.base)
    if not os.path.isdir(base):
        parser.error(f"Base directory invalid: {base}")

    whitelist = None
    if args.sub:
        with open(args.sub, "r", encoding="utf-8") as f:
            whitelist = set(f.read().split())

    merged = {}
    out_cols = []

    print(f"Base directory: {base}\nReading files...")

    for test, col_str in zip(args.test, args.cols):
        target_cols = [c.strip() for c in col_str.split(",")]
        data, col_map = extract_scores(base, test, target_cols)

        if not data and not col_map:
            continue

        saved_cols = list(col_map.values())
        print(f"  {test:20s} | {len(data):4d} subjects | {saved_cols}")

        for c in saved_cols:
            if c not in out_cols:
                out_cols.append(c)

        for subj, vals in data.items():
            if subj not in merged:
                merged[subj] = {}
            merged[subj].update(vals)

    # Write output
    headers = ["ID"] + out_cols
    written = 0

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=headers, extrasaction="ignore", restval="NaN"
        )
        writer.writeheader()

        for subj in sorted(merged):
            if whitelist and subj not in whitelist:
                continue

            writer.writerow({"ID": subj, **merged[subj]})
            written += 1

    print(f"\n✓ Saved to: {args.output}")
    print(f"  Total subjects: {written}")


if __name__ == "__main__":
    main()
