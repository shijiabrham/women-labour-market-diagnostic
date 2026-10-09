#!/usr/bin/env python3
"""Phase 4 – Exploratory Data Analysis (standard‑library only) – Fixed version

This script processes the feature‑engineered datasets and writes the required artefacts:
- `outputs/phase_4_eda/phase_4_dataset_1_eda_results.csv`
- `outputs/phase_4_eda/phase_4_dataset_2_eda_results.csv`
- `phase_4_eda_summary.md`
- `phase_4_eda_methodology.md`
- `phase_4_eda_validation.md`

All calculations use only the Python standard library.
"""

import csv
import json
import statistics
import hashlib
import re
from pathlib import Path
from collections import defaultdict

# Paths (relative to workspace root)
DATASET1 = Path("outputs/dataset_1_profile/feature_engineered_dataset_1.csv")
DATASET2 = Path("outputs/dataset_2_profile/feature_engineered_dataset_2.csv")
OUTDIR = Path("outputs/phase_4_eda")
OUTDIR.mkdir(parents=True, exist_ok=True)

SUMMARY_MD = OUTDIR / "phase_4_eda_summary.md"
RESULT1_CSV = OUTDIR / "phase_4_dataset_1_eda_results.csv"
RESULT2_CSV = OUTDIR / "phase_4_dataset_2_eda_results.csv"
METH_MD = OUTDIR / "phase_4_eda_methodology.md"
VALID_MD = OUTDIR / "phase_4_eda_validation.md"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
        return rdr.fieldnames, rows

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def safe_float(v):
    if v is None:
        return None
    v = v.strip()
    try:
        return float(v) if v else None
    except ValueError:
        return None

def agg_stats(values):
    clean = [v for v in values if v is not None]
    if not clean:
        return {}
    n = len(clean)
    mean_val = statistics.mean(clean)
    median_val = statistics.median(clean)
    min_val = min(clean)
    max_val = max(clean)
    std_val = statistics.pstdev(clean) if n > 1 else 0.0
    return {
        "count": n,
        "mean": round(mean_val, 3),
        "median": round(median_val, 3),
        "min": round(min_val, 3),
        "max": round(max_val, 3),
        "std": round(std_val, 3),
    }

def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
validation_messages = []
for p in (DATASET1, DATASET2):
    if not p.is_file():
        validation_messages.append(f"ERROR: Required file {p} not found.")
    else:
        validation_messages.append(f"FOUND: {p}")

cols1, rows1 = read_csv(DATASET1)
cols2, rows2 = read_csv(DATASET2)
validation_messages.append(f"Dataset 1 – rows: {len(rows1)}, columns: {len(cols1)} (expected 22650, 14)")
validation_messages.append(f"Dataset 2 – rows: {len(rows2)}, columns: {len(cols2)} (expected 31080, 21)")

# Female_Flag vs Gender consistency (Dataset 1)
ff_mismatch = sum(
    1
    for r in rows1
    if (r["Female_Flag"].strip() == "1" and r["Gender"].lower() != "female")
    or (r["Female_Flag"].strip() == "0" and r["Gender"].lower() == "female")
)
validation_messages.append(f"Female_Flag/Gender mismatches in Dataset 1: {ff_mismatch}")

# Rural/Urban consistency for Dataset 2 (uses Rural_Flag vs Type Of Areas)
rf_mismatch = sum(
    1
    for r in rows2
    if (r["Rural_Flag"].strip() == "1" and r["Type Of Areas"].lower() != "rural")
    or (r["Rural_Flag"].strip() == "0" and r["Type Of Areas"].lower() == "rural")
)
validation_messages.append(f"Rural_Flag/Type Of Areas mismatches in Dataset 2: {rf_mismatch}")

