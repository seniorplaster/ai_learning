import os
import pandas as pd
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
FOLDER = Path(r"E:\Work\Etisalat\Sergas\Prompts\Ready to Upload\preview_listen\preview_listen")
EXCEL  = FOLDER / "changepromptsname.xlsx"

# ── Load the rename mapping ────────────────────────────────────────────────────
df = pd.read_excel(
    EXCEL,
    usecols=["Existing Filename", "New Filename"],
    dtype=str
).dropna(subset=["Existing Filename", "New Filename"])

df["Existing Filename"] = df["Existing Filename"].str.strip()
df["New Filename"]      = df["New Filename"].str.strip()

# ── Rename with full reporting ─────────────────────────────────────────────────
renamed, skipped, errors = [], [], []

for _, row in df.iterrows():
    old_name = row["Existing Filename"]
    new_name = row["New Filename"]
    old_path = FOLDER / old_name
    new_path = FOLDER / new_name

    if not old_path.exists():
        skipped.append((old_name, new_name, "source file not found"))
        continue

    if new_path.exists() and old_path != new_path:
        skipped.append((old_name, new_name, "target filename already exists"))
        continue

    try:
        old_path.rename(new_path)
        renamed.append((old_name, new_name))
    except Exception as e:
        errors.append((old_name, new_name, str(e)))

# ── Summary report ─────────────────────────────────────────────────────────────
col = 45  # column width for filenames

print(f"\n{'='*100}")
print(f"  RENAME REPORT  |  Folder: {FOLDER}")
print(f"{'='*100}")

if renamed:
    print(f"\n✅ RENAMED ({len(renamed)}):")
    print(f"  {'Old Name':<{col}}  {'New Name':<{col}}")
    print(f"  {'-'*col}  {'-'*col}")
    for old, new in renamed:
        print(f"  {old:<{col}}  {new:<{col}}")

if skipped:
    print(f"\n⚠️  SKIPPED ({len(skipped)}):")
    print(f"  {'Old Name':<{col}}  {'New Name':<{col}}  Reason")
    print(f"  {'-'*col}  {'-'*col}  {'-'*30}")
    for old, new, reason in skipped:
        print(f"  {old:<{col}}  {new:<{col}}  {reason}")

if errors:
    print(f"\n❌ ERRORS ({len(errors)}):")
    print(f"  {'Old Name':<{col}}  {'New Name':<{col}}  Error")
    print(f"  {'-'*col}  {'-'*col}  {'-'*30}")
    for old, new, err in errors:
        print(f"  {old:<{col}}  {new:<{col}}  {err}")

print(f"\n{'='*100}")
print(f"  Total: {len(renamed)} renamed | {len(skipped)} skipped | {len(errors)} errors")
print(f"{'='*100}\n")