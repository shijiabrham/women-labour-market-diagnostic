#!/usr/bin/env python3
"""
q10_state_area_lfpr.py

Compute female Labor Force Participation Rate (LFPR) by State × Area_Type and Year.
Outputs a CSV with columns:
Country,State,Area_Type,Year,LFPR,Missing_Count,All_Years

All_Years row aggregates across available years (mean of LFPR).
Missing_Count is the count of missing LFPR values for that State/Area_Type/Year.
"""

import pandas as pd
import os

def main():
    # Paths
    data_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv")
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q10_state_area_lfpr.csv"))

    # Load dataset
    df = pd.read_csv(data_path)
    # Filter female rows
    df_female = df[df["Gender"] == "Female"].copy()
    # Keep relevant columns
    # The LFPR column name in the dataset is the first metric column after Education Level etc.
    # It is the column named "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
    lfpr_col = "Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1"
    # Rename for convenience
    df_female = df_female.rename(columns={lfpr_col: "LFPR"})
    # Ensure Area_Type is the column "Type Of Areas"
    df_female = df_female.rename(columns={"Type Of Areas": "Area_Type"})
    # Extract Year numeric from Year column (e.g., "PLFS Year (Jul - Jun), 2023")
    df_female["Year"] = df_female["Year"].str.extract(r"(\d{4})").astype(int)
    # Select needed columns
    cols = ["Country", "State", "Area_Type", "Year", "LFPR"]
    df_female = df_female[cols]
    # Missing count per row (if LFPR is NaN)
    df_female["Missing_Count"] = df_female["LFPR"].isna().astype(int)
    # Compute aggregated rows per State/Area_Type/Year (mean of LFPR, sum of Missing_Count)
    agg_year = (
        df_female.groupby(["Country", "State", "Area_Type", "Year"], as_index=False)
        .agg({"LFPR": "mean", "Missing_Count": "sum"})
        .assign(All_Years=False)
    )
    # Compute All_Years aggregate per State/Area_Type
    agg_all = (
        df_female.groupby(["Country", "State", "Area_Type"], as_index=False)
        .agg({"LFPR": "mean", "Missing_Count": "sum"})
        .assign(Year="All_Years", All_Years=True)
    )
    # Combine year-level and all-years aggregates
    result = pd.concat([agg_year, agg_all], ignore_index=True, sort=False)
    # Order columns
    result = result[["Country", "State", "Area_Type", "Year", "LFPR", "Missing_Count", "All_Years"]]
    # Write CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.to_csv(output_path, index=False, float_format='%.3f')

if __name__ == "__main__":
    main()