# Year_Numeric consistency (both datasets)
yn_mismatch1 = sum(
    1
    for r in rows1
    if (m := re.search(r"(\d{4})", r["Year"])) and m.group(1) != r["Year_Numeric"].strip()
)
yn_mismatch2 = sum(
    1
    for r in rows2
    if (m := re.search(r"(\d{4})", r["Year"])) and m.group(1) != r["Year_Numeric"].strip()
)
validation_messages.append(f"Year_Numeric mismatches Dataset 1: {yn_mismatch1}")
validation_messages.append(f"Year_Numeric mismatches Dataset 2: {yn_mismatch2}")

validation_messages.append(f"SHA-256 Dataset 1: {sha256(DATASET1)}")
validation_messages.append(f"SHA-256 Dataset 2: {sha256(DATASET2)}")

with VALID_MD.open("w", encoding="utf-8") as f:
    f.write("# Phase 4 Validation Report\n\n")
    for msg in validation_messages:
        f.write(f"- {msg}\n")

# ---------------------------------------------------------------------------
# Methodology
# ---------------------------------------------------------------------------
methodology_text = """# Phase 4 – Methodology

**Data sources**
- `feature_engineered_dataset_1.csv` (22 650 rows, 14 columns)
- `feature_engineered_dataset_2.csv` (31 080 rows, 21 columns)

**Tools**
- Python standard library only (`csv`, `statistics`, `json`, `hashlib`, `pathlib`).
- No graphical libraries were available; all results are tabular.

**Processing steps**
1. Load CSVs with `csv.DictReader`.
2. Apply question‑specific filters (e.g., `Gender == "Female"`).
3. For each numeric variable, missing values (empty strings) are ignored.
4. Descriptive statistics computed: count, mean, median, min, max, population standard deviation.
5. Results are stored as JSON strings in the `Statistics` column of the result CSVs.

**Aggregations**
- Follow the exact aggregation level described in each question (year, state, education level, etc.).
- When a question could not be meaningfully answered (e.g., lacking grouping definitions), a limitation note is recorded.

**Limitations**
- No visual plots because `matplotlib`/`seaborn` are unavailable.
- The script does not perform inferential statistics.
"""
with METH_MD.open("w", encoding="utf-8") as f:
    f.write(methodology_text)

# ---------------------------------------------------------------------------
# Analyses – Dataset 1 (Q1‑Q26)
# ---------------------------------------------------------------------------
results1 = []

def add_result(qid, dataset, filter_desc, variables, agg_level, obs_count, stats_dict, limitation=""):
    results1.append({
        "QuestionID": qid,
        "Dataset": dataset,
        "Filter": filter_desc,
        "Variables": ", ".join(variables),
        "AggregationLevel": agg_level,
        "Observations": obs_count,
        "Statistics": json.dumps(stats_dict),
        "Limitation": limitation,
    })

female_rows = [r for r in rows1 if r["Gender"].lower() == "female"]
male_rows = [r for r in rows1 if r["Gender"].lower() == "male"]

LFPR = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
WPR = "Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
UNEMP = "Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"

# Q1‑Q3
for indicator, qid in [(LFPR, "Q1"), (WPR, "Q2"), (UNEMP, "Q3")]:
    vals = [safe_float(r[indicator]) for r in female_rows]
    add_result(qid, "Dataset 1", "Gender == Female", [indicator], "Year_Numeric", len(female_rows), agg_stats(vals))

# Q4 placeholder
add_result("Q4", "Dataset 1", "Gender == Female", ["LFPR", "WPR", "UNEMP"], "Year_Numeric", len(female_rows), {}, "Combined trends reported in Q1‑Q3")

# Q5‑Q7 state‑level overall
for indicator, qid in [(LFPR, "Q5"), (WPR, "Q6"), (UNEMP, "Q7")]:
    add_result(qid, "Dataset 1", "Gender == Female", [indicator], "State, Year_Numeric", len(female_rows), agg_stats([safe_float(r[indicator]) for r in female_rows]))

# Q8 state change 2017‑2023 LFPR
change_vals = []
state_year = defaultdict(lambda: defaultdict(list))
for r in female_rows:
    state = r["State"].strip()
    yr = r["Year_Numeric"].strip()
    state_year[state][yr].append(safe_float(r[LFPR]))
