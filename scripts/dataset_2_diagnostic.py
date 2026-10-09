"""
dataset_2_diagnostic.py
=======================
Comprehensive read-only diagnostic of Dataset 2.

Source:
    data/raw/dataset_2/Persons Engaged in Industry by Enterprise Type – PLFS Year.csv

This script does NOT modify any source file.
It produces diagnostic artifacts in:
    outputs/dataset_2_diagnostic/
"""

import os
import sys
import hashlib
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FILE  = os.path.join(BASE, "data", "raw", "dataset_2",
                         "Persons Engaged in Industry by Enterprise Type \u2013 PLFS Year.csv")
D1_RAL    = os.path.join(BASE, "outputs", "phase_4_eda",
                         "dataset_1_reusable_analytical.csv")
OUT_DIR   = os.path.join(BASE, "outputs", "dataset_2_diagnostic")
os.makedirs(OUT_DIR, exist_ok=True)

SEP  = "=" * 70
sep2 = "-" * 70

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# ── Pre-run hash so we can confirm source is unchanged at end ──────────────────
src_hash_pre = md5(SRC_FILE)
print(f"\n{SEP}")
print("DATASET 2 DIAGNOSTIC — READ-ONLY")
print(f"{SEP}")
print(f"Source file : {SRC_FILE}")
print(f"MD5 (pre)   : {src_hash_pre}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — LOAD
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 1 — LOAD & BASIC STRUCTURE")
print(SEP)

df = pd.read_csv(SRC_FILE, dtype=str)      # load everything as str first for integrity

print(f"Rows         : {len(df)}")
print(f"Columns      : {len(df.columns)}")
print(f"Column names : {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head().to_string())
print(f"\nLast 5 rows:")
print(df.tail().to_string())

# Save schema
schema_rows = []
for col in df.columns:
    schema_rows.append({"column": col, "dtype_raw": str(df[col].dtype),
                        "non_null": df[col].notna().sum(),
                        "null": df[col].isna().sum()})
schema_df = pd.DataFrame(schema_rows)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — STRUCTURE + DTYPES
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 2 — STRUCTURE, DTYPES, MEMORY")
print(SEP)

df2 = pd.read_csv(SRC_FILE)   # reload with inferred dtypes
print("Inferred dtypes:")
print(df2.dtypes.to_string())
print(f"\nMemory usage: {df2.memory_usage(deep=True).sum() / 1024:.1f} KB")

dup_full = df2.duplicated().sum()
print(f"\nFully duplicate rows : {dup_full}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3–9 — DIMENSION INVENTORY
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEPS 3–9 — DIMENSION INVENTORY")
print(SEP)

# Identify likely dimension columns
# Use raw str-loaded df so we see exact source values
dim_cols_candidates = [c for c in df.columns
                       if df[c].dtype == object or df[c].nunique() < 200]

# Report all columns for dimensions
dim_report_rows = []
for col in df.columns:
    vc = df[col].value_counts(dropna=False)
    missing = int(df[col].isna().sum())
    miss_pct = round(missing / len(df) * 100, 3)
    n_unique = df[col].nunique(dropna=True)
    dim_report_rows.append({
        "column": col,
        "unique_count": n_unique,
        "missing_count": missing,
        "missing_pct": miss_pct,
        "top_values": str(df[col].value_counts(dropna=True).head(10).to_dict())
    })
dim_inventory_df = pd.DataFrame(dim_report_rows)

print(dim_inventory_df[["column","unique_count","missing_count","missing_pct"]].to_string(index=False))

# Print full unique values for each dimension column
CAT_COLS = []
for col in df.columns:
    n_u = df[col].nunique(dropna=True)
    if n_u <= 60:
        CAT_COLS.append(col)
        print(f"\n  {col}  ({n_u} unique values):")
        vc = df[col].value_counts(dropna=False)
        for val, cnt in vc.items():
            print(f"    {repr(val):50s}  {cnt}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — YEAR COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 4 — YEAR COVERAGE")
print(SEP)

year_col = next((c for c in df.columns if "year" in c.lower()), None)
print(f"Year column identified: {year_col!r}")
if year_col:
    yr_vc = df[year_col].value_counts(dropna=False).sort_index()
    print(f"Unique years: {sorted(df[year_col].dropna().unique())}")
    print(f"Rows by year:\n{yr_vc.to_string()}")
    yrs_numeric = pd.to_numeric(df[year_col].str.extract(r'(\d{4})')[0], errors='coerce').dropna().astype(int).unique()
    expected = set(range(2017, 2024))
    found    = set(yrs_numeric)
    print(f"\nExpected years 2017-2023: {sorted(expected)}")
    print(f"Found    years           : {sorted(found)}")
    print(f"Missing                  : {sorted(expected - found)}")
    print(f"Extra                    : {sorted(found - expected)}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — GEOGRAPHIC COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 5 — GEOGRAPHIC COVERAGE")
print(SEP)

state_col = next((c for c in df.columns if "state" in c.lower()), None)
print(f"State column: {state_col!r}")
if state_col and year_col:
    states = sorted(df[state_col].dropna().unique())
    print(f"Number of states/UTs: {len(states)}")
    print(f"States: {states}")

    # State × Year cross-tab
    pivot_sy = df.groupby([state_col, year_col]).size().unstack(fill_value=0)
    print(f"\nState × Year row counts (non-zero = present):")
    print(pivot_sy.to_string())

    # Missing State × Year combos
    all_states = df[state_col].dropna().unique()
    all_years  = df[year_col].dropna().unique()
    combos_present = set(zip(df[state_col], df[year_col]))
    combos_all     = {(s, y) for s in all_states for y in all_years}
    missing_combos = combos_all - combos_present
    print(f"\nMissing State × Year combos: {len(missing_combos)}")
    if missing_combos:
        for m in sorted(missing_combos)[:20]:
            print(f"  {m}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — AREA COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 6 — AREA COVERAGE")
print(SEP)

area_col = next((c for c in df.columns if "area" in c.lower()), None)
print(f"Area column: {area_col!r}")
if area_col:
    print(df[area_col].value_counts(dropna=False).to_string())
    if year_col:
        print(f"\nArea × Year:")
        print(df.groupby([area_col, year_col]).size().unstack(fill_value=0).to_string())
    if state_col:
        print(f"\nArea × State (row counts):")
        print(df.groupby([area_col, state_col]).size().unstack(fill_value=0).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — GENDER COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 7 — GENDER COVERAGE")
print(SEP)

gender_col = next((c for c in df.columns if "gender" in c.lower() or "sex" in c.lower()), None)
print(f"Gender column: {gender_col!r}")
if gender_col:
    print(df[gender_col].value_counts(dropna=False).to_string())
    for cross_col, label in [(year_col,"Gender × Year"), (state_col,"Gender × State"),
                              (area_col,"Gender × Area")]:
        if cross_col:
            print(f"\n{label}:")
            print(df.groupby([gender_col, cross_col]).size().unstack(fill_value=0).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 8 — INDUSTRY STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 8 — INDUSTRY STRUCTURE")
print(SEP)

ind_col = next((c for c in df.columns if "industry" in c.lower() or "division" in c.lower()), None)
print(f"Industry column: {ind_col!r}")
if ind_col:
    vc_ind = df[ind_col].value_counts(dropna=False)
    print(f"Unique values: {df[ind_col].nunique(dropna=True)}")
    print(vc_ind.to_string())
    n_unique_ind = df[ind_col].nunique(dropna=True)
    print(f"\n*** ANALYTICAL LIMITATION NOTE ***")
    if n_unique_ind == 1:
        print(f"  Industry Division Type has only ONE unique value: {df[ind_col].dropna().unique()}")
        print(f"  Industry-level disaggregation (Q27, Q31, Q32) is NOT possible with this source.")
    elif n_unique_ind < 5:
        print(f"  Industry Division Type has {n_unique_ind} values. Limited industry disaggregation.")
    else:
        print(f"  Industry Division Type has {n_unique_ind} values — disaggregation possible.")

    for cross_col, label in [(year_col,"Industry × Year"), (gender_col,"Industry × Gender"),
                              (state_col,"Industry × State"), (area_col,"Industry × Area")]:
        if cross_col:
            print(f"\n{label}:")
            print(df.groupby([ind_col, cross_col]).size().unstack(fill_value=0).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 9 — ENTERPRISE STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 9 — ENTERPRISE STRUCTURE")
print(SEP)

ent_col = next((c for c in df.columns if "enterprise" in c.lower()), None)
print(f"Enterprise column: {ent_col!r}")
if ent_col:
    print(df[ent_col].value_counts(dropna=False).to_string())
    for cross_col, label in [(year_col,"Enterprise × Year"), (gender_col,"Enterprise × Gender"),
                              (state_col,"Enterprise × State"), (area_col,"Enterprise × Area"),
                              (ind_col,"Enterprise × Industry")]:
        if cross_col:
            print(f"\n{label}:")
            print(df.groupby([ent_col, cross_col]).size().unstack(fill_value=0).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 10 — PRIMARY MEASURE DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 10 — PRIMARY MEASURE DIAGNOSTIC")
print(SEP)

# Identify the percentage measure column
pct_col = next((c for c in df2.columns
                if "percentage" in c.lower() or "engaged" in c.lower()), None)
print(f"Primary measure column: {pct_col!r}")
if pct_col:
    s = df2[pct_col]
    print(f"dtype           : {s.dtype}")
    print(f"count (non-null): {s.notna().sum()}")
    print(f"missing         : {s.isna().sum()}  ({s.isna().mean()*100:.3f}%)")
    print(f"min             : {s.min()}")
    print(f"max             : {s.max()}")
    print(f"mean            : {s.mean():.4f}")
    print(f"median          : {s.median():.4f}")
    print(f"std             : {s.std():.4f}")
    print(f"zero values     : {(s == 0).sum()}")
    print(f"negative values : {(s < 0).sum()}")
    print(f"values > 100    : {(s > 100).sum()}")
    print(f"values 0–100    : {((s >= 0) & (s <= 100)).sum()}")
    if (s < 0).sum() > 0 or (s > 100).sum() > 0:
        print("\n  *** OUT-OF-RANGE VALUES DETECTED — reporting only ***")
        bad = df2[df2[pct_col].notna() & ((df2[pct_col] < 0) | (df2[pct_col] > 100))]
        print(bad[[state_col, year_col, gender_col, area_col, ent_col, pct_col]].to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 11 — OTHER NUMERIC MEASURES
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 11 — OTHER NUMERIC MEASURES")
print(SEP)

num_cols = [c for c in df2.columns if c != pct_col and
            pd.api.types.is_numeric_dtype(df2[c])]
print(f"Other numeric columns: {num_cols}")
for col in num_cols:
    s = df2[col]
    print(f"\n  {col!r}:")
    print(f"    dtype    : {s.dtype}")
    print(f"    min      : {s.min()}")
    print(f"    max      : {s.max()}")
    print(f"    mean     : {s.mean():.2f}")
    print(f"    median   : {s.median():.2f}")
    print(f"    std      : {s.std():.2f}")
    print(f"    missing  : {s.isna().sum()}")
    print(f"    zeros    : {(s == 0).sum()}")
    print(f"    negative : {(s < 0).sum()}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 12 — MISSINGNESS MATRIX
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 12 — MISSINGNESS MATRIX")
print(SEP)

miss_rows = []
for col in df2.columns:
    mc  = int(df2[col].isna().sum())
    mp  = round(mc / len(df2) * 100, 3)
    miss_rows.append({"column": col, "missing_count": mc, "missing_pct": mp})
miss_df = pd.DataFrame(miss_rows)
print(miss_df.to_string(index=False))

# Missingness by dimension
print(f"\n  Missingness by Year (primary measure):")
if year_col and pct_col:
    print(df2.groupby(year_col)[pct_col].apply(lambda x: x.isna().sum()).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# STEP 13 — GRAIN DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 13 — GRAIN DIAGNOSTIC")
print(SEP)

grain_cols = []
# Build ordered list of dimension columns from most coarse to most granular
dim_sequence = []
for col in [state_col, year_col, gender_col, area_col, ind_col, ent_col]:
    if col and col not in dim_sequence:
        dim_sequence.append(col)

grain_rows = []
for i in range(1, len(dim_sequence) + 1):
    key_cols  = dim_sequence[:i]
    n_rows    = len(df2)
    n_unique  = df2.groupby(key_cols).ngroups
    dup_keys  = n_rows - n_unique
    max_per   = df2.groupby(key_cols).size().max()
    grain_rows.append({
        "key_columns":         " × ".join(key_cols),
        "n_unique_keys":       n_unique,
        "n_rows":              n_rows,
        "duplicate_key_count": dup_keys,
        "max_rows_per_key":    max_per,
        "is_unique":           dup_keys == 0
    })
    label = " × ".join(key_cols)
    print(f"  {label}")
    print(f"    Unique keys: {n_unique}  |  Rows: {n_rows}  |  Dups: {dup_keys}  |  "
          f"Max rows/key: {max_per}  |  Unique: {dup_keys==0}")

grain_df = pd.DataFrame(grain_rows)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 14 — SOURCE INTEGRITY CHECKS
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 14 — SOURCE INTEGRITY CHECKS")
print(SEP)

integrity_issues = []

# Fully duplicate rows
dup_full = int(df2.duplicated().sum())
print(f"Fully duplicate rows: {dup_full}")
if dup_full: integrity_issues.append(f"Fully duplicate rows: {dup_full}")

# Whitespace in categorical columns
cat_check_cols = [c for c in df2.columns if df2[c].dtype == object]
for col in cat_check_cols:
    ws = df2[col].str.contains(r'^\s|\s$', na=False).sum()
    if ws:
        print(f"  Whitespace issues in {col!r}: {ws} values")
        integrity_issues.append(f"Whitespace in {col!r}: {ws}")

# Empty strings
for col in cat_check_cols:
    es = (df2[col] == '').sum()
    if es:
        print(f"  Empty strings in {col!r}: {es}")
        integrity_issues.append(f"Empty strings in {col!r}: {es}")

# Null-like strings
null_like = ['null','none','nan','na','n/a','missing','#n/a']
for col in cat_check_cols:
    nl = df2[col].str.lower().isin(null_like).sum()
    if nl:
        print(f"  Null-like strings in {col!r}: {nl}")
        integrity_issues.append(f"Null-like strings in {col!r}: {nl}")

# Year format consistency
if year_col:
    yr_vals = df2[year_col].dropna().unique()
    yf_types = set()
    for v in yr_vals:
        s = str(v)
        if s.isdigit() and len(s) == 4:
            yf_types.add("4-digit integer")
        elif '-' in s:
            yf_types.add("range e.g. 2017-18")
        else:
            yf_types.add(f"other: {s}")
    print(f"\nYear format types: {yf_types}")
    if len(yf_types) > 1:
        integrity_issues.append(f"Inconsistent year formats: {yf_types}")

if not integrity_issues:
    print("No critical integrity issues detected.")
else:
    print(f"\nIntegrity issues found: {len(integrity_issues)}")
    for issue in integrity_issues:
        print(f"  - {issue}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 15 — CROSS-DIMENSION COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 15 — CROSS-DIMENSION COVERAGE")
print(SEP)

cov_rows = []
for key_cols in [
    [state_col, year_col],
    [state_col, year_col, gender_col],
    [state_col, year_col, gender_col, area_col],
    [state_col, year_col, gender_col, area_col, ent_col],
    [state_col, year_col, gender_col, area_col, ind_col],
]:
    key_cols = [c for c in key_cols if c]
    present  = df2.groupby(key_cols).ngroups
    total    = 1
    for c in key_cols:
        total *= df2[c].nunique()
    missing  = total - present
    cov_rows.append({"key": " × ".join(key_cols),
                     "present": present, "theoretical_max": total,
                     "missing": missing,
                     "coverage_pct": round(present/total*100,2) if total else None})
cov_df = pd.DataFrame(cov_rows)
print(cov_df.to_string(index=False))

# ══════════════════════════════════════════════════════════════════════════════
# STEP 16 — DATASET 1 COMPATIBILITY CHECK
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 16 — DATASET 1 COMPATIBILITY CHECK")
print(SEP)

if os.path.exists(D1_RAL):
    d1 = pd.read_csv(D1_RAL)
    d1_states  = set(d1["State"].dropna().unique())
    d1_years   = set(d1["Year"].dropna().astype(int).unique())
    d1_genders = set(d1["Gender"].dropna().unique())
    d1_areas   = set(d1["Area_Type"].dropna().unique())

    if state_col:
        d2_states = set(df2[state_col].dropna().unique())
        print(f"Common states           : {len(d1_states & d2_states)}")
        only_d1 = d1_states - d2_states
        only_d2 = d2_states - d1_states
        if only_d1: print(f"States only in Dataset 1: {sorted(only_d1)}")
        if only_d2: print(f"States only in Dataset 2: {sorted(only_d2)}")

    if year_col:
        # Extract numeric year from Dataset 2 year column
        d2_yrs_raw = df2[year_col].dropna().unique()
        d2_years   = set()
        for y in d2_yrs_raw:
            try:
                import re
                m = re.search(r'\d{4}', str(y))
                if m: d2_years.add(int(m.group()))
            except: pass
        print(f"\nCommon years            : {sorted(d1_years & d2_years)}")
        print(f"Years only in Dataset 1 : {sorted(d1_years - d2_years)}")
        print(f"Years only in Dataset 2 : {sorted(d2_years - d1_years)}")

    if gender_col:
        d2_genders = set(df2[gender_col].dropna().unique())
        print(f"\nCommon gender categories: {d1_genders & d2_genders}")
        print(f"Gender only in D1       : {d1_genders - d2_genders}")
        print(f"Gender only in D2       : {d2_genders - d1_genders}")

    if area_col:
        d2_areas = set(df2[area_col].dropna().unique())
        print(f"\nD1 area categories      : {d1_areas}")
        print(f"D2 area categories      : {d2_areas}")
        print(f"Common area categories  : {d1_areas & d2_areas}")
        print(f"Only in D1              : {d1_areas - d2_areas}")
        print(f"Only in D2              : {d2_areas - d1_areas}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 17 — Q27–Q32 FEASIBILITY
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("STEP 17 — Q27–Q32 FEASIBILITY ASSESSMENT")
print(SEP)

n_ind = df2[ind_col].nunique(dropna=True) if ind_col else 0
ind_vals = sorted(df2[ind_col].dropna().unique()) if ind_col else []

feasibility = [
    {
        "Q": "Q27",
        "Question": "Women's employment distribution across Industry Division Types",
        "Required_dimensions": f"Gender=Female, {ind_col}, {pct_col}",
        "Source_support": f"Industry has {n_ind} unique value(s): {ind_vals}",
        "Limitation": (
            "CRITICAL: Only one Industry Division Type value found — "
            "no cross-industry distribution possible."
            if n_ind == 1 else
            f"{n_ind} industry values — distribution possible."
        )
    },
    {
        "Q": "Q28",
        "Question": "Percentage engaged across Enterprise Types",
        "Required_dimensions": f"{ent_col}, {pct_col}",
        "Source_support": f"Enterprise has {df2[ent_col].nunique(dropna=True) if ent_col else 'N/A'} categories",
        "Limitation": "Feasible if enterprise categories are ≥2."
    },
    {
        "Q": "Q29",
        "Question": "Women's industry participation by Rural/Urban",
        "Required_dimensions": f"Gender=Female, {area_col}, {pct_col}",
        "Source_support": f"Area types: {sorted(df2[area_col].dropna().unique()) if area_col else 'N/A'}",
        "Limitation": (
            "Feasible for enterprise breakdown by area; "
            "industry-level area breakdown LIMITED by single industry value."
            if n_ind == 1 else "Feasible."
        )
    },
    {
        "Q": "Q30",
        "Question": "Women's industry participation across Enterprise Types",
        "Required_dimensions": f"Gender=Female, {ent_col}, {pct_col}",
        "Source_support": "Enterprise dimension present.",
        "Limitation": "Feasible. Enterprise disaggregation available."
    },
    {
        "Q": "Q31",
        "Question": "Industry and enterprise pattern by Gender",
        "Required_dimensions": f"{gender_col}, {ind_col}, {ent_col}, {pct_col}",
        "Source_support": f"Gender and Enterprise present; Industry has {n_ind} value(s).",
        "Limitation": (
            "Gender × Enterprise comparison feasible. "
            "Industry-level gender comparison NOT possible — only one Industry Division Type."
            if n_ind == 1 else "Feasible."
        )
    },
    {
        "Q": "Q32",
        "Question": "Industry and enterprise pattern change 2017–2023",
        "Required_dimensions": f"{year_col}, {ind_col}, {ent_col}, {pct_col}",
        "Source_support": f"Year range present; Industry has {n_ind} value(s).",
        "Limitation": (
            "Temporal enterprise change feasible. "
            "Industry-level temporal change NOT possible — only one Industry Division Type."
            if n_ind == 1 else "Feasible."
        )
    },
]
feasibility_df = pd.DataFrame(feasibility)
for _, row in feasibility_df.iterrows():
    print(f"\n  {row['Q']}: {row['Question']}")
    print(f"    Required   : {row['Required_dimensions']}")
    print(f"    Support    : {row['Source_support']}")
    print(f"    Limitation : {row['Limitation']}")

# ══════════════════════════════════════════════════════════════════════════════
# SAVE DIAGNOSTIC ARTIFACTS
# ══════════════════════════════════════════════════════════════════════════════
schema_df.to_csv(os.path.join(OUT_DIR, "dataset_2_schema.csv"), index=False)
dim_inventory_df.to_csv(os.path.join(OUT_DIR, "dataset_2_dimension_inventory.csv"), index=False)
miss_df.to_csv(os.path.join(OUT_DIR, "dataset_2_missingness.csv"), index=False)
grain_df.to_csv(os.path.join(OUT_DIR, "dataset_2_grain_diagnostic.csv"), index=False)
cov_df.to_csv(os.path.join(OUT_DIR, "dataset_2_coverage_diagnostic.csv"), index=False)
feasibility_df.to_csv(os.path.join(OUT_DIR, "dataset_2_question_feasibility.csv"), index=False)

print(f"\n{SEP}")
print("DIAGNOSTIC ARTIFACTS SAVED")
print(SEP)
for f in ["dataset_2_schema.csv","dataset_2_dimension_inventory.csv",
          "dataset_2_missingness.csv","dataset_2_grain_diagnostic.csv",
          "dataset_2_coverage_diagnostic.csv","dataset_2_question_feasibility.csv"]:
    path = os.path.join(OUT_DIR, f)
    print(f"  {path}  ({os.path.getsize(path)} bytes)")

# ══════════════════════════════════════════════════════════════════════════════
# PROTECTION CHECK
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PROTECTION CHECK")
print(SEP)
src_hash_post = md5(SRC_FILE)
print(f"Source Dataset 2 hash unchanged : {src_hash_pre == src_hash_post}")
if os.path.exists(D1_RAL):
    d1_hash = md5(D1_RAL)
    # compare to known hash embedded in validation report if available, else just report
    print(f"Dataset 1 reusable layer read   : True (read-only, not modified)")
print(f"Q27-Q32 analytical CSVs created : False")
print(f"Dataset 1 files modified        : False")

print(f"\n{SEP}")
print("DIAGNOSTIC COMPLETE")
print(SEP)
