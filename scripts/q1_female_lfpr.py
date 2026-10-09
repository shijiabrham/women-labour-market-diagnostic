#!/usr/bin/env python3
"""Phase 4 – Q1 only: Female Labour Force Participation Rate (LFPR) statistics

Generates:
- outputs/phase_4_eda/q1_dataset_1_eda_result.csv
- outputs/phase_4_eda/q1_dataset_1_eda_validation.md

All calculations use only the Python standard library.
"""

import csv
import json
import statistics
import hashlib
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration / paths
# ---------------------------------------------------------------------------
DATASET1 = Path("outputs/dataset_1_profile/feature_engineered_dataset_1.csv")
OUTDIR = Path("outputs/phase_4_eda")
OUTDIR.mkdir(parents=True, exist_ok=True)
RESULT_CSV = OUTDIR / "q1_dataset_1_eda_result.csv"
VALID_MD = OUTDIR / "q1_dataset_1_eda_validation.md"

# ---------------------------------------------------------------------------
# Helper utilities
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

def agg_stats(values):
    clean = [v for v in values if v is not None]
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
# Load data and basic integrity checks
# ---------------------------------------------------------------------------
if not DATASET1.is_file():
    raise FileNotFoundError(f"Source dataset not found: {DATASET1}")

with DATASET1.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Expected dimensions
expected_rows = 22650
expected_cols = 14
integrity_messages = []
integrity_messages.append(f"Source file exists: {DATASET1}")
integrity_messages.append(f"Row count: {len(rows)} (expected {expected_rows})")
integrity_messages.append(f"Column count: {len(fieldnames)} (expected {expected_cols})")
integrity_messages.append(f"SHA-256 before processing: {sha256(DATASET1)}")

# Identify LFPR column name exactly as present
lfpr_column = None
for name in fieldnames:
    if "Labour Force Participation Rate" in name or "Labor Force Participation Rate" in name:
        lfpr_column = name
        break
if lfpr_column is None:
    raise KeyError("LFPR column not found in dataset")

# ---------------------------------------------------------------------------
# Filter Female rows
# ---------------------------------------------------------------------------
female_rows = [r for r in rows if r.get("Gender", "").strip().lower() == "female"]
total_female = len(female_rows)

# ---------------------------------------------------------------------------
# Gather values per year, handling missing LFPR
# ---------------------------------------------------------------------------
values_by_year = defaultdict(list)
missing_by_year = defaultdict(int)
for r in female_rows:
    year = r.get("Year_Numeric", "").strip()
    lfpr_raw = r.get(lfpr_column, "")
    lfpr = safe_float(lfpr_raw)
    if lfpr is None:
        missing_by_year[year] += 1
    else:
        values_by_year[year].append(lfpr)

missing_total = sum(missing_by_year.values())
valid_total = sum(len(v) for v in values_by_year.values())

# ---------------------------------------------------------------------------
# Compute per‑year statistics
# ---------------------------------------------------------------------------
result_rows = []
for year in sorted(values_by_year.keys()):
    stats = agg_stats(values_by_year[year])
    result_rows.append({
        "Question_ID": "Q1",
        "Dataset": "Dataset 1",
        "Year": year,
        "Filter": "Gender == Female",
        "Aggregation_Level": "Year",
        "Observation_Count": stats["count"],
        "Mean": stats["mean"],
        "Median": stats["median"],
        "Minimum": stats["min"],
        "Maximum": stats["max"],
        "Standard_Deviation": stats["std"],
        "Missing_Count": missing_by_year.get(year, 0),
        "Status": "OK",
    })

# Overall statistics across all years
overall_stats = agg_stats([v for lst in values_by_year.values() for v in lst])
result_rows.append({
    "Question_ID": "Q1",
    "Dataset": "Dataset 1",
    "Year": "All",
    "Filter": "Gender == Female",
    "Aggregation_Level": "All Years",
    "Observation_Count": overall_stats["count"],
    "Mean": overall_stats["mean"],
    "Median": overall_stats["median"],
    "Minimum": overall_stats["min"],
    "Maximum": overall_stats["max"],
    "Standard_Deviation": overall_stats["std"],
    "Missing_Count": missing_total,
    "Status": "OK",
})

