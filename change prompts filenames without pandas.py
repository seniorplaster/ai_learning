import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
FOLDER = Path(r"E:\Work\Etisalat\Sergas\Prompts\Ready to Upload\preview_listen\preview_listen")
EXCEL  = FOLDER / "changepromptsname.xlsx"

# ── Read .xlsx without pandas ──────────────────────────────────────────────────
def read_xlsx(path):
    """Extract rows from the first sheet of an .xlsx file using only stdlib."""
    rows = []
    with zipfile.ZipFile(path) as zf:
        # Load shared strings (text values are stored here in .xlsx format)
        strings = []
        if "xl/sharedStrings.xml" in zf.namelist():
            tree = ET.parse(zf.open("xl/sharedStrings.xml"))
            ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            for si in tree.findall(".//ns:si", ns):
                text = "".join(t.text or "" for t in si.findall(".//ns:t", ns))
                strings.append(text)

        # Parse the first sheet
        tree = ET.parse(zf.open("xl/worksheets/sheet1.xml"))
        ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

        for row in tree.findall(".//ns:row", ns):
            cells = {}
            for cell in row.findall("ns:c", ns):
                ref   = cell.get("r")           # e.g. "A2", "B2"
                col   = "".join(c for c in ref if c.isalpha())
                v_el  = cell.find("ns:v", ns)
                value = ""
                if v_el is not None and v_el.text is not None:
                    if cell.get("t") == "s":    # shared string index
                        value = strings[int(v_el.text)]
                    else:
                        value = v_el.text
                cells[col] = value.strip()
            rows.append(cells)

    return rows

# ── Load mapping (skip header row, require both B and C columns) ───────────────
all_rows = read_xlsx(EXCEL)
mapping  = [
    (r["B"], r["C"])
    for r in all_rows[1:]           # row 0 is the header
    if r.get("B") and r.get("C")
]

# ── Rename files ───────────────────────────────────────────────────────────────
renamed, skipped, errors = [], [], []

for old_name, new_name in mapping:
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

# ── Report ─────────────────────────────────────────────────────────────────────
col = 45

print(f"\n{'='*100}")
print(f"  RENAME REPORT  |  Folder: {FOLDER}")
print(f"{'='*100}")

if renamed:
    print(f"\n✅ RENAMED ({len(renamed)}):")
    print(f"  {'#':<6}{'Old Name':<{col}}  {'New Name'}")
    print(f"  {'-'*6}{'-'*col}  {'-'*col}")
    for i, (old, new) in enumerate(renamed, 1):
        print(f"  {i:<6}{old:<{col}}  {new}")

if skipped:
    print(f"\n⚠️  SKIPPED ({len(skipped)}):")
    print(f"  {'#':<6}{'Old Name':<{col}}  {'New Name':<{col}}  Reason")
    print(f"  {'-'*6}{'-'*col}  {'-'*col}  {'-'*30}")
    for i, (old, new, reason) in enumerate(skipped, 1):
        print(f"  {i:<6}{old:<{col}}  {new:<{col}}  {reason}")

if errors:
    print(f"\n❌ ERRORS ({len(errors)}):")
    print(f"  {'#':<6}{'Old Name':<{col}}  {'New Name':<{col}}  Error")
    print(f"  {'-'*6}{'-'*col}  {'-'*col}  {'-'*30}")
    for i, (old, new, err) in enumerate(errors, 1):
        print(f"  {i:<6}{old:<{col}}  {new:<{col}}  {err}")

print(f"\n{'='*100}")
print(f"  Total: {len(renamed)} renamed | {len(skipped)} skipped | {len(errors)} errors")
print(f"{'='*100}\n")