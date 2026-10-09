#!/usr/bin/env python3
"""
q11_state_area_wpr.py

Compute female Working Population Rate (WPR) by State × Area_Type and Year.
Outputs a CSV with columns:
Country,State,Area_Type,Year,WPR,Missing_Count,All_Years
"""
import pandas as pd, os

def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv")
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q11_state_area_wpr.csv"))
    df = pd.read_csv(data_path)
    df_f = df[df["Gender"] == "Female"].copy()
    wpr_col = "Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
    df_f = df_f.rename(columns={wpr_col: "WPR"})
    df_f = df_f.rename(columns={"Type Of Areas": "Area_Type"})
    df_f["Year"] = df_f["Year"].str.extract(r"(\d{4})").astype(int)
    df_f = df_f[["Country", "State", "Area_Type", "Year", "WPR"]]
    df_f["Missing_Count"] = df_f["WPR"].isna().astype(int)
    # Compute aggregated rows per State/Area_Type/Year (mean of WPR, sum of Missing_Count)
    agg_year = (
        df_f.groupby(["Country", "State", "Area_Type", "Year"], as_index=False)
        .agg({"WPR": "mean", "Missing_Count": "sum"})
        .assign(All_Years=False)
    )
    # Compute All_Years aggregate per State/Area_Type
    agg_all = (
        df_f.groupby(["Country", "State", "Area_Type"], as_index=False)
        .agg({"WPR": "mean", "Missing_Count": "sum"})
        .assign(Year="All_Years", All_Years=True)
    )
    result = pd.concat([agg_year, agg_all], ignore_index=True, sort=False)
    result = result[["Country", "State", "Area_Type", "Year", "WPR", "Missing_Count", "All_Years"]]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == "__main__":
    main()
