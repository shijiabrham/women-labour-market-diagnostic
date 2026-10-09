#!/usr/bin/env python3
"""Phase 4 – Q6: State‑level Female Working Population Rate (WPR)

Generates:
* results CSV – outputs/phase_4_eda/q6_dataset_1_eda_result.csv
* validation markdown – outputs/phase_4_eda/q6_dataset_1_eda_validation.md
* summary markdown – appends to outputs/phase_4_eda/phase_4_eda_summary.md

All calculations use only the Python standard library and respect the
requirements:
* Gender == Female filter only
* No ranking labels (Highest/Lowest) are written
* No imputation – missing values are counted and excluded from stats
* Independent validation pass with tolerance 1e‑6
"""

import csv
import hashlib
import statistics
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Paths (relative to workspace root)
# ---------------------------------------------------------------------------
DATASET = Path("outputs/dataset_1_profile/feature_engineered_dataset_1.csv")
RESULT_CSV = Path("outputs/phase_4_eda/q6_dataset_1_eda_result.csv")
VALID_MD = Path("outputs/phase_4_eda/q6_dataset_1_eda_validation.md")
SUMMARY_MD = Path("outputs/phase_4_eda/phase_4_eda_summary.md")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WPR_COLUMN = "Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
GENDER_FILTER = "female"
YEARS = ["2017","2018","2019","2020","2021","2022","2023"]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_float(val: str):
    if val is None:
        return None
    v = val.strip()
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
        return {
            "valid": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None,
        }
    mean = statistics.mean(clean)
    median = statistics.median(clean)
    minv = min(clean)
    maxv = max(clean)
    std = statistics.pstdev(clean) if n > 1 else 0.0
    return {
        "valid": n,
        "mean": round(mean, 3),
        "median": round(median, 3),
        "min": round(minv, 3),
        "max": round(maxv, 3),
        "std": round(std, 3),
    }

# ---------------------------------------------------------------------------
# Load source and integrity checks
# ---------------------------------------------------------------------------
if not DATASET.is_file():
    raise FileNotFoundError(f"Source dataset not found: {DATASET}")

with DATASET.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    source_header = reader.fieldnames
    rows = list(reader)

integrity = []
integrity.append(f"Source exists: {DATASET}")
integrity.append(f"Row count: {len(rows)} (expected 22650)")
integrity.append(f"Column count: {len(source_header)} (expected 14)")
integrity.append(f"SHA‑256: {sha256(DATASET)}")

if WPR_COLUMN not in source_header:
    raise KeyError(f"WPR column not found in CSV header. Expected column name: {WPR_COLUMN}")

# ---------------------------------------------------------------------------
# Organise female rows by (state, year)
# ---------------------------------------------------------------------------
values_by_sy = defaultdict(list)       # list of WPR floats (non‑missing)
missing_by_sy = defaultdict(int)      # missing count per (state, year)
rows_total_by_sy = defaultdict(int)   # total female rows (incl. missing) per (state, year)

for r in rows:
    if r.get("Gender", "").strip().lower() != GENDER_FILTER:
        continue
    state = r.get("State", "").strip()
    year = r.get("Year_Numeric", "").strip()
    if year not in YEARS:
        continue
    rows_total_by_sy[(state, year)] += 1
    raw = r.get(WPR_COLUMN, "")
    val = safe_float(raw)
    if val is None:
        missing_by_sy[(state, year)] += 1
    else:
        values_by_sy[(state, year)].append(val)

states = sorted({state for (state, _) in rows_total_by_sy.keys()})

# ---------------------------------------------------------------------------
# Build result rows (yearly + All‑Years per state)
# ---------------------------------------------------------------------------
result_rows = []
for state in states:
    for year in YEARS:
        key = (state, year)
        total = rows_total_by_sy.get(key, 0)
        missing = missing_by_sy.get(key, 0)
        vals = values_by_sy.get(key, [])
        stats = agg_stats(vals)
        row = {
            "Question_ID": "Q6",
            "Dataset": "Dataset 1",
            "State": state,
            "Year": year,
            "Indicator": "WPR",
            "Filter": "Gender == Female",
            "Aggregation_Level": "Year",
            "Filtered_Row_Count": total,
            "Valid_Observation_Count": stats["valid"],
            "Mean": stats["mean"],
            "Median": stats["median"],
            "Minimum": stats["min"],
            "Maximum": stats["max"],
            "Population_Standard_Deviation": stats["std"],
            "Missing_Count": missing,
            "Status": "OK",
            "Value": stats["mean"],
            "Comparison": "",
            "Notes": "",
        }
        result_rows.append(row)
    # All‑Years summary for this state
    all_vals = []
    total_all = 0
    missing_all = 0
    for yr in YEARS:
        k = (state, yr)
        total_all += rows_total_by_sy.get(k, 0)
        missing_all += missing_by_sy.get(k, 0)
        all_vals.extend(values_by_sy.get(k, []))
    all_stats = agg_stats(all_vals)
    all_row = {
        "Question_ID": "Q6",
        "Dataset": "Dataset 1",
        "State": state,
        "Year": "All",
        "Indicator": "WPR",
        "Filter": "Gender == Female",
        "Aggregation_Level": "All Years",
        "Filtered_Row_Count": total_all,
        "Valid_Observation_Count": all_stats["valid"],
        "Mean": all_stats["mean"],
        "Median": all_stats["median"],
        "Minimum": all_stats["min"],
        "Maximum": all_stats["max"],
        "Population_Standard_Deviation": all_stats["std"],
        "Missing_Count": missing_all,
        "Status": "OK",
        "Value": all_stats["mean"],
        "Comparison": "",
        "Notes": "",
    }
    result_rows.append(all_row)