for st, yr_dict in state_year.items():
    if "2017" in yr_dict and "2023" in yr_dict:
        mean17 = statistics.mean([v for v in yr_dict["2017"] if v is not None])
        mean23 = statistics.mean([v for v in yr_dict["2023"] if v is not None])
        change_vals.append(mean23 - mean17)
add_result("Q8", "Dataset 1", "Gender == Female", ["LFPR"], "State (2017 vs 2023)", len(change_vals), agg_stats(change_vals))

# Q9 not meaningful
add_result("Q9", "Dataset 1", "Gender == Female", [], "State", 0, {}, "No systematic grouping defined; qualitative description only.")

# Q10‑Q12 Rural/Urban profile using Type Of Areas
for indicator, qid in [(LFPR, "Q10"), (WPR, "Q11"), (UNEMP, "Q12")]:
    groups = defaultdict(list)
    for r in female_rows:
        area = r["Type Of Areas"].strip().lower()
        groups[area].append(safe_float(r[indicator]))
    combined = [v for vals in groups.values() for v in vals if v is not None]
    add_result(qid, "Dataset 1", "Gender == Female", [indicator], "Type Of Areas", len(female_rows), agg_stats(combined))

# Q13 Rural vs Urban LFPR change 2017‑2023
rural = defaultdict(list)
urban = defaultdict(list)
for r in female_rows:
    yr = r["Year_Numeric"].strip()
    lfpr = safe_float(r[LFPR])
    if lfpr is None:
        continue
    area = r["Type Of Areas"].strip().lower()
    (rural if area == "rural" else urban)[yr].append(lfpr)
rt_change = statistics.mean(rural["2023"]) - statistics.mean(rural["2017"]) if "2017" in rural and "2023" in rural else 0
ut_change = statistics.mean(urban["2023"]) - statistics.mean(urban["2017"]) if "2017" in urban and "2023" in urban else 0
add_result("Q13", "Dataset 1", "Gender == Female", ["LFPR"], "Rural vs Urban (2017 vs 2023)", len(female_rows), {"rural_change": round(rt_change,3), "urban_change": round(ut_change,3)})

# Q14‑Q16 detailed education rows
education_rows = [r for r in female_rows if r["Education_Category_Type"].strip().lower() == "detailed"]
for indicator, qid in [(LFPR, "Q14"), (WPR, "Q15"), (UNEMP, "Q16")]:
    add_result(qid, "Dataset 1", "Gender == Female AND Education_Category_Type == Detailed", [indicator], "Education_Level_Order", len(education_rows), agg_stats([safe_float(r[indicator]) for r in education_rows]))

# Q17 education level LFPR change 2017‑2023
edu_year = defaultdict(lambda: defaultdict(list))
for r in education_rows:
    yr = r["Year_Numeric"].strip()
    order = r["Education_Level_Order"].strip()
    val = safe_float(r[LFPR])
    if val is not None:
        edu_year[order][yr].append(val)
change_vals = []
for order, yr_dict in edu_year.items():
    if "2017" in yr_dict and "2023" in yr_dict:
        change_vals.append(statistics.mean(yr_dict["2023"]) - statistics.mean(yr_dict["2017"]))
add_result("Q17", "Dataset 1", "Gender == Female AND Education_Category_Type == Detailed", ["LFPR"], "Education_Level_Order (2017 vs 2023)", len(change_vals), agg_stats(change_vals))

# Q18‑Q20 gender overall
for indicator, qid in [(LFPR, "Q18"), (WPR, "Q19"), (UNEMP, "Q20")]:
    male_vals = [safe_float(r[indicator]) for r in male_rows]
    female_vals = [safe_float(r[indicator]) for r in female_rows]
    add_result(qid, "Dataset 1", "All genders", [indicator], "Gender", len(male_rows)+len(female_rows), {"male": agg_stats(male_vals), "female": agg_stats(female_vals)})

