"""
Q18-Q26 Implementation – Dataset 1 Reusable Analytical Layer
=============================================================

Source (read-only):
    outputs/phase_4_eda/dataset_1_reusable_analytical.csv

Outputs:
    outputs/phase_4_eda/q18_gender_education_lfpr.csv
    outputs/phase_4_eda/q19_gender_education_wpr.csv
    outputs/phase_4_eda/q20_gender_education_unemployment.csv
    outputs/phase_4_eda/q21_gender_area_labour_market.csv
    outputs/phase_4_eda/q22_women_lfpr_trend.csv
    outputs/phase_4_eda/q23_women_wpr_trend.csv
    outputs/phase_4_eda/q24_women_unemployment_trend.csv
    outputs/phase_4_eda/q25_women_education_change.csv
    outputs/phase_4_eda/q26_women_rural_urban_trends.csv
    outputs/phase_4_eda/q18_q26_methodological_specification.md

Protection:
    No Q1-Q17 files touched.
    Source Dataset 1 not modified.
    Reusable analytical layer not modified.
"""

import os
import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE, "outputs", "phase_4_eda", "dataset_1_reusable_analytical.csv")
OUT_DIR  = os.path.join(BASE, "outputs", "phase_4_eda")

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
DETAILED_EDU = [
    "Not Literate",
    "Literate & Upto Primary",
    "Middle",
    "Secondary",
    "Higher Secondary",
    "Diploma/ Certificate Course",
    "Graduate",
    "Post Graduate & Above",
]

# ------------------------------------------------------------------
# Load reusable layer (read-only)
# ------------------------------------------------------------------
print("Loading reusable analytical layer …")
df = pd.read_csv(SRC_PATH)
print(f"  Loaded: {len(df)} rows × {len(df.columns)} columns")

# ------------------------------------------------------------------
# Reusable utility functions
# ------------------------------------------------------------------

def filter_df(base, gender=None, area=None, education=None, year=None):
    """Apply dimension filters to the reusable layer."""
    out = base.copy()
    if gender    is not None: out = out[out["Gender"].isin(gender)]
    if area      is not None: out = out[out["Area_Type"].isin(area)]
    if education is not None: out = out[out["Education"].isin(education)]
    if year      is not None: out = out[out["Year"].isin(year)]
    return out


def aggregate(base, group_cols, indicators):
    """
    Unweighted arithmetic mean across group_cols for each indicator.
    NaN values are excluded from the mean.
    If all values in a group are NaN the result is NaN (not 0).
    """
    agg_dict = {ind: "mean" for ind in indicators if ind in base.columns}
    result = base.groupby(group_cols, as_index=False, dropna=False).agg(agg_dict)
    return result


def add_fm_gap(df_wide, indicator):
    """
    Add Female-Male Gap = Female_value - Male_value for an indicator.
    Requires columns f'{indicator}_Female' and f'{indicator}_Male'.
    """
    f_col = f"{indicator}_Female"
    m_col = f"{indicator}_Male"
    if f_col in df_wide.columns and m_col in df_wide.columns:
        df_wide[f"{indicator}_FM_Gap"] = df_wide[f_col] - df_wide[m_col]
    return df_wide


def pivot_gender(df_long, key_cols, indicator):
    """
    Pivot Gender into wide format for one indicator:
        key_cols + [f'{indicator}_Female', f'{indicator}_Male', f'{indicator}_FM_Gap']
    """
    pivoted = df_long.pivot_table(
        index=key_cols, columns="Gender", values=indicator, aggfunc="first"
    ).reset_index()
    pivoted.columns.name = None
    for g in ["Female", "Male"]:
        if g in pivoted.columns:
            pivoted.rename(columns={g: f"{indicator}_{g}"}, inplace=True)
    pivoted = add_fm_gap(pivoted, indicator)
    return pivoted


def compute_change(df, value_col, year_col="Year", key_cols=None):
    """
    Compute Absolute_Change and Percentage_Change from 2017 to 2023.
    Returns a DataFrame with one row per key_cols combination.
    """
    if key_cols is None:
        key_cols = [c for c in df.columns if c not in [value_col, year_col, "Year"]]
    y2017 = df[df[year_col] == 2017].set_index(key_cols)[value_col].rename("Value_2017")
    y2023 = df[df[year_col] == 2023].set_index(key_cols)[value_col].rename("Value_2023")
    combined = pd.concat([y2017, y2023], axis=1).reset_index()
    combined["Absolute_Change"] = combined["Value_2023"] - combined["Value_2017"]
    combined["Percentage_Change"] = np.where(
        (combined["Value_2017"].notna()) & (combined["Value_2017"] != 0),
        (combined["Absolute_Change"] / combined["Value_2017"]) * 100,
        np.nan,
    )
    return combined


