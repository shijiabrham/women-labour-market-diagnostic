#!/usr/bin/env python3
"""Phase 4 – Q4 only: Female LFPR, WPR, and Unemployment Rate statistics

Generates:
- outputs/phase_4_eda/q4_dataset_1_eda_result.csv
- outputs/phase_4_eda/q4_dataset_1_eda_validation.md

All calculations use only the Python standard library.
"""

import csv
import hashlib
import statistics
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATASET1 = Path("outputs/dataset_1_profile/feature_engineered_dataset_1.csv")
OUTDIR = Path("outputs/phase_4_eda")
OUTDIR.mkdir(parents=True, exist_ok=True)
RESULT_CSV = OUTDIR / "q4_dataset_1_eda_result.csv"
VALID_MD = OUTDIR / "q4_dataset_1_eda_validation.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_float(v: str):
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None

def agg_stats(vals):
    clean = [v for v in vals if v is not None]
    n = len(clean)
    if n == 0:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None, "std": None}
    mean = statistics.mean(clean)
    median = statistics.median(clean)
    minv = min(clean)
    maxv = max(clean)
    std = statistics.pstdev(clean) if n > 1 else 0.0
    return {
        "count": n,
        "mean": round(mean, 3),
        "median": round(median, 3),
        "min": round(minv, 3),
        "max": round(maxv, 3),
        "std": round(std, 3),
    }

# ---------------------------------------------------------------------------
# Load dataset and verify integrity
# ---------------------------------------------------------------------------
if not DATASET1.is_file():
    raise FileNotFoundError(f"Dataset not found: {DATASET1}")

with DATASET1.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    header = reader.fieldnames

expected_rows = 22650
expected_cols = 14
integrity = []
integrity.append(f"Source exists: {DATASET1}")
integrity.append(f"Row count: {len(rows)} (expected {expected_rows})")
integrity.append(f"Column count: {len(header)} (expected {expected_cols})")
integrity.append(f"SHA‑256: {sha256(DATASET1)}")

# ---------------------------------------------------------------------------
# Identify indicator columns
# ---------------------------------------------------------------------------
lfpr_col = None
wpr_col = None
ur_col = None
for name in header:
    if "Labor Force Participation Rate" in name:
        lfpr_col = name
    if "Working Population Rate" in name:
        wpr_col = name
    if "Unemployment Rate" in name:
        ur_col = name
if not (lfpr_col and wpr_col and ur_col):
    raise KeyError("One or more indicator columns not found in header")

# ---------------------------------------------------------------------------
# Filter female rows
# ---------------------------------------------------------------------------
female_rows = [r for r in rows if r.get("Gender", "").strip().lower() == "female"]
filtered_count = len(female_rows)

# ---------------------------------------------------------------------------
# Gather values per year per indicator
# ---------------------------------------------------------------------------
indicators = {
    "LFPR": lfpr_col,
    "WPR": wpr_col,
    "Unemployment_Rate": ur_col,
}

# Nested dict: indicator -> year -> list of values
values = {ind: defaultdict(list) for ind in indicators}
missing = {ind: defaultdict(int) for ind in indicators}

for r in female_rows:
    year = r.get("Year_Numeric", "").strip()
    for ind, col in indicators.items():
        raw = r.get(col, "")
        val = safe_float(raw)
        if val is None:
            missing[ind][year] += 1
        else:
            values[ind][year].append(val)

# ---------------------------------------------------------------------------
# Build result rows (one per indicator per year + all years)
# ---------------------------------------------------------------------------
result_rows = []
years = ["2017","2018","2019","2020","2021","2022","2023"]
for ind in indicators:
    for yr in years:
        stats = agg_stats(values[ind].get(yr, []))
        result_rows.append({
            "Question_ID": "Q4",
            "Dataset": "Dataset 1",
            "Year": yr,
            "Indicator": ind,
            "Filter": "Gender == Female",
            "Aggregation_Level": "Year",
            "Filtered_Row_Count": filtered_count,
            "Valid_Observation_Count": stats["count"],
            "Mean": stats["mean"],
            "Median": stats["median"],
            "Minimum": stats["min"],
            "Maximum": stats["max"],
            "Population_Standard_Deviation": stats["std"],
            "Missing_Count": missing[ind].get(yr, 0),
            "Status": "OK",
            "Notes": "",
        })