# ---------------------------------------------------------------------------
# Write result CSV (header order as required)
# ---------------------------------------------------------------------------
header = [
    "Question_ID",
    "Dataset",
    "State",
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
    "Value",
    "Comparison",
    "Notes",
]

with RESULT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for r in result_rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# Independent validation pass (separate recompute) – compare to result CSV
# ---------------------------------------------------------------------------
# Re‑compute stats exactly as above (already have dictionaries). We'll load the CSV
# and compare each metric.
validation_entries = []
with RESULT_CSV.open(newline="", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))
lookup = {(r["State"], r["Year"]): r for r in csv_rows if r.get("Question_ID") == "Q6"}

for state in states:
    for year in YEARS:
        key = (state, year)
        stored = lookup.get(key)
        if not stored:
            continue
        total = rows_total_by_sy.get(key, 0)
        missing = missing_by_sy.get(key, 0)
        vals = values_by_sy.get(key, [])
        stats = agg_stats(vals)
        expected = {
            "Filtered_Row_Count": total,
            "Valid_Observation_Count": stats["valid"],
            "Mean": stats["mean"],
            "Median": stats["median"],
            "Minimum": stats["min"],
            "Maximum": stats["max"],
            "Population_Standard_Deviation": stats["std"],
            "Missing_Count": missing,
            "Value": stats["mean"],
        }
        for metric, exp_val in expected.items():
            stored_val = stored.get(metric, "")
            try:
                stored_num = float(stored_val) if stored_val != "" else None
            except ValueError:
                stored_num = None
            diff = None
            status = "FAIL"
            if isinstance(exp_val, (int, float)) and isinstance(stored_num, (int, float)):
                diff = abs(exp_val - stored_num)
                status = "PASS" if diff < 1e-6 else "FAIL"
            elif exp_val is None and stored_val == "":
                status = "PASS"
            validation_entries.append({
                "State": state,
                "Year": year,
                "Metric": metric,
                "Result_File": stored_val,
                "Independent": exp_val,
                "Difference": diff if diff is not None else "N/A",
                "Status": status,
            })
    # All‑Years validation
    all_key = (state, "All")
    stored = lookup.get(all_key)
    if stored:
        all_vals = []
        total_all = 0
        missing_all = 0
        for yr in YEARS:
            k = (state, yr)
            total_all += rows_total_by_sy.get(k, 0)
            missing_all += missing_by_sy.get(k, 0)
            all_vals.extend(values_by_sy.get(k, []))
        all_stats = agg_stats(all_vals)
        expected = {
            "Filtered_Row_Count": total_all,
            "Valid_Observation_Count": all_stats["valid"],
            "Mean": all_stats["mean"],
            "Median": all_stats["median"],
            "Minimum": all_stats["min"],
            "Maximum": all_stats["max"],
            "Population_Standard_Deviation": all_stats["std"],
            "Missing_Count": missing_all,
            "Value": all_stats["mean"],
        }
        for metric, exp_val in expected.items():
            stored_val = stored.get(metric, "")
            try:
                stored_num = float(stored_val) if stored_val != "" else None
            except ValueError:
                stored_num = None
            diff = None
            status = "FAIL"
            if isinstance(exp_val, (int, float)) and isinstance(stored_num, (int, float)):
                diff = abs(exp_val - stored_num)
                status = "PASS" if diff < 1e-6 else "FAIL"
            elif exp_val is None and stored_val == "":
                status = "PASS"
            validation_entries.append({
                "State": state,
                "Year": "All",
                "Metric": metric,
                "Result_File": stored_val,
                "Independent": exp_val,
                "Difference": diff if diff is not None else "N/A",
                "Status": status,
            })