def round_cols(df, decimals=3):
    """Round all float columns to 3 decimal places."""
    for c in df.select_dtypes(include="float").columns:
        df[c] = df[c].round(decimals)
    return df


def save(df, path, label):
    df = round_cols(df.copy())
    df.to_csv(path, index=False, na_rep="")
    print(f"  [{label}] Written: {os.path.basename(path)}  ({len(df)} rows × {len(df.columns)} cols)")


# ==================================================================
# Q18 – Female vs Male LFPR across education levels
# ==================================================================
# Methodology:
#   Indicator : LFPR
#   Gender    : Female, Male  (filter)
#   Education : 8 detailed categories (filter; exclude All, Secondary & Above)
#   Area_Type : Filter to 'Rural + Urban'  — existing source aggregate; avoids
#               constructing an artificial across-area mean
#   State     : Collapse — aggregate with unweighted mean across all 36 states
#   Year      : Retain — preserves the full 2017-2023 time dimension
#   Output grain: Year × Education × Gender (wide: LFPR_Female, LFPR_Male, LFPR_FM_Gap)
# ==================================================================
print("\nQ18 …")
q18_base = filter_df(df,
                     gender=["Female", "Male"],
                     area=["Rural + Urban"],
                     education=DETAILED_EDU)
q18_agg  = aggregate(q18_base, group_cols=["Year", "Education", "Gender"],
                     indicators=["LFPR"])
q18_wide = pivot_gender(q18_agg, key_cols=["Year", "Education"], indicator="LFPR")
# Enforce education ordering
q18_wide["Edu_Order"] = q18_wide["Education"].map({e: i for i, e in enumerate(DETAILED_EDU)})
q18_wide = q18_wide.sort_values(["Year", "Edu_Order"]).drop(columns=["Edu_Order"])
save(q18_wide, os.path.join(OUT_DIR, "q18_gender_education_lfpr.csv"), "Q18")


# ==================================================================
# Q19 – Female vs Male WPR across education levels
# ==================================================================
# Methodology: identical to Q18, indicator = WPR
# ==================================================================
print("Q19 …")
q19_base = filter_df(df,
                     gender=["Female", "Male"],
                     area=["Rural + Urban"],
                     education=DETAILED_EDU)
q19_agg  = aggregate(q19_base, group_cols=["Year", "Education", "Gender"],
                     indicators=["WPR"])
q19_wide = pivot_gender(q19_agg, key_cols=["Year", "Education"], indicator="WPR")
q19_wide["Edu_Order"] = q19_wide["Education"].map({e: i for i, e in enumerate(DETAILED_EDU)})
q19_wide = q19_wide.sort_values(["Year", "Edu_Order"]).drop(columns=["Edu_Order"])
save(q19_wide, os.path.join(OUT_DIR, "q19_gender_education_wpr.csv"), "Q19")


# ==================================================================
# Q20 – Female vs Male Unemployment across education levels
# ==================================================================
# Methodology: identical to Q18, indicator = Unemployment_Rate
# ==================================================================
print("Q20 …")
q20_base = filter_df(df,
                     gender=["Female", "Male"],
                     area=["Rural + Urban"],
                     education=DETAILED_EDU)
q20_agg  = aggregate(q20_base, group_cols=["Year", "Education", "Gender"],
                     indicators=["Unemployment_Rate"])
q20_wide = pivot_gender(q20_agg, key_cols=["Year", "Education"], indicator="Unemployment_Rate")
q20_wide["Edu_Order"] = q20_wide["Education"].map({e: i for i, e in enumerate(DETAILED_EDU)})
q20_wide = q20_wide.sort_values(["Year", "Edu_Order"]).drop(columns=["Edu_Order"])
save(q20_wide, os.path.join(OUT_DIR, "q20_gender_education_unemployment.csv"), "Q20")


# ==================================================================
# Q21 – Gender differences by Rural and Urban areas
# ==================================================================
# Methodology:
#   Indicators: LFPR, WPR, Unemployment_Rate
#   Gender    : Female, Male (filter; exclude Persons)
#   Area_Type : Rural, Urban (filter; exclude Rural + Urban — this is the comparison)
#   Education : Filter to 'All' — existing source aggregate; avoids collapsing 10 edu rows
#   State     : Collapse — unweighted mean across 36 states
#   Year      : Retain — preserves time dimension; gender×area gap evolves over years
#   Output grain: Year × Area_Type × Gender (wide: LFPR_Female/Male/Gap, WPR_..., UR_...)
# ==================================================================
print("Q21 …")
q21_base = filter_df(df,
                     gender=["Female", "Male"],
                     area=["Rural", "Urban"],
                     education=["All"])
