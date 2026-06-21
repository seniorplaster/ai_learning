import os
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────
FOLDER = r"E:\Work\Etisalat\Sergas\Prompts\Ready to Upload\preview_listen\preview_listen"

# ── Gather .wav files ──────────────────────────────────────────
folder = Path(FOLDER)

if not folder.exists():
    raise FileNotFoundError(f"Folder not found: {FOLDER}")

wav_files = sorted(
    f.name for f in folder.iterdir()
    if f.is_file() and f.suffix.lower() == ".wav"
)

total = len(wav_files)
print(f"Found {total} .wav file(s) in:\n  {FOLDER}\n")

# ── Print table ────────────────────────────────────────────────
col_width = max((len(name) for name in wav_files), default=20) + 2
header = f"{'#':<6}{'File Name':<{col_width}}"
separator = "-" * len(header)

print(separator)
print(header)
print(separator)

for i, name in enumerate(wav_files, start=1):
    print(f"{i:<6}{name:<{col_width}}")

print(separator)
print(f"Total: {total} files")