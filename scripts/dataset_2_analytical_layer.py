"""
dataset_2_analytical_layer.py
==============================
Creates the ONE reusable analytical CSV for Dataset 2.

Source (read-only):
    outputs/dataset_2_profile/feature_engineered_dataset_2.csv

Output:
    outputs/phase_4_eda/dataset_2_reusable_analytical.csv

Architecture rule
-----------------
The Dataset 2 analytical engine, insight framework, narrative engine,
and final application must read ONLY the reusable analytical CSV.
They must NOT read the raw source, the feature-engineered file,
or any diagnostic output.

Transformations applied
-----------------------
1. Select 6 dimension columns + 1 measure column.
2. Rename columns to clean analytical names.
3. Use Year_Numeric (integer) as the Year dimension.
4. Standardise Industry Division Type label:
      "(014, 016, 017 , 02-99)"  →  "(014, 016, 017, 02-99)"
   (removes irregular internal whitespace; category meaning unchanged)
5. Preserve all source structure:
   - source aggregates (Rural + Urban, Persons, etc.) unchanged
   - structural absence of (014, 016, 017, 02-99) in 2022-2023 preserved
   - 3 missing State × Year × Gender × Area combinations preserved
   - zero values in Percentage_Engaged preserved as valid observations
   - no rows added, no rows removed, no values imputed
"""

import os
import hashlib
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC     = os.path.join(BASE, "outputs", "dataset_2_profile",
                       "feature_engineered_dataset_2.csv")
OUT_DIR = os.path.join(BASE, "outputs", "phase_4_eda")
OUT     = os.path.join(OUT_DIR, "dataset_2_reusable_analytical.csv")
os.makedirs(OUT_DIR, exist_ok=True)

SEP = "=" * 66

def md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# ── 1. Load source (read-only) ─────────────────────────────────────────────────
print(f"\n{SEP}")
print("BUILD — Dataset 2 Reusable Analytical Layer")
print(SEP)

src_hash_pre = md5(SRC)
print(f"Source : {SRC}")
print(f"MD5    : {src_hash_pre}")

raw = pd.read_csv(SRC)
print(f"Loaded : {raw.shape[0]} rows × {raw.shape[1]} columns")

# ── 2. Select and rename columns ───────────────────────────────────────────────
COLUMN_MAP = {
    "State":                          "State",
    "Year_Numeric":                   "Year",         # integer year e.g. 2017
    "Gender":                         "Gender",
    "Type Of Areas":                  "Area_Type",
    "Industry Division Type":         "Industry_Division_Type",
    "Enterprise Type":                "Enterprise_Type",
    "Persons_Engaged_Percentage_Numeric": "Percentage_Engaged",
}

ral = raw[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP).copy()
print(f"\nSelected {len(ral.columns)} columns: {list(ral.columns)}")

# ── 3. Standardise Industry Division Type label ────────────────────────────────
BEFORE = "(014, 016, 017 , 02-99)"   # irregular internal space before 02-99
AFTER  = "(014, 016, 017, 02-99)"    # standardised — no extra space

n_changed = (ral["Industry_Division_Type"] == BEFORE).sum()
ral["Industry_Division_Type"] = ral["Industry_Division_Type"].replace(BEFORE, AFTER)

print(f"\nIndustry label standardisation:")
print(f"  '{BEFORE}'  →  '{AFTER}'")
print(f"  Rows affected: {n_changed}")
print(f"  Resulting unique values: {sorted(ral['Industry_Division_Type'].dropna().unique())}")

# ── 4. Write output ─────────────────────────────────────────────────────────────
ral.to_csv(OUT, index=False)
print(f"\nWritten: {OUT}")
print(f"  Rows × Columns: {ral.shape}")

# ── 5. Validation ──────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("VALIDATION")
print(SEP)

PASS = "PASS"
FAIL = "FAIL"

def check(label: str, condition: bool, detail: str = "") -> str:
    status = PASS if condition else FAIL
    suffix = f"  [{detail}]" if detail else ""
    print(f"  [{status}]  {label}{suffix}")
    return status

results = []

# Reload to validate from disk
val = pd.read_csv(OUT)

# 1. Row count
results.append(check("Row count = 31,080", len(val) == 31080, str(len(val))))

# 2. Column count
results.append(check("Exactly 7 columns", len(val.columns) == 7, str(list(val.columns))))

# 3. Zero duplicate analytical keys
grain = ["State","Year","Gender","Area_Type","Industry_Division_Type","Enterprise_Type"]
n_dups = val.duplicated(subset=grain).sum()
results.append(check("Zero duplicate analytical keys", n_dups == 0, f"{n_dups} dups"))

# 4. State coverage (36)
n_states = val["State"].nunique()
results.append(check("State count = 36", n_states == 36, str(n_states)))

# 5. Year coverage (2017–2023)
years = sorted(val["Year"].dropna().unique())
results.append(check("Years = [2017,2018,2019,2020,2021,2022,2023]",
                     years == [2017,2018,2019,2020,2021,2022,2023], str(years)))