q21_agg  = aggregate(q21_base,
                     group_cols=["Year", "Area_Type", "Gender"],
                     indicators=["LFPR", "WPR", "Unemployment_Rate"])

# Pivot each indicator separately then merge
q21_l = pivot_gender(q21_agg, key_cols=["Year", "Area_Type"], indicator="LFPR")
q21_w = pivot_gender(q21_agg, key_cols=["Year", "Area_Type"], indicator="WPR")
q21_u = pivot_gender(q21_agg, key_cols=["Year", "Area_Type"], indicator="Unemployment_Rate")
q21_out = q21_l.merge(q21_w, on=["Year", "Area_Type"]).merge(q21_u, on=["Year", "Area_Type"])
q21_out = q21_out.sort_values(["Year", "Area_Type"])
save(q21_out, os.path.join(OUT_DIR, "q21_gender_area_labour_market.csv"), "Q21")


# ==================================================================
# Q22 – Women's LFPR trend 2017-2023
# ==================================================================
# Methodology:
#   Indicator : LFPR
#   Gender    : Female (filter)
#   Area_Type : Filter to 'Rural + Urban' — existing source aggregate
#   Education : Filter to 'All'           — existing source aggregate
#   State     : Collapse — unweighted mean across 36 states
#   Year      : Retain (primary dimension)
#   Output grain: Year  (one row per year, plus a summary change row)
# ==================================================================
print("Q22 …")
q22_base = filter_df(df,
                     gender=["Female"],
                     area=["Rural + Urban"],
                     education=["All"])
q22_agg  = aggregate(q22_base, group_cols=["Year"], indicators=["LFPR"])
q22_agg  = q22_agg.sort_values("Year")
q22_out  = q22_agg.copy()
base_2017_lfpr = float(q22_agg[q22_agg["Year"]==2017]["LFPR"])
q22_out["Absolute_Change_vs_2017"] = q22_out["LFPR"] - base_2017_lfpr
q22_out["Percentage_Change_vs_2017"] = np.where(
    base_2017_lfpr != 0, (q22_out["Absolute_Change_vs_2017"] / base_2017_lfpr) * 100, np.nan
)
save(q22_out, os.path.join(OUT_DIR, "q22_women_lfpr_trend.csv"), "Q22")



# ==================================================================
# Q23 – Women's WPR trend 2017-2023
# ==================================================================
# Same methodology as Q22, indicator = WPR
# ==================================================================
print("Q23 …")
q23_base = filter_df(df, gender=["Female"], area=["Rural + Urban"], education=["All"])
q23_agg  = aggregate(q23_base, group_cols=["Year"], indicators=["WPR"]).sort_values("Year")
q23_out  = q23_agg.copy()
base_2017_wpr = float(q23_agg[q23_agg["Year"]==2017]["WPR"])
q23_out["Absolute_Change_vs_2017"] = q23_out["WPR"] - base_2017_wpr
q23_out["Percentage_Change_vs_2017"] = np.where(
    base_2017_wpr != 0, (q23_out["Absolute_Change_vs_2017"] / base_2017_wpr) * 100, np.nan
)
save(q23_out, os.path.join(OUT_DIR, "q23_women_wpr_trend.csv"), "Q23")


# ==================================================================
# Q24 – Women's Unemployment trend 2017-2023
# ==================================================================
# Same methodology as Q22, indicator = Unemployment_Rate
# ==================================================================
print("Q24 …")
q24_base = filter_df(df, gender=["Female"], area=["Rural + Urban"], education=["All"])
q24_agg  = aggregate(q24_base, group_cols=["Year"], indicators=["Unemployment_Rate"]).sort_values("Year")
q24_out  = q24_agg.copy()
base_2017_ur = float(q24_agg[q24_agg["Year"]==2017]["Unemployment_Rate"])
q24_out["Absolute_Change_vs_2017"] = q24_out["Unemployment_Rate"] - base_2017_ur
q24_out["Percentage_Change_vs_2017"] = np.where(
    base_2017_ur != 0, (q24_out["Absolute_Change_vs_2017"] / base_2017_ur) * 100, np.nan
)
save(q24_out, os.path.join(OUT_DIR, "q24_women_unemployment_trend.csv"), "Q24")


