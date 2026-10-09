#!/usr/bin/env python3
"""Phase 4 – Q3 only: Female Unemployment Rate (UR) statistics

Generates:
- outputs/phase_4_eda/q3_dataset_1_eda_result.csv
- outputs/phase_4_eda/q3_dataset_1_eda_validation.md

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
RESULT_CSV = OUTDIR / "q3_dataset_1_eda_result.csv"
VALID_MD = OUTDIR / "q3_dataset_1_eda_validation.md"

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
# Identify Unemployment Rate column
# ---------------------------------------------------------------------------
ur_col = None
for name in header:
    if "Unemployment Rate" in name:
        ur_col = name
        break
if ur_col is None:
    raise KeyError("Unemployment Rate column not found in header")

# ---------------------------------------------------------------------------
# Filter female rows
# ---------------------------------------------------------------------------
female_rows = [r for r in rows if r.get("Gender", "").strip().lower() == "female"]
filtered_count = len(female_rows)

# ---------------------------------------------------------------------------
# Gather values per year
# ---------------------------------------------------------------------------
values_by_year = defaultdict(list)
missing_by_year = defaultdict(int)
for r in female_rows:
    year = r.get("Year_Numeric", "").strip()
    raw = r.get(ur_col, "")
    val = safe_float(raw)
    if val is None:
        missing_by_year[year] += 1
    else:
        values_by_year[year].append(val)

missing_total = sum(missing_by_year.values())
valid_total = sum(len(v) for v in values_by_year.values())

# ---------------------------------------------------------------------------
# Build result rows
# ---------------------------------------------------------------------------
result_rows = []
for yr in sorted(values_by_year.keys()):
    stats = agg_stats(values_by_year[yr])
    result_rows.append({
        "Question_ID": "Q3",
        "Dataset": "Dataset 1",
        "Year": yr,
        "Filter": "Gender == Female",
        "Aggregation_Level": "Year",
        "Filtered_Row_Count": filtered_count,
        "Valid_Observation_Count": stats["count"],
        "Mean": stats["mean"],
        "Median": stats["median"],
        "Minimum": stats["min"],
        "Maximum": stats["max"],
        "Population_Standard_Deviation": stats["std"],
        "Missing_Count": missing_by_year.get(yr, 0),
        "Status": "OK",
    })

overall = agg_stats([v for lst in values_by_year.values() for v in lst])
result_rows.append({
    "Question_ID": "Q3",
    "Dataset": "Dataset 1",
    "Year": "All",
    "Filter": "Gender == Female",
    "Aggregation_Level": "All Years",
    "Filtered_Row_Count": filtered_count,
    "Valid_Observation_Count": overall["count"],
    "Mean": overall["mean"],
    "Median": overall["median"],
    "Minimum": overall["min"],
    "Maximum": overall["max"],
    "Population_Standard_Deviation": overall["std"],
    "Missing_Count": missing_total,
    "Status": "OK",
})

# ---------------------------------------------------------------------------
# Write CSV
# ---------------------------------------------------------------------------
fieldnames_out = [
    "Question_ID",
    "Dataset",
    "Year",
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
for calc, stored in zip(result_rows, csv_rows):
    for key in ["Filtered_Row_Count", "Valid_Observation_Count", "Mean", "Median", "Minimum", "Maximum", "Population_Standard_Deviation", "Missing_Count"]:
        calc_val = calc[key]
        stored_val = stored[key]
        try:
            stored_num = float(stored_val) if stored_val != "" else None
        except ValueError:
            stored_num = None
        diff = None
        if isinstance(calc_val, (int, float)) and isinstance(stored_num, (int, float)):
            diff = abs(calc_val - stored_num)
        status = "PASS" if diff is None or (diff is not None and diff < 1e-6) else "FAIL"
        validation_entries.append({
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
    f.write("# Q3 – Female Unemployment Rate – Validation Report\n\n")
    f.write("## Source integrity\n")
    for line in integrity:
        f.write(f"- {line}\n")
    f.write("\n")
    f.write(f"- Filtered female rows: {filtered_count}\n")
    f.write(f"- Valid UR observations: {valid_total}\n")
    f.write(f"- Missing UR observations: {missing_total}\n\n")
    f.write("## Per‑year statistics (as written)\n\n")
    f.write("| Year | Filtered | Valid | Mean | Median | Min | Max | Std | Missing |\n")
    f.write("|------|--------:|------:|-----:|-------:|----:|----:|----:|--------:|\n")
    for r in result_rows:
        if r["Year"] == "All":
            continue
        f.write(f"| {r['Year']} | {r['Filtered_Row_Count']} | {r['Valid_Observation_Count']} | {r['Mean']} | {r['Median']} | {r['Minimum']} | {r['Maximum']} | {r['Population_Standard_Deviation']} | {r['Missing_Count']} |\n")
    f.write("\n## Overall statistics\n\n")
    o = result_rows[-1]
    f.write(f"- Filtered female rows: {o['Filtered_Row_Count']}\n")
    f.write(f"- Valid UR observations: {o['Valid_Observation_Count']}\n")
    f.write(f"- Missing UR observations: {o['Missing_Count']}\n")
    f.write(f"- Mean: {o['Mean']}\n")
    f.write(f"- Median: {o['Median']}\n")
    f.write(f"- Minimum: {o['Minimum']}\n")
    f.write(f"- Maximum: {o['Maximum']}\n")
    f.write(f"- Population SD: {o['Population_Standard_Deviation']}\n\n")
    f.write("## Independent validation comparison\n\n")
    f.write("| Metric | Result File | Independent | Difference | Status |\n")
    f.write("|--------|------------:|------------:|-----------:|--------|\n")
    for e in validation_entries:
        f.write(f"| {e['Metric']} | {e['Result_File']} | {e['Independent']} | {e['Difference']} | {e['Status']} |\n")
    f.write("\n## Final status\n\n")
    final = "PASS" if all(e['Status'] == 'PASS' for e in validation_entries) else "FAIL"
    f.write(f"**{final}**\n")

print("Q3 analysis complete. Results written to outputs/phase_4_eda/")
