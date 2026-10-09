"""
Build Dataset 1 Reusable Analytical Layer
==========================================
Reads feature_engineered_dataset_1.csv and produces:
  outputs/phase_4_eda/dataset_1_reusable_analytical.csv

Rules:
- No modification to source dataset.
- No fabrication of missing dimensional combinations.
- No imputation of missing indicator values.
- No aggregation at this stage; one row per five-dimensional key.
"""

import os
import pandas as pd

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv")
OUT_DIR  = os.path.join(BASE_DIR, "outputs", "phase_4_eda")
OUT_PATH = os.path.join(OUT_DIR, "dataset_1_reusable_analytical.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Exact source column names (from dimensional audit)
# ------------------------------------------------------------------
COL_STATE  = "State"
COL_YEAR   = "Year"          # raw string, e.g. "2017-18"
COL_GENDER = "Gender"
COL_AREA   = "Type Of Areas"
COL_EDU    = "Education Level"
COL_LFPR   = ("Labor Force Participation Rate According To Usual Status Based "
               "On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1")
COL_WPR    = ("Working Population Rate According To Usual Status Based "
               "On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1")
COL_UNEMP  = ("Unemployment Rate According To Usual Status Based "
               "On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1")

# ------------------------------------------------------------------
# 1. Read source dataset (read-only; no modification)
# ------------------------------------------------------------------
print("Reading source dataset …")
df = pd.read_csv(SRC_PATH)
src_rows, src_cols = df.shape
print(f"  Source: {src_rows} rows × {src_cols} columns")

# ------------------------------------------------------------------
# 2. Derive numeric year (same approach as existing scripts)
# ------------------------------------------------------------------
df["YearNum"] = df[COL_YEAR].str.extract(r"(\d{4})").astype(int)

# ------------------------------------------------------------------
# 3. Select and rename columns for the analytical layer
# ------------------------------------------------------------------
analytical = df[[COL_STATE, "YearNum", COL_GENDER, COL_AREA, COL_EDU,
                 COL_LFPR, COL_WPR, COL_UNEMP]].copy()

analytical.columns = [
    "State", "Year", "Gender", "Area_Type", "Education",
    "LFPR", "WPR", "Unemployment_Rate"
]

# ------------------------------------------------------------------
# 4. Confirm uniqueness at five-dimensional grain
# ------------------------------------------------------------------
KEY_COLS = ["State", "Year", "Gender", "Area_Type", "Education"]
n_total  = len(analytical)
n_unique = analytical.drop_duplicates(subset=KEY_COLS).shape[0]
assert n_total == n_unique, (
    f"FATAL: Duplicate five-dimensional keys detected "
    f"({n_total - n_unique} duplicates). Aborting."
)
print(f"  Five-dimensional uniqueness confirmed: {n_total} rows, 0 duplicates.")

# ------------------------------------------------------------------
# 5. Write output (NaN preserved as empty in CSV)
# ------------------------------------------------------------------
analytical.to_csv(OUT_PATH, index=False, na_rep="")
print(f"  Written to: {OUT_PATH}")
print("Done.")