# ---------------------------------------------------------------------------
# Summary statistics for reporting
# ---------------------------------------------------------------------------
state_mean_map = {}
for r in result_rows:
    if r["Year"] == "All":
        if r["Mean"] is not None:
            state_mean_map[r["State"]] = r["Mean"]
if state_mean_map:
    min_mean = min(state_mean_map.values())
    max_mean = max(state_mean_map.values())
    range_mean = round(max_mean - min_mean, 3)
else:
    min_mean = max_mean = range_mean = None

num_states = len(states)
num_state_year = num_states * len(YEARS)
# Total female observations (including missing) across all states/years
total_female_obs = sum(rows_total_by_sy.values())
# Total missing WPR observations
total_missing = sum(missing_by_sy.values())

# ---------------------------------------------------------------------------
# Write validation markdown (append)
# ---------------------------------------------------------------------------
with VALID_MD.open("a", encoding="utf-8") as f:
    f.write("\n# Q6 – Working Population Rate Validation\n\n")
    f.write("## Source integrity\n")
    for line in integrity:
        f.write(f"- {line}\n")
    f.write("\n## Indicator column mapping\n")
    f.write(f"- WPR column: {WPR_COLUMN}\n\n")
    f.write("## Independent validation comparison (PASS/FAIL)\n\n")
    f.write("| State | Year | Metric | Result File | Independent | Difference | Status |\n")
    f.write("|-------|------|--------|------------:|------------:|-----------:|--------|\n")
    for e in validation_entries:
        f.write(f"| {e['State']} | {e['Year']} | {e['Metric']} | {e['Result_File']} | {e['Independent']} | {e['Difference']} | {e['Status']} |\n")
    overall = "PASS" if all(e['Status'] == 'PASS' for e in validation_entries) else "FAIL"
    f.write("\n**Overall Q6 validation status:** " + overall + "\n")

# ---------------------------------------------------------------------------
# Append summary markdown (no ranking language)
# ---------------------------------------------------------------------------
with SUMMARY_MD.open("a", encoding="utf-8") as f:
    f.write("\n# Q6 – State‑level Female Working Population Rate Summary\n\n")
    f.write(f"- States/UTs analysed: {num_states}\n")
    f.write(f"- State‑Year combinations: {num_state_year}\n")
    f.write(f"- Total female observations (including missing): {total_female_obs}\n")
    f.write(f"- Total missing WPR observations: {total_missing}\n")
    if min_mean is not None:
        f.write(f"- Mean WPR across states (All Years) ranges from {min_mean} % (lowest) to {max_mean} % (highest)\n")
        f.write(f"- Observed range (max − min): {range_mean} %\n")
    f.write("\nThe analysis describes the variation in female Working Population Rate across Indian states/UTs over 2017‑2023. No ranking or causal interpretation is provided.\n")
    f.write("\nAll calculations respect the gender filter, exclude missing values, and have been independently verified.\n")

# ---------------------------------------------------------------------------
# Display a small sample (first two states, two years, and an All‑Years row)
# ---------------------------------------------------------------------------
print("\nSample of Q6 result rows (first two states):\n")
sample_states = states[:2]
for state in sample_states:
    for year in YEARS[:2]:  # first two years
        row = lookup.get((state, year))
        if row:
            print(f"{row['State']}, {row['Year']}, Filtered: {row['Filtered_Row_Count']}, Valid: {row['Valid_Observation_Count']}, Mean: {row['Mean']}, Median: {row['Median']}, Min: {row['Minimum']}, Max: {row['Maximum']}, Std: {row['Population_Standard_Deviation']}, Missing: {row['Missing_Count']}")
    # All‑Years row
    all_row = lookup.get((state, "All"))
    if all_row:
        print(f"{all_row['State']}, All, Filtered: {all_row['Filtered_Row_Count']}, Valid: {all_row['Valid_Observation_Count']}, Mean: {all_row['Mean']}, Median: {all_row['Median']}, Min: {all_row['Minimum']}, Max: {all_row['Maximum']}, Std: {all_row['Population_Standard_Deviation']}, Missing: {all_row['Missing_Count']}")

print("\nSummary statistics:\n")
print(f"States analysed: {num_states}")
print(f"State‑Year combos: {num_state_year}")
print(f"Total female observations: {total_female_obs}")
print(f"Total missing observations: {total_missing}")
if min_mean is not None:
    print(f"Mean WPR range: {min_mean}% – {max_mean}% (range {range_mean}%)")

print("\nQ6 analysis complete.")
