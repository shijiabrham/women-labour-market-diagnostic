#!/usr/bin/env python3
"""Generate Q5 (state‑level female LFPR) and Q6 (state‑level female WPR) CSVs
and validation markdown files directly from the feature‑engineered Dataset 1.
The script follows the original methodology, uses three‑decimal rounding, counts
missing values, and does not perform any imputation.
"""

import csv, hashlib, statistics, sys
from pathlib import Path
from collections import defaultdict

# Paths
DATASET = Path("outputs/dataset_1_profile/feature_engineered_dataset_1.csv")
Q5_CSV = Path("outputs/phase_4_eda/q5_state_lfpr.csv")
Q5_VAL = Path("outputs/phase_4_eda/q5_state_lfpr_validation.md")
Q6_CSV = Path("outputs/phase_4_eda/q6_state_wpr.csv")
Q6_VAL = Path("outputs/phase_4_eda/q6_state_wpr_validation.md")

# Column names exactly as in source CSV
LFPR_COL = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
WPR_COL = "Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
GENDER = "female"
YEARS = ["2017","2018","2019","2020","2021","2022","2023"]

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_float(v: str):
    if v is None:
        return None
    s = v.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None

def agg(values):
    clean = [x for x in values if x is not None]
    n = len(clean)
    if n == 0:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None, "std": None}
    mean = statistics.mean(clean)
    median = statistics.median(clean)
    minv = min(clean)
    maxv = max(clean)
    std = statistics.pstdev(clean) if n > 1 else 0.0
    return {"count": n, "mean": round(mean,3), "median": round(median,3), "min": round(minv,3), "max": round(maxv,3), "std": round(std,3)}

if not DATASET.is_file():
    sys.exit(f"Source dataset not found: {DATASET}")
with DATASET.open(newline="", encoding="utf-8") as f:
    dr = csv.DictReader(f)
    rows = list(dr)
    header = dr.fieldnames
if LFPR_COL not in header or WPR_COL not in header:
    sys.exit("Required LFPR or WPR column missing in source CSV")

# ------------------- Q5 -------------------
lfpr_vals = defaultdict(lambda: defaultdict(list))
lfpr_miss = defaultdict(lambda: defaultdict(int))
lfpr_total = defaultdict(int)
for r in rows:
    if r.get("Gender", "").strip().lower() != GENDER:
        continue
    st = r.get("State", "").strip()
    yr = r.get("Year_Numeric", "").strip()
    lfpr_total[st] += 1
    val = safe_float(r.get(LFPR_COL, ""))
    if val is None:
        lfpr_miss[st][yr] += 1
    else:
        lfpr_vals[st][yr].append(val)

q5_rows = []
for st in sorted(lfpr_vals.keys()):
    for yr in sorted(lfpr_vals[st].keys(), key=int):
        stats = agg(lfpr_vals[st][yr])
        q5_rows.append({
            "Question_ID":"Q5","Dataset":"Dataset 1","State":st,"Year":yr,"Indicator":"LFPR",
            "Filter":"Gender == Female","Aggregation_Level":"Year",
            "Filtered_Row_Count":lfpr_total[st],"Valid_Observation_Count":stats["count"],
            "Mean":stats["mean"],"Median":stats["median"],"Minimum":stats["min"],"Maximum":stats["max"],
            "Population_Standard_Deviation":stats["std"],"Missing_Count":lfpr_miss[st].get(yr,0),"Status":"OK",
            "Value":stats["mean"],"Comparison":"","Notes":""})
    # All‑Years summary
    all_vals = [v for yrlist in lfpr_vals[st].values() for v in yrlist]
    all_stats = agg(all_vals)
    total_miss = sum(lfpr_miss[st].values())
    q5_rows.append({
        "Question_ID":"Q5","Dataset":"Dataset 1","State":st,"Year":"All","Indicator":"LFPR",
        "Filter":"Gender == Female","Aggregation_Level":"All Years",
        "Filtered_Row_Count":lfpr_total[st],"Valid_Observation_Count":all_stats["count"],
        "Mean":all_stats["mean"],"Median":all_stats["median"],"Minimum":all_stats["min"],"Maximum":all_stats["max"],
        "Population_Standard_Deviation":all_stats["std"],"Missing_Count":total_miss,"Status":"OK",
        "Value":all_stats["mean"],"Comparison":"","Notes":""})

header_fields = ["Question_ID","Dataset","State","Year","Indicator","Filter","Aggregation_Level",
                 "Filtered_Row_Count","Valid_Observation_Count","Mean","Median","Minimum","Maximum",
                 "Population_Standard_Deviation","Missing_Count","Status","Value","Comparison","Notes"]
with Q5_CSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header_fields)
    w.writeheader()
    for r in q5_rows:
        w.writerow(r)

