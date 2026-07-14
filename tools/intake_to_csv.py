#!/usr/bin/env python3
"""
Turn saved welder-repair intake emails into a spreadsheet.

Every survey the website sends carries a hidden machine-readable block:

    ----- WWR-DATA v1 (for record keeping - please leave this alone) -----
    {"job_id": "WWR-2607-K3Q", "name": "...", "make_model": "...", ...}
    ----- END WWR-DATA -----

This script finds those blocks in whatever you feed it and writes one row per
job. It reads plain text, .eml files, Gmail .mbox exports, or a whole folder of
them -- it just scans for the block, so the container does not matter.

USAGE
    python3 tools/intake_to_csv.py ~/Downloads/mail-export.mbox -o jobs.csv
    python3 tools/intake_to_csv.py ~/Documents/welder-emails/ -o jobs.csv

WHERE THE OUTPUT GOES
    Write the CSV somewhere OUTSIDE this repository. It has customer names,
    emails, and phone numbers in it -- that is business records, not website
    content, and it must never be pushed to a public repo.

OUTCOMES: how the statistics actually happen
    The CSV has empty columns at the end -- outcome, parts_cost, hours_spent,
    charged, notes. Fill them in yourself as jobs finish, in a spreadsheet.
    That is the other half of the data. Intake tells you what came in the door;
    those columns tell you what it was worth. Only together do they answer
    "which machines are worth my time."

    Re-running this script will NOT overwrite a CSV that already has outcomes
    filled in -- it merges by job number and leaves your entries alone.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

BLOCK = re.compile(
    r"-----\s*WWR-DATA v1.*?-----\s*(\{.*?\})\s*-----\s*END WWR-DATA\s*-----",
    re.DOTALL,
)

# Intake columns, in the order they make sense to read.
INTAKE_FIELDS = [
    "job_id", "submitted", "name", "email", "phone", "location",
    "welder_type", "make_model", "serial", "age",
    "volts_120", "volts_240", "volts_leads", "idle", "jumpstarted",
    "symptoms", "story", "urgency", "transport",
]

# You fill these in by hand as each job closes. The script never touches them.
OUTCOME_FIELDS = ["outcome", "root_cause", "parts_cost", "hours_spent", "charged", "notes"]


def find_records(paths):
    """Scan every file given (recursing into folders) for WWR-DATA blocks."""
    records, seen, bad = {}, set(), 0

    files = []
    for p in paths:
        path = Path(p).expanduser()
        if path.is_dir():
            files.extend(f for f in path.rglob("*") if f.is_file())
        elif path.is_file():
            files.append(path)
        else:
            print(f"  ! not found, skipping: {path}", file=sys.stderr)

    for f in files:
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for match in BLOCK.finditer(text):
            try:
                rec = json.loads(match.group(1))
            except json.JSONDecodeError:
                bad += 1
                continue
            job_id = rec.get("job_id")
            if not job_id or job_id in seen:
                continue  # same email saved twice, or a reply quoting the original
            seen.add(job_id)
            if isinstance(rec.get("symptoms"), list):
                rec["symptoms"] = "; ".join(rec["symptoms"])
            records[job_id] = rec

    return records, bad


def load_existing(csv_path):
    """Read back a CSV you have already annotated, so we never clobber it."""
    if not csv_path.exists():
        return {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        return {r["job_id"]: r for r in csv.DictReader(fh) if r.get("job_id")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="Email files, mbox exports, or folders to scan")
    ap.add_argument("-o", "--out", required=True, help="CSV to write (keep it outside this repo)")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    found, bad = find_records(args.sources)
    existing = load_existing(out)

    new_ids = [j for j in found if j not in existing]

    # Merge: keep hand-entered outcome columns, refresh nothing that you own.
    rows = {}
    for job_id, rec in found.items():
        row = {f: "" for f in INTAKE_FIELDS + OUTCOME_FIELDS}
        row.update({k: v for k, v in rec.items() if k in INTAKE_FIELDS})
        if job_id in existing:
            for f in OUTCOME_FIELDS:
                row[f] = existing[job_id].get(f, "")
        rows[job_id] = row

    # Anything already in the CSV but not in this scan stays put.
    for job_id, row in existing.items():
        rows.setdefault(job_id, row)

    ordered = sorted(rows.values(), key=lambda r: (r.get("submitted", ""), r.get("job_id", "")))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=INTAKE_FIELDS + OUTCOME_FIELDS)
        w.writeheader()
        w.writerows(ordered)

    kept = len(existing)
    print(f"Wrote {out}")
    print(f"  {len(ordered)} jobs total  ({len(new_ids)} new, {kept} already on file)")
    if kept:
        print("  Outcome columns you had already filled in were preserved.")
    if bad:
        print(f"  ! {bad} data block(s) were unreadable and got skipped.", file=sys.stderr)
    if not ordered:
        print("  Nothing found. Check that you exported the emails themselves,")
        print("  not just a list of them.")


if __name__ == "__main__":
    main()