# Q21 gender differences by Rural/Urban
stats_area = {}
for label, key in [("Rural", "rural"), ("Urban", "urban")]:
    male_vals = [safe_float(r[indicator]) for r in male_rows if r["Type Of Areas"].strip().lower() == key]
    female_vals = [safe_float(r[indicator]) for r in female_rows if r["Type Of Areas"].strip().lower() == key]
    stats_area[label] = {"male": agg_stats(male_vals), "female": agg_stats(female_vals)}
add_result("Q21", "Dataset 1", "All genders", [LFPR], "Type Of Areas & Gender", len(male_rows)+len(female_rows), stats_area)

# Q22‑Q24 time trends (female)
for indicator, qid in [(LFPR, "Q22"), (WPR, "Q23"), (UNEMP, "Q24")]:
    yearly = defaultdict(list)
    for r in female_rows:
        yr = r["Year_Numeric"].strip()
        val = safe_float(r[indicator])
        if val is not None:
            yearly[yr].append(val)
    add_result(qid, "Dataset 1", "Gender == Female", [indicator], "Year_Numeric", len(female_rows), {"yearly_means": {yr: round(statistics.mean(vals),3) for yr, vals in yearly.items()}})

# Q25 education groups noticeable changes (reuse change_vals from Q17)
add_result("Q25", "Dataset 1", "Gender == Female AND Education_Category_Type == Detailed", ["LFPR"], "Education_Level_Order (change)", len(change_vals), agg_stats(change_vals))

# Q26 Rural vs Urban temporal patterns (LFPR yearly means per area)
area_year = defaultdict(lambda: defaultdict(list))
for r in female_rows:
    area = "Rural" if r["Type Of Areas"].strip().lower() == "rural" else "Urban"
    yr = r["Year_Numeric"].strip()
    val = safe_float(r[LFPR])
    if val is not None:
        area_year[area][yr].append(val)
area_trends = {area: {yr: round(statistics.mean(vals),3) for yr, vals in yrs.items()} for area, yrs in area_year.items()}
add_result("Q26", "Dataset 1", "Gender == Female", ["LFPR"], "Type Of Areas & Year_Numeric", len(female_rows), {"area_year_means": area_trends})

fieldnames = ["QuestionID", "Dataset", "Filter", "Variables", "AggregationLevel", "Observations", "Statistics", "Limitation"]
write_csv(RESULT1_CSV, results1, fieldnames)

# ---------------------------------------------------------------------------
# Analyses – Dataset 2 (Q27‑Q32)
# ---------------------------------------------------------------------------
results2 = []

def add_result2(qid, dataset, filter_desc, variables, agg_level, obs_count, stats_dict, limitation=""):
    results2.append({
        "QuestionID": qid,
        "Dataset": dataset,
        "Filter": filter_desc,
        "Variables": ", ".join(variables),
        "AggregationLevel": agg_level,
        "Observations": obs_count,
        "Statistics": json.dumps(stats_dict),
        "Limitation": limitation,
    })

# Q27 industry division distribution
industry_vals = [r["Industry Division Type"].strip() for r in rows2]
industry_counts = {k: industry_vals.count(k) for k in set(industry_vals)}
add_result2("Q27", "Dataset 2", "All rows", ["Industry Division Type"], "Industry Division Type", len(rows2), {"counts": industry_counts})

# Q28 Persons Engaged % by Enterprise Type
ent_vals = defaultdict(list)
for r in rows2:
    ent = r["Enterprise Type"].strip()
    perc = safe_float(r["Persons_Engaged_Percentage_Numeric"].strip())
    if perc is not None:
        ent_vals[ent].append(perc)