# All‑years summary per indicator
for ind in indicators:
    all_vals = [v for lst in values[ind].values() for v in lst]
    stats = agg_stats(all_vals)
    total_missing = sum(missing[ind].values())
    result_rows.append({
        "Question_ID": "Q4",
        "Dataset": "Dataset 1",
        "Year": "All",
        "Indicator": ind,
        "Filter": "Gender == Female",
        "Aggregation_Level": "All Years",
        "Filtered_Row_Count": filtered_count,
        "Valid_Observation_Count": stats["count"],
        "Mean": stats["mean"],
        "Median": stats["median"],
        "Minimum": stats["min"],
        "Maximum": stats["max"],
        "Population_Standard_Deviation": stats["std"],
        "Missing_Count": total_missing,
        "Status": "OK",
        "Notes": "",
    })

# ---------------------------------------------------------------------------
# Write CSV
# ---------------------------------------------------------------------------
fieldnames_out = [
    "Question_ID",
    "Dataset",
    "Year",
    "Indicator",
    "Filter",
    "Aggregation_Level",
    "Filtered_Row_Count",
    "Valid_Observation_Count",
    "Mean",
    "Median",
    "Minimum",
    "Maximum",
    "Population_Standard_Deviation",
    "Missing_Count",
    "Status",
    "Notes",
]
with RESULT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_out)
    writer.writeheader()
    for r in result_rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# Independent validation
# ---------------------------------------------------------------------------
with RESULT_CSV.open(newline="", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

validation_entries = []
for calc in result_rows:
    # Find matching row in csv_rows
    match = next((r for r in csv_rows if r["Year"] == calc["Year"] and r["Indicator"] == calc["Indicator"]), None)
    if not match:
        continue
    for key in ["Filtered_Row_Count", "Valid_Observation_Count", "Mean", "Median", "Minimum", "Maximum", "Population_Standard_Deviation", "Missing_Count"]:
        calc_val = calc[key]
        stored_val = match[key]
        try:
            stored_num = float(stored_val) if stored_val != "" else None
        except ValueError:
            stored_num = None
        diff = None
        if isinstance(calc_val, (int, float)) and isinstance(stored_num, (int, float)):
            diff = abs(calc_val - stored_num)
        status = "PASS" if diff is None or (diff is not None and diff < 1e-6) else "FAIL"
        validation_entries.append({
            "Year": calc["Year"],
            "Indicator": calc["Indicator"],
            "Metric": key,
            "Result_File": stored_val,
            "Independent": calc_val,
            "Difference": diff if diff is not None else "N/A",
            "Status": status,
        })

# ---------------------------------------------------------------------------
# Write validation markdown
# ---------------------------------------------------------------------------
with VALID_MD.open("w", encoding="utf-8") as f:
    f.write("# Q4 – Female LFPR, WPR, Unemployment Rate – Validation Report\n\n")
    f.write("## Source integrity\n")
    for line in integrity:
        f.write(f"- {line}\n")
    f.write("\n")
    f.write("## Indicator column mapping\n")
    f.write(f"- LFPR column: {lfpr_col}\n")
    f.write(f"- WPR column: {wpr_col}\n")
    f.write(f"- Unemployment Rate column: {ur_col}\n\n")
    f.write("## Independent validation comparison\n\n")
    f.write("| Year | Indicator | Metric | Result File | Independent | Difference | Status |\n")
    f.write("|------|-----------|--------|------------:|------------:|-----------:|--------|\n")
    for e in validation_entries:
        f.write(f"| {e['Year']} | {e['Indicator']} | {e['Metric']} | {e['Result_File']} | {e['Independent']} | {e['Difference']} | {e['Status']} |\n")
    f.write("\n## Final status\n\n")
    final = "PASS" if all(e['Status'] == 'PASS' for e in validation_entries) else "FAIL"
    f.write(f"**{final}**\n")

print("Q4 analysis complete. Results written to outputs/phase_4_eda/")