# ------------------- Q6 -------------------
wpr_vals = defaultdict(lambda: defaultdict(list))
wpr_miss = defaultdict(lambda: defaultdict(int))
wpr_total = defaultdict(int)
for r in rows:
    if r.get("Gender", "").strip().lower() != GENDER:
        continue
    st = r.get("State", "").strip()
    yr = r.get("Year_Numeric", "").strip()
    if yr not in YEARS:
        continue
    wpr_total[st] += 1
    val = safe_float(r.get(WPR_COL, ""))
    if val is None:
        wpr_miss[st][yr] += 1
    else:
        wpr_vals[st][yr].append(val)

q6_rows = []
for st in sorted(wpr_vals.keys()):
    for yr in YEARS:
        stats = agg(wpr_vals[st].get(yr, []))
        missing = wpr_miss[st].get(yr,0)
        total = wpr_total[st] if yr in wpr_vals[st] else 0
        q6_rows.append({
            "Question_ID":"Q6","Dataset":"Dataset 1","State":st,"Year":yr,"Indicator":"WPR",
            "Filter":"Gender == Female","Aggregation_Level":"Year",
            "Filtered_Row_Count":total,"Valid_Observation_Count":stats["count"],
            "Mean":stats["mean"],"Median":stats["median"],"Minimum":stats["min"],"Maximum":stats["max"],
            "Population_Standard_Deviation":stats["std"],"Missing_Count":missing,"Status":"OK",
            "Value":stats["mean"],"Comparison":"","Notes":""})
    # All‑Years summary
    all_vals = [v for yrlist in wpr_vals[st].values() for v in yrlist]
    all_stats = agg(all_vals)
    total_missing = sum(wpr_miss[st].values())
    total_all = sum(wpr_total[st] for _ in YEARS)
    q6_rows.append({
        "Question_ID":"Q6","Dataset":"Dataset 1","State":st,"Year":"All","Indicator":"WPR",
        "Filter":"Gender == Female","Aggregation_Level":"All Years",
        "Filtered_Row_Count":total_all,"Valid_Observation_Count":all_stats["count"],
        "Mean":all_stats["mean"],"Median":all_stats["median"],"Minimum":all_stats["min"],"Maximum":all_stats["max"],
        "Population_Standard_Deviation":all_stats["std"],"Missing_Count":total_missing,"Status":"OK",
        "Value":all_stats["mean"],"Comparison":"","Notes":""})

with Q6_CSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header_fields)
    w.writeheader()
    for r in q6_rows:
        w.writerow(r)

# ------------------- Validation -------------------
TOL = 1e-6

def validate(orig, generated, key_fields):
    orig_map = {tuple(r[k] for k in key_fields): r for r in orig}
    gen_map = {tuple(r[k] for k in key_fields): r for r in generated}
    mism = []
    for k, o in orig_map.items():
        g = gen_map.get(k)
        if g is None:
            mism.append(f"Missing generated row {k}")
            continue
        for fld in ["Mean","Valid_Observation_Count","Missing_Count"]:
            ov = o.get(fld)
            gv = g.get(fld)
            if ov in ("", None) and gv in ("", None):
                continue
            try:
                ovf = float(ov) if ov not in ("", None) else None
                gvf = float(gv) if gv not in ("", None) else None
            except ValueError:
                ovf = ov; gvf = gv
            if ovf is None or gvf is None:
                if ovf != gvf:
                    mism.append(f"{k} field {fld} mismatch ({ov} vs {gv})")
            elif abs(ovf - gvf) > TOL:
                mism.append(f"{k} field {fld} diff {ovf} vs {gvf}")
    for k in gen_map:
        if k not in orig_map:
            mism.append(f"Extra generated row {k}")
    return (len(mism)==0, "\n".join(mism))

def read_csv(p):
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

q5_gen = read_csv(Q5_CSV)
q6_gen = read_csv(Q6_CSV)

q5_ok, q5_msg = validate(q5_rows, q5_gen, ["Question_ID","State","Year"])
q6_ok, q6_msg = validate(q6_rows, q6_gen, ["Question_ID","State","Year"])

with Q5_VAL.open("w", encoding="utf-8") as f:
    f.write("# Q5 Validation Report\n\n")
    f.write(f"**Overall Result:** {'PASS' if q5_ok else 'FAIL'}\n\n")
    f.write(f"- State/UT count (including All): {len(set([r['State'] for r in q5_rows]))}\n")
    f.write(f"- Total rows: {len(q5_rows)}\n")
    f.write("## Details\n\n")
    f.write(q5_msg + "\n")

with Q6_VAL.open("w", encoding="utf-8") as f:
    f.write("# Q6 Validation Report\n\n")
    f.write(f"**Overall Result:** {'PASS' if q6_ok else 'FAIL'}\n\n")
    f.write(f"- State/UT count (including All): {len(set([r['State'] for r in q6_rows]))}\n")
    f.write(f"- Total rows: {len(q6_rows)}\n")
    f.write("## Details\n\n")
    f.write(q6_msg + "\n")

print("Q5 and Q6 generation complete. Validation files written.")