# ==================================================================
# Q25 – Education groups showing noticeable changes (2017 vs 2023)
# ==================================================================
# Methodology:
#   Indicators: LFPR, WPR, Unemployment_Rate
#   Gender    : Female (filter)
#   Education : 8 detailed categories (filter; exclude All, Secondary & Above)
#   Area_Type : Filter to 'Rural + Urban' — existing source aggregate
#   State     : Collapse — unweighted mean across 36 states
#   Year      : Filter to 2017 and 2023 only (endpoint comparison)
#   Output grain: Education × Indicator, with Value_2017, Value_2023,
#                 Absolute_Change, Percentage_Change
# ==================================================================
print("Q25 …")
q25_base = filter_df(df,
                     gender=["Female"],
                     area=["Rural + Urban"],
                     education=DETAILED_EDU,
                     year=[2017, 2023])
q25_agg  = aggregate(q25_base,
                     group_cols=["Education", "Year"],
                     indicators=["LFPR", "WPR", "Unemployment_Rate"])

rows = []
for edu in DETAILED_EDU:
    sub = q25_agg[q25_agg["Education"] == edu]
    v2017 = sub[sub["Year"] == 2017].squeeze()
    v2023 = sub[sub["Year"] == 2023].squeeze()
    for ind in ["LFPR", "WPR", "Unemployment_Rate"]:
        val17 = v2017[ind] if not v2017.empty else np.nan
        val23 = v2023[ind] if not v2023.empty else np.nan
        abs_chg = (val23 - val17) if pd.notna(val17) and pd.notna(val23) else np.nan
        pct_chg = ((abs_chg / val17) * 100
                   if pd.notna(abs_chg) and pd.notna(val17) and val17 != 0
                   else np.nan)
        rows.append({
            "Education": edu,
            "Indicator": ind,
            "Value_2017": val17,
            "Value_2023": val23,
            "Absolute_Change": abs_chg,
            "Percentage_Change": pct_chg,
        })

q25_out = pd.DataFrame(rows)
q25_out["Edu_Order"] = q25_out["Education"].map({e: i for i, e in enumerate(DETAILED_EDU)})
q25_out = q25_out.sort_values(["Edu_Order", "Indicator"]).drop(columns=["Edu_Order"])
save(q25_out, os.path.join(OUT_DIR, "q25_women_education_change.csv"), "Q25")


# ==================================================================
# Q26 – Rural vs Urban temporal patterns among women
# ==================================================================
# Methodology:
#   Indicators: LFPR, WPR, Unemployment_Rate
#   Gender    : Female (filter)
#   Area_Type : Rural, Urban (filter; exclude Rural + Urban — this IS the comparison)
#   Education : Filter to 'All' — existing source aggregate
#   State     : Collapse — unweighted mean across 36 states
#   Year      : Retain (primary time dimension)
#   Output grain: Year × Area_Type (wide: LFPR, WPR, UR per area + Rural-Urban gap)
# ==================================================================
print("Q26 …")
q26_base = filter_df(df,
                     gender=["Female"],
                     area=["Rural", "Urban"],
                     education=["All"])
q26_agg  = aggregate(q26_base,
                     group_cols=["Year", "Area_Type"],
                     indicators=["LFPR", "WPR", "Unemployment_Rate"])
q26_agg  = q26_agg.sort_values(["Year", "Area_Type"])

# Pivot to wide format: Year | LFPR_Rural | LFPR_Urban | LFPR_RU_Gap | ...
q26_out_rows = []
for yr in sorted(q26_agg["Year"].unique()):
    sub = q26_agg[q26_agg["Year"] == yr]
    row = {"Year": yr}
    for ind in ["LFPR", "WPR", "Unemployment_Rate"]:
        r_val = sub[sub["Area_Type"] == "Rural"][ind].values
        u_val = sub[sub["Area_Type"] == "Urban"][ind].values
        row[f"{ind}_Rural"]  = r_val[0] if len(r_val) else np.nan
        row[f"{ind}_Urban"]  = u_val[0] if len(u_val) else np.nan
        row[f"{ind}_RU_Gap"] = (row[f"{ind}_Rural"] - row[f"{ind}_Urban"]
                                if pd.notna(row[f"{ind}_Rural"]) and pd.notna(row[f"{ind}_Urban"])
                                else np.nan)
    q26_out_rows.append(row)

q26_out = pd.DataFrame(q26_out_rows)

# Add 2017-2023 change columns
for ind in ["LFPR", "WPR", "Unemployment_Rate"]:
    for area in ["Rural", "Urban"]:
        col = f"{ind}_{area}"
        v17 = float(q26_out[q26_out["Year"] == 2017][col])
        q26_out[f"{col}_AbsChg"] = q26_out[col] - v17
        q26_out[f"{col}_PctChg"] = np.where(
            v17 != 0, (q26_out[f"{col}_AbsChg"] / v17) * 100, np.nan
        )

save(q26_out, os.path.join(OUT_DIR, "q26_women_rural_urban_trends.csv"), "Q26")

print("\nAll Q18-Q26 outputs written successfully.")