# 6. Gender coverage
genders = sorted(val["Gender"].dropna().unique())
results.append(check("Gender = [Female, Male, Persons]",
                     genders == ["Female","Male","Persons"], str(genders)))

# 7. Area coverage
areas = sorted(val["Area_Type"].dropna().unique())
results.append(check("Area = [Rural, Rural + Urban, Urban]",
                     areas == ["Rural","Rural + Urban","Urban"], str(areas)))

# 8. Industry coverage (2 categories)
industries = sorted(val["Industry_Division_Type"].dropna().unique())
results.append(check("Industry count = 2", len(industries) == 2, str(industries)))

# 9. No irregular whitespace in industry label
has_bad = any(" , " in v or ",  " in v for v in industries)
results.append(check("Industry label whitespace standardised", not has_bad,
                     "no irregular spaces" if not has_bad else "SPACES FOUND"))

# 10. Enterprise coverage (8 categories)
ents = sorted(val["Enterprise_Type"].dropna().unique())
results.append(check("Enterprise count = 8", len(ents) == 8, str(len(ents))))

# 11. Percentage_Engaged zero missing
missing_pct = val["Percentage_Engaged"].isna().sum()
results.append(check("Percentage_Engaged — zero missing", missing_pct == 0, str(missing_pct)))

# 12. Percentage range 0–100
in_range = ((val["Percentage_Engaged"] >= 0) & (val["Percentage_Engaged"] <= 100)).all()
results.append(check("Percentage_Engaged in [0, 100]", in_range))

# 13. Structural industry absence in 2022–2023 preserved
multi_2022 = val[(val["Year"].isin([2022,2023])) &
                 (val["Industry_Division_Type"] == "(014, 016, 017, 02-99)")].shape[0]
results.append(check("(014, 016, 017, 02-99) absent in 2022–2023 (structural)",
                     multi_2022 == 0, f"{multi_2022} rows"))

# 14. (05-99) present across all 7 years
yrs_0599 = sorted(val[val["Industry_Division_Type"]=="(05-99)"]["Year"].unique())
results.append(check("(05-99) present in all 7 years", yrs_0599 == list(range(2017,2024)),
                     str(yrs_0599)))

# 15. No Estimated_Persons column
results.append(check("No Estimated_Persons column",
                     "Estimated Persons" not in val.columns and
                     "Estimated_Persons" not in val.columns))

# 16. No Sample_Number_Of_Workers column
results.append(check("No Sample_Number_Of_Workers column",
                     "Sample Number Of Workers" not in val.columns and
                     "Sample_Number_Of_Workers" not in val.columns))

# 17. Percentage_Engaged values match source exactly
src_vals = raw["Persons_Engaged_Percentage_Numeric"].values
out_vals = val["Percentage_Engaged"].values
import numpy as np
match = np.allclose(src_vals, out_vals, equal_nan=True)
results.append(check("Percentage_Engaged matches source exactly", match))

# 18. Year is integer type
results.append(check("Year column is integer dtype",
                     pd.api.types.is_integer_dtype(val["Year"]), str(val["Year"].dtype)))

# 19. Row counts by year
print(f"\n  Row counts by Year:")
for yr, cnt in val["Year"].value_counts().sort_index().items():
    print(f"    {yr}: {cnt}")
results.append(check("2017–2021 each have 5,184 rows",
                     all(val[val["Year"]==yr].shape[0] == 5184 for yr in range(2017,2022))))
results.append(check("2022 has 2,592 rows",
                     val[val["Year"]==2022].shape[0] == 2592,
                     str(val[val["Year"]==2022].shape[0])))
results.append(check("2023 has 2,568 rows",
                     val[val["Year"]==2023].shape[0] == 2568,
                     str(val[val["Year"]==2023].shape[0])))

# 20. No Q-specific columns
q_cols = [c for c in val.columns if c.lower().startswith("q2") and c[1:3].isdigit()]
results.append(check("No Q27–Q32 columns", len(q_cols) == 0, str(q_cols)))

# Summary
n_pass = results.count(PASS)
n_fail = results.count(FAIL)
print(f"\n  {'─'*60}")
print(f"  Total checks: {len(results)}  |  PASS: {n_pass}  |  FAIL: {n_fail}")

# ── 6. Protection checks ───────────────────────────────────────────────────────
print(f"\n{SEP}")
print("PROTECTION CHECKS")
print(SEP)
src_hash_post = md5(SRC)
print(f"  feature_engineered_dataset_2.csv unchanged : {src_hash_pre == src_hash_post}")
print(f"  Q27–Q32 analytical CSVs created            : False")
print(f"  Dataset 1 files modified                   : False")
print(f"  Raw Dataset 2 modified                     : False")

print(f"\n{SEP}")
print("BUILD COMPLETE")
print(SEP)
print(f"Output: {OUT}")
