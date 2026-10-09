#!/usr/bin/env python3
"""Validation for Q8 – Change in Women's LFPR (2017 vs 2023)

Recalculates the per‑State LFPR means for 2017 and 2023 directly from the
original Dataset 1 CSV and compares them to the values stored in
`outputs/phase_4_eda/q8_state_lfpr_change.csv`.
All numeric comparisons use a tolerance of 1e-6 before rounding to three
decimal places.
The script prints a PASS/FAIL summary and writes a detailed markdown report
to `outputs/phase_4_eda/q8_state_lfpr_change_full_validation.md`.
"""

import csv
import pathlib
import math
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_CSV = PROJECT_ROOT / "outputs" / "dataset_1_profile" / "feature_engineered_dataset_1.csv"
RESULT_CSV = PROJECT_ROOT / "outputs" / "phase_4_eda" / "q8_state_lfpr_change.csv"
VALIDATION_MD = PROJECT_ROOT / "outputs" / "phase_4_eda" / "q8_state_lfpr_change_full_validation.md"

LFPR_COL = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
GENDER_COL = "Gender"
STATE_COL = "State"
YEAR_COL = "Year"

YEAR_2017 = "PLFS Year (Jul - Jun), 2017"
YEAR_2023 = "PLFS Year (Jul - Jun), 2023"

TOL = 1e-6

def safe_float(v):
    if v is None:
        return None
    s = v.strip()
    if s == "" or s.lower() == "nan":
        return None
    try:
        return float(s)
    except ValueError:
        return None

def fmt(v):
    return "" if v is None else f"{v:.3f}"

# ---------------------------------------------------------------------------
# Load source and aggregate
# ---------------------------------------------------------------------------
with SOURCE_CSV.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data = defaultdict(lambda: {YEAR_2017: [], YEAR_2023: []})
    for row in reader:
        if row.get(GENDER_COL) != "Female":
            continue
        state = row.get(STATE_COL)
        year = row.get(YEAR_COL)
        if year not in (YEAR_2017, YEAR_2023):
            continue
        lfpr = safe_float(row.get(LFPR_COL))
        data[state][year].append(lfpr)

# Compute expected values per state
expected = {}
for state, years in data.items():
    vals_2017 = [v for v in years[YEAR_2017] if v is not None]
    vals_2023 = [v for v in years[YEAR_2023] if v is not None]
    mean_2017 = sum(vals_2017) / len(vals_2017) if vals_2017 else None
    mean_2023 = sum(vals_2023) / len(vals_2023) if vals_2023 else None
    if mean_2017 is not None and mean_2017 != 0:
        abs_change = (mean_2023 - mean_2017) if mean_2023 is not None else None
        pct_change = (abs_change / mean_2017) * 100 if abs_change is not None else None
    else:
        abs_change = None
        pct_change = None
    expected[state] = {
        "LFPR_2017": mean_2017,
        "LFPR_2023": mean_2023,
        "Absolute_Change": abs_change,
        "Percentage_Change": pct_change,
        "Valid_2017_Observation_Count": len(vals_2017),
        "Valid_2023_Observation_Count": len(vals_2023),
        "Missing_2017_Count": len(years[YEAR_2017]) - len(vals_2017),
        "Missing_2023_Count": len(years[YEAR_2023]) - len(vals_2023),
    }

# ---------------------------------------------------------------------------
# Load result CSV
# ---------------------------------------------------------------------------
with RESULT_CSV.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    result_rows = list(reader)

# ---------------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------------
all_pass = True
lines = []
for r in result_rows:
    state = r["State"]
    exp = expected.get(state)
    if not exp:
        all_pass = False
        lines.append(f"- State {state} present in result but not in source data.")
        continue
    # Helper to compare numeric fields
    def compare(field, fmt_expected):
        raw = r[field]
        got = safe_float(raw) if raw != "" else None
        exp_val = exp[field]
        if exp_val is None and got is None:
            return True
        if exp_val is None or got is None:
            return False
        # compare after rounding to 3 decimals (as stored in result)
        exp_round = round(exp_val, 3)
        got_round = round(got, 3)
        return math.isclose(exp_round, got_round, abs_tol=TOL)

    checks = {
        "LFPR_2017": compare("LFPR_2017", fmt),
        "LFPR_2023": compare("LFPR_2023", fmt),
        "Absolute_Change": compare("Absolute_Change", fmt),
        "Percentage_Change": compare("Percentage_Change", fmt),
        "Valid_2017_Observation_Count": int(r["Valid_2017_Observation_Count"]) == exp["Valid_2017_Observation_Count"],
        "Valid_2023_Observation_Count": int(r["Valid_2023_Observation_Count"]) == exp["Valid_2023_Observation_Count"],
        "Missing_2017_Count": int(r["Missing_2017_Count"]) == exp["Missing_2017_Count"],
        "Missing_2023_Count": int(r["Missing_2023_Count"]) == exp["Missing_2023_Count"],
    }
    if not all(checks.values()):
        all_pass = False
        failing = [k for k, v in checks.items() if not v]
        lines.append(f"- State {state}: mismatched fields: {', '.join(failing)}")

# Write markdown report
with VALIDATION_MD.open("w", encoding="utf-8") as f:
    f.write("# Q8 Full Validation Report\n\n")
    f.write(f"**Overall result:** {'PASS' if all_pass else 'FAIL'}\n\n")
    if lines:
        f.write("## Issues found\n\n")
        for l in lines:
            f.write(l + "\n")
    else:
        f.write("No discrepancies detected. All values match within tolerance.\n")

print(f"Validation {'PASS' if all_pass else 'FAIL'} – report written to {VALIDATION_MD}")
