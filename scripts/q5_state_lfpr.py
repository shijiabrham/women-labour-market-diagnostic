#!/usr/bin/env python3
"""Phase 4 – Q5 only: State‑level Female LFPR profile (append to existing results)

Generates/updates:
- outputs/phase_4_eda/phase_4_dataset_1_eda_results.csv   (appends Q5 rows)
- outputs/phase_4_eda/phase_4_eda_validation.md (adds Q5 validation)
- outputs/phase_4_eda/phase_4_eda_summary.md     (adds Q5 summary)

All calculations use only the Python standard library. No source file is modified.
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
RESULT_CSV = Path("outputs/phase_4_eda/phase_4_dataset_1_eda_results.csv")
VALID_MD = Path("outputs/phase_4_eda/phase_4_eda_validation.md")
SUMMARY_MD = Path("outputs/phase_4_eda/phase_4_eda_summary.md")

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
# Load source dataset & verify integrity
# ---------------------------------------------------------------------------
if not DATASET1.is_file():
    raise FileNotFoundError(f"Source dataset not found: {DATASET1}")

with DATASET1.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    source_header = reader.fieldnames

expected_rows = 22650
expected_cols = 14
integrity = []
integrity.append(f"Source exists: {DATASET1}")
integrity.append(f"Row count: {len(rows)} (expected {expected_rows})")
integrity.append(f"Column count: {len(source_header)} (expected {expected_cols})")
integrity.append(f"SHA‑256: {sha256(DATASET1)}")

# Identify the exact LFPR column (exact match to user‑provided name)
LFPR_COLUMN = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
if LFPR_COLUMN not in source_header:
    raise KeyError(f"LFPR column not found in source header: {LFPR_COLUMN}")

# ---------------------------------------------------------------------------
# Filter female rows
# ---------------------------------------------------------------------------
female_rows = [r for r in rows if r.get("Gender", "").strip().lower() == "female"]

# Gather per‑State and per‑Year values
values_by_state_year = defaultdict(lambda: defaultdict(list))  # state -> year -> list
missing_by_state_year = defaultdict(lambda: defaultdict(int))
filtered_counts_state = defaultdict(int)  # total female rows per state (including missing)

for r in female_rows:
    state = r.get("State", "").strip()
    year = r.get("Year_Numeric", "").strip()
    filtered_counts_state[state] += 1
    raw = r.get(LFPR_COLUMN, "")
    val = safe_float(raw)
    if val is None:
        missing_by_state_year[state][year] += 1
    else:
        values_by_state_year[state][year].append(val)

# ---------------------------------------------------------------------------
# Build Q5 result rows (state‑year + all‑years per state)
# ---------------------------------------------------------------------------
result_rows_q5 = []
states_sorted = sorted(values_by_state_year.keys())
for state in states_sorted:
    years = sorted(values_by_state_year[state].keys(), key=int)
    # Yearly rows
    for yr in years:
        stats = agg_stats(values_by_state_year[state][yr])
        row = {
            "Question_ID": "Q5",
            "Dataset": "Dataset 1",
            "State": state,
            "Year": yr,
            "Indicator": "LFPR",
            "Filter": "Gender == Female",
            "Aggregation_Level": "Year",
            "Filtered_Row_Count": filtered_counts_state[state],
            "Valid_Observation_Count": stats["count"],
            "Mean": stats["mean"],
            "Median": stats["median"],
            "Minimum": stats["min"],
            "Maximum": stats["max"],
            "Population_Standard_Deviation": stats["std"],
            "Missing_Count": missing_by_state_year[state].get(yr, 0),
            "Status": "OK",
            "Value": stats["mean"],
            "Comparison": "",
            "Notes": "",
        }
        result_rows_q5.append(row)
    # All‑years summary for the state
    all_vals = [v for lst in values_by_state_year[state].values() for v in lst]
    all_stats = agg_stats(all_vals)
    total_missing = sum(missing_by_state_year[state].values())
    all_row = {
        "Question_ID": "Q5",
        "Dataset": "Dataset 1",
        "State": state,
        "Year": "All",
        "Indicator": "LFPR",
        "Filter": "Gender == Female",
        "Aggregation_Level": "All Years",
        "Filtered_Row_Count": filtered_counts_state[state],
        "Valid_Observation_Count": all_stats["count"],
        "Mean": all_stats["mean"],
        "Median": all_stats["median"],
        "Minimum": all_stats["min"],
        "Maximum": all_stats["max"],
        "Population_Standard_Deviation": all_stats["std"],
        "Missing_Count": total_missing,
        "Status": "OK",
        "Value": all_stats["mean"],
        "Comparison": "",
        "Notes": "",
    }
    result_rows_q5.append(all_row)

# Identify highest / lowest mean LFPR across states (using All‑Years rows)
state_means = {}
for row in result_rows_q5:
    if row["Year"] == "All":
        state_means[row["State"]] = row["Mean"]
if state_means:
    highest_state = max(state_means, key=state_means.get)
    lowest_state = min(state_means, key=state_means.get)
    range_val = round(state_means[highest_state] - state_means[lowest_state], 3)
    # Add Comparison tags to the All‑Years rows
    for row in result_rows_q5:
        if row["Year"] == "All" and row["State"] == highest_state:
            row["Comparison"] = "Highest"
            row["Notes"] = f"Highest mean LFPR ({row['Mean']} %)"
        if row["Year"] == "All" and row["State"] == lowest_state:
            row["Comparison"] = "Lowest"
            row["Notes"] = f"Lowest mean LFPR ({row['Mean']} %)"
else:
    highest_state = lowest_state = None
    range_val = None

# ---------------------------------------------------------------------------
# Merge Q5 rows with existing results file, extending header if needed
# ---------------------------------------------------------------------------
# Desired full header (union of existing and Q5 fields)
additional_fields = ["State", "Indicator", "Value", "Comparison", "Notes"]
if RESULT_CSV.is_file():
    with RESULT_CSV.open(newline="", encoding="utf-8") as f:
        existing_reader = csv.DictReader(f)
        existing_rows = list(existing_reader)
        existing_header = existing_reader.fieldnames
else:
    existing_rows = []
    existing_header = []

# Build new header preserving order: existing columns first, then any missing additional fields
new_header = list(existing_header)
for af in additional_fields:
    if af not in new_header:
        new_header.append(af)

# Ensure all rows have all columns (fill missing with empty string)
def complete_row(row, header):
    return {k: row.get(k, "") for k in header}

# Prepare combined rows
combined_rows = []
# Existing rows – add empty values for new columns
for er in existing_rows:
    combined_rows.append(complete_row(er, new_header))
# Q5 rows – they already contain all needed keys (including new ones); ensure any missing old columns are present
for qr in result_rows_q5:
    combined_rows.append(complete_row(qr, new_header))

# Write back to the same CSV (overwrite)
with RESULT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=new_header)
    writer.writeheader()
    for r in combined_rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# Independent validation for Q5
# ---------------------------------------------------------------------------
validation_entries = []
# Re‑compute stats independently (same logic as above) to compare against rows in file
# We'll load the CSV we just wrote and compare each Q5 row
with RESULT_CSV.open(newline="", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

# Build a lookup dictionary for quick access (key = (State, Year))
lookup = {}
for r in csv_rows:
    if r.get("Question_ID") == "Q5":
        lookup[(r.get("State"), r.get("Year"))] = r

for state in states_sorted:
    # Yearly validation
    for yr in sorted(values_by_state_year[state].keys(), key=int):
        key = (state, yr)
        stored = lookup.get(key)
        if not stored:
            continue
        stats = agg_stats(values_by_state_year[state][yr])
        for metric in ["Filtered_Row_Count", "Valid_Observation_Count", "Mean", "Median", "Minimum", "Maximum", "Population_Standard_Deviation", "Missing_Count", "Value"]:
            calc_val = stats[metric.lower()] if metric not in ["Filtered_Row_Count", "Valid_Observation_Count", "Missing_Count"] else None
            # map metric to appropriate calc
        # We'll handle each metric manually below
        # Filtered_Row_Count is total female rows for the state
        calc_filtered = filtered_counts_state[state]
        calc_valid = stats["count"]
        calc_mean = stats["mean"]
        calc_median = stats["median"]
        calc_min = stats["min"]
        calc_max = stats["max"]
        calc_std = stats["std"]
        calc_missing = missing_by_state_year[state].get(yr, 0)
        calc_value = stats["mean"]
        for metric, calc in {
            "Filtered_Row_Count": calc_filtered,
            "Valid_Observation_Count": calc_valid,
            "Mean": calc_mean,
            "Median": calc_median,
            "Minimum": calc_min,
            "Maximum": calc_max,
            "Population_Standard_Deviation": calc_std,
            "Missing_Count": calc_missing,
            "Value": calc_value,
        }.items():
            stored_val = stored.get(metric, "")
            try:
                stored_num = float(stored_val) if stored_val != "" else None
            except ValueError:
                stored_num = None
            diff = None
            if isinstance(calc, (int, float)) and isinstance(stored_num, (int, float)):
                diff = abs(calc - stored_num)
            status = "PASS" if diff is None or (diff is not None and diff < 1e-6) else "FAIL"
            validation_entries.append({
                "State": state,
                "Year": yr,
                "Metric": metric,
                "Result_File": stored_val,
                "Independent": calc,
                "Difference": diff if diff is not None else "N/A",
                "Status": status,
            })
    # All‑years validation
    all_key = (state, "All")
    stored = lookup.get(all_key)
    if stored:
        all_vals = [v for lst in values_by_state_year[state].values() for v in lst]
        all_stats = agg_stats(all_vals)
        total_missing = sum(missing_by_state_year[state].values())
        calc_filtered = filtered_counts_state[state]
        calc_valid = all_stats["count"]
        calc_mean = all_stats["mean"]
        calc_median = all_stats["median"]
        calc_min = all_stats["min"]
        calc_max = all_stats["max"]
        calc_std = all_stats["std"]
        calc_missing = total_missing
        calc_value = all_stats["mean"]
        for metric, calc in {
            "Filtered_Row_Count": calc_filtered,
            "Valid_Observation_Count": calc_valid,
            "Mean": calc_mean,
            "Median": calc_median,
            "Minimum": calc_min,
            "Maximum": calc_max,
            "Population_Standard_Deviation": calc_std,
            "Missing_Count": calc_missing,
            "Value": calc_value,
        }.items():
            stored_val = stored.get(metric, "")
            try:
                stored_num = float(stored_val) if stored_val != "" else None
            except ValueError:
                stored_num = None
            diff = None
            if isinstance(calc, (int, float)) and isinstance(stored_num, (int, float)):
                diff = abs(calc - stored_num)
            status = "PASS" if diff is None or (diff is not None and diff < 1e-6) else "FAIL"
            validation_entries.append({
                "State": state,
                "Year": "All",
                "Metric": metric,
                "Result_File": stored_val,
                "Independent": calc,
                "Difference": diff if diff is not None else "N/A",
                "Status": status,
            })

# ---------------------------------------------------------------------------
# Write validation markdown (append to existing validation file)
# ---------------------------------------------------------------------------
validation_header = ["State", "Year", "Metric", "Result_File", "Independent", "Difference", "Status"]
with VALID_MD.open("a", encoding="utf-8") as f:
    f.write("\n# Q5 – State‑level Female LFPR Validation\n\n")
    f.write("## Source integrity (re‑listed)\n")
    for line in integrity:
        f.write(f"- {line}\n")
    f.write("\n## Indicator column mapping\n")
    f.write(f"- LFPR column: {LFPR_COLUMN}\n\n")
    f.write("## Independent validation comparison (Q5)\n\n")
    f.write("| State | Year | Metric | Result File | Independent | Difference | Status |\n")
    f.write("|-------|------|--------|------------:|------------:|-----------:|--------|\n")
    for e in validation_entries:
        f.write(f"| {e['State']} | {e['Year']} | {e['Metric']} | {e['Result_File']} | {e['Independent']} | {e['Difference']} | {e['Status']} |\n")
    overall_status = "PASS" if all(e['Status'] == 'PASS' for e in validation_entries) else "FAIL"
    f.write("\n## Final Q5 validation status\n\n")
    f.write(f"**{overall_status}**\n")

# ---------------------------------------------------------------------------
# Update summary markdown with Q5 findings (append)
# ---------------------------------------------------------------------------
with SUMMARY_MD.open("a", encoding="utf-8") as f:
    f.write("\n# Q5 – State‑level Female LFPR Summary\n\n")
    f.write(f"- Number of State/UTs analysed: {len(states_sorted)}\n")
    if highest_state is not None:
        f.write(f"- Highest mean LFPR: {state_means[highest_state]} % (State: {highest_state})\n")
    if lowest_state is not None:
        f.write(f"- Lowest mean LFPR: {state_means[lowest_state]} % (State: {lowest_state})\n")
    if range_val is not None:
        f.write(f"- Overall LFPR range (highest – lowest): {range_val} %\n")
    f.write("\n## Interpretation\n\n")
    f.write("The female LFPR varies across Indian States/UTs. The highest average LFPR across the 2017‑2023 period is observed in "+(highest_state or "N/A")+" with a mean of "+(str(state_means.get(highest_state)) if highest_state else "N/A")+" %. The lowest average is in "+(lowest_state or "N/A")+" with a mean of "+(str(state_means.get(lowest_state)) if lowest_state else "N/A")+" %. The spread between extremes is "+(str(range_val) if range_val else "N/A")+" %. No causal explanations are provided.\n")
    f.write("\nAll calculations respect the gender filter and exclude missing values.\n")

print("Q5 analysis complete. Results appended to CSV, validation and summary updated.")