# ---------------------------------------------------------------------------
# Write result CSV
# ---------------------------------------------------------------------------
fieldnames_out = [
    "Question_ID",
    "Dataset",
    "Year",
    "Filter",
    "Aggregation_Level",
    "Observation_Count",
    "Mean",
    "Median",
    "Minimum",
    "Maximum",
    "Standard_Deviation",
    "Missing_Count",
    "Status",
]
with RESULT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_out)
    writer.writeheader()
    for r in result_rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# Independent validation – recompute and compare to CSV content
# ---------------------------------------------------------------------------
with RESULT_CSV.open(newline="", encoding="utf-8") as f:
    csv_reader = csv.DictReader(f)
    csv_rows = list(csv_reader)

validation_table = []
for calc, stored in zip(result_rows, csv_rows):
    for key in ["Observation_Count", "Mean", "Median", "Minimum", "Maximum", "Standard_Deviation", "Missing_Count"]:
        calc_val = calc[key]
        stored_val = stored[key]
        # Convert stored string to number when possible
        try:
            stored_num = float(stored_val) if stored_val != "" else None
        except ValueError:
            stored_num = None
        diff = None
        if isinstance(calc_val, (int, float)) and isinstance(stored_num, (int, float)):
            diff = abs(calc_val - stored_num)
        status = "PASS" if diff is None or (diff is not None and diff < 1e-6) else "FAIL"
        validation_table.append({
            "Metric": key,
            "Result_File": stored_val,
            "Independent": calc_val,
            "Difference": diff if diff is not None else "N/A",
            "Status": status,
        })

# ---------------------------------------------------------------------------
# Validation markdown report
# ---------------------------------------------------------------------------
with VALID_MD.open("w", encoding="utf-8") as f:
    f.write("# Q1 – Female LFPR – Validation Report\n\n")
    f.write("## Source integrity\n")
    for msg in integrity_messages:
        f.write(f"- {msg}\n")
    f.write("\n")
    f.write(f"- Total female rows (before missing exclusion): {total_female}\n")
    f.write(f"- Valid LFPR observations: {valid_total}\n")
    f.write(f"- Missing LFPR observations: {missing_total}\n\n")
    f.write("## Per‑year statistics (as written)\n\n")
    f.write("| Year | Obs | Mean | Median | Min | Max | Std | Missing |\n")
    f.write("|------|----:|-----:|-------:|----:|----:|----:|--------:|\n")
    for r in result_rows:
        if r["Year"] == "All":
            continue
        f.write(f"| {r['Year']} | {r['Observation_Count']} | {r['Mean']} | {r['Median']} | {r['Minimum']} | {r['Maximum']} | {r['Standard_Deviation']} | {r['Missing_Count']} |\n")
    f.write("\n## Overall statistics\n\n")
    overall = result_rows[-1]
    f.write(f"- Observation_Count: {overall['Observation_Count']}\n")
    f.write(f"- Mean: {overall['Mean']}\n")
    f.write(f"- Median: {overall['Median']}\n")
    f.write(f"- Minimum: {overall['Minimum']}\n")
    f.write(f"- Maximum: {overall['Maximum']}\n")
    f.write(f"- Standard_Deviation: {overall['Standard_Deviation']}\n")
    f.write(f"- Missing_Count: {overall['Missing_Count']}\n\n")
    f.write("## Independent validation comparison\n\n")
    f.write("| Metric | Result File | Independent | Difference | Status |\n")
    f.write("|--------|------------:|------------:|-----------:|--------|\n")
    for entry in validation_table:
        f.write(f"| {entry['Metric']} | {entry['Result_File']} | {entry['Independent']} | {entry['Difference']} | {entry['Status']} |\n")
    f.write("\n## Final status\n\n")
    overall_status = "PASS" if all(e['Status'] == 'PASS' for e in validation_table) else "FAIL"
    f.write(f"**{overall_status}**\n")

print("Q1 analysis and validation completed. Files written to outputs/phase_4_eda/")