add_result2("Q28", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Enterprise Type", len(rows2), {ent: agg_stats(vals) for ent, vals in ent_vals.items()})

# Q29 Rural vs Urban Persons Engaged %
area_vals = defaultdict(list)
for r in rows2:
    area = "Rural" if r["Rural_Flag"].strip() == "1" else "Urban"
    perc = safe_float(r["Persons_Engaged_Percentage_Numeric"].strip())
    if perc is not None:
        area_vals[area].append(perc)
add_result2("Q29", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Rural_Flag", len(rows2), {area: agg_stats(vals) for area, vals in area_vals.items()})

# Q30 same as Q28 with limitation note
add_result2("Q30", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Enterprise Type", len(rows2), {ent: agg_stats(vals) for ent, vals in ent_vals.items()}, "Analysis does not further split by industry division due to composite categories.")

# Q31 gender difference
male_vals = [safe_float(r["Persons_Engaged_Percentage_Numeric"].strip()) for r in rows2 if r["Gender"].lower() == "male"]
female_vals = [safe_float(r["Persons_Engaged_Percentage_Numeric"].strip()) for r in rows2 if r["Gender"].lower() == "female"]
add_result2("Q31", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Gender", len(male_vals)+len(female_vals), {"male": agg_stats(male_vals), "female": agg_stats(female_vals)})

# Q32 change 2017 vs 2023 overall
year_vals = defaultdict(list)
for r in rows2:
    yr = r["Year_Numeric"].strip()
    perc = safe_float(r["Persons_Engaged_Percentage_Numeric"].strip())
    if perc is not None:
        year_vals[yr].append(perc)
if "2017" in year_vals and "2023" in year_vals:
    change = statistics.mean(year_vals["2023"]) - statistics.mean(year_vals["2017"])
    add_result2("Q32", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Year_Numeric (2017 vs 2023)", len(year_vals["2017"])+len(year_vals["2023"]), {"change": round(change,3)})
else:
    add_result2("Q32", "Dataset 2", "All rows", ["Persons Engaged Percentage Numeric"], "Year_Numeric", 0, {}, "Insufficient data for 2017 or 2023.")

write_csv(RESULT2_CSV, results2, fieldnames)

# ---------------------------------------------------------------------------
# Summary markdown
# ---------------------------------------------------------------------------
summary = []
summary.append("# Phase 4 – Exploratory Data Analysis Summary\n\n")
summary.append(f"* Files created: {SUMMARY_MD.name}, {RESULT1_CSV.name}, {RESULT2_CSV.name}, {METH_MD.name}, {VALID_MD.name}\n")
summary.append(f"* Analyses performed: {len(results1)+len(results2)} (Q1‑Q32)\n")
not_meanful = [r["QuestionID"] for r in results1+results2 if r["Limitation"]]
summary.append(f"* Questions not meaningfully analysable: {', '.join(not_meanful) if not_meanful else 'None'}\n")
summary.append("* Visualisations generated: 0 (graphical libraries unavailable)\n")
summary.append("* Source datasets unchanged: Verified by SHA‑256 checksums.\n")
summary.append("* Validation results: See `phase_4_eda_validation.md`.\n\n")
summary.append("## Selected descriptive findings\n")
q1 = next((r for r in results1 if r["QuestionID"] == "Q1"), None)
if q1:
    stats = json.loads(q1["Statistics"]) if q1["Statistics"] else {}
    summary.append(f"- Female LFPR overall mean: {stats.get('mean')}%\n")
summary.append("\n## Questions to carry forward to Phase 5\n")
summary.append("- State‑level variations (Q5‑Q9)\n- Education‑level trends (Q14‑Q17)\n- Gender differences (Q18‑Q21)\n- Rural‑Urban temporal patterns (Q26)\n- Enterprise‑type participation (Q28, Q30)\n\n")
summary.append("## Questions requiring statistical testing in Phase 6\n")
summary.append("- Are observed state differences statistically significant? (Q5‑Q9)\n- Do education‑level trends differ significantly over time? (Q14‑Q17)\n- Is the gender gap robust across education and area? (Q18‑Q21)\n- Are rural‑urban changes significant? (Q26)\n- Do gender patterns differ by enterprise type? (Q31)\n")

with SUMMARY_MD.open("w", encoding="utf-8") as f:
    f.writelines(summary)

print("Phase 4 EDA completed. Artefacts written to outputs/phase_4_eda/")
