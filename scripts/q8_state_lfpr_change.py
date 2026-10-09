#!/usr/bin/env python3
"""Q8 – Change in Women's LFPR (2017 vs 2023)

This script computes, for each State/UT, the mean LFPR for 2017 and 2023 (female only),
the absolute and percentage change, and counts of valid / missing observations.
All numeric results are rounded to three decimal places. No external libraries are required.
The result CSV is written to `outputs/phase_4_eda/q8_state_lfpr_change.csv`.
A short sample (first five states) is printed to stdout.
"""

import csv
import pathlib
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_CSV = PROJECT_ROOT / "outputs" / "dataset_1_profile" / "feature_engineered_dataset_1.csv"
RESULT_CSV = PROJECT_ROOT / "outputs" / "phase_4_eda" / "q8_state_lfpr_change.csv"

LFPR_COL = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
GENDER_COL = "Gender"
STATE_COL = "State"
YEAR_COL = "Year"

YEAR_2017 = "PLFS Year (Jul - Jun), 2017"
YEAR_2023 = "PLFS Year (Jul - Jun), 2023"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def safe_float(value):
    """Convert a string to float, returning None for missing or non‑numeric values."""
    if value is None:
        return None
    v = value.strip()
    if v == "" or v.lower() == "nan":
        return None
    try:
        return float(v)
    except ValueError:
        return None

def fmt(value):
    """Format a number to three decimals, or empty string for None."""
    return "" if value is None else f"{value:.3f}"

# ---------------------------------------------------------------------------
# Load data and aggregate
# ---------------------------------------------------------------------------
print("Loading source CSV…")
with SOURCE_CSV.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    # Verify required columns are present
    required = {LFPR_COL, GENDER_COL, STATE_COL, YEAR_COL}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise RuntimeError(f"Missing columns in source CSV: {missing}")

    # Data structures: nested dict state -> year -> list of floats
    data = defaultdict(lambda: {YEAR_2017: [], YEAR_2023: []})
    for row in reader:
        if row.get(GENDER_COL) != "Female":
            continue
        state = row.get(STATE_COL)
        year = row.get(YEAR_COL)
        if year not in (YEAR_2017, YEAR_2023):
            continue
        lfpr_val = safe_float(row.get(LFPR_COL))
        data[state][year].append(lfpr_val)  # may be None for missing

# ---------------------------------------------------------------------------
# Compute per‑state statistics
# ---------------------------------------------------------------------------
rows = []
for state in sorted(data.keys()):
    vals_2017 = data[state][YEAR_2017]
    vals_2023 = data[state][YEAR_2023]

    # Separate valid and missing counts
    valid_2017 = [v for v in vals_2017 if v is not None]
    missing_2017 = len(vals_2017) - len(valid_2017)
    valid_2023 = [v for v in vals_2023 if v is not None]
    missing_2023 = len(vals_2023) - len(valid_2023)

    mean_2017 = sum(valid_2017) / len(valid_2017) if valid_2017 else None
    mean_2023 = sum(valid_2023) / len(valid_2023) if valid_2023 else None

    if mean_2017 is not None and mean_2017 != 0:
        abs_change = (mean_2023 - mean_2017) if mean_2023 is not None else None
        pct_change = (abs_change / mean_2017) * 100 if abs_change is not None else None
    else:
        abs_change = None
        pct_change = None

    row = {
        "State": state,
        "LFPR_2017": fmt(mean_2017),
        "LFPR_2023": fmt(mean_2023),
        "Absolute_Change": fmt(abs_change),
        "Percentage_Change": fmt(pct_change),
        "Valid_2017_Observation_Count": len(valid_2017),
        "Valid_2023_Observation_Count": len(valid_2023),
        "Missing_2017_Count": missing_2017,
        "Missing_2023_Count": missing_2023,
    }
    rows.append(row)

# ---------------------------------------------------------------------------
# Write result CSV
# ---------------------------------------------------------------------------
FIELDNAMES = [
    "State",
    "LFPR_2017",
    "LFPR_2023",
    "Absolute_Change",
    "Percentage_Change",
    "Valid_2017_Observation_Count",
    "Valid_2023_Observation_Count",
    "Missing_2017_Count",
    "Missing_2023_Count",
]

RESULT_CSV.parent.mkdir(parents=True, exist_ok=True)
with RESULT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Result CSV written to {RESULT_CSV}")

# ---------------------------------------------------------------------------
# Show a sample (first five states)
# ---------------------------------------------------------------------------
print("\nSample output (first five states):")
for r in rows[:5]:
    print(r)
