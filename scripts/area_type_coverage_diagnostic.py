#!/usr/bin/env python3
"""
area_type_coverage_diagnostic.py

Prints a diagnostic table showing, for each State, which Area_Type categories are present
in the feature‑engineered dataset (female observations only).
The script writes the table to stdout – the narrative script will capture this output.
"""
import pandas as pd, os, sys

def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv")
    df = pd.read_csv(data_path)
    df_f = df[df["Gender"] == "Female"].copy()
    df_f = df_f.rename(columns={"Type Of Areas": "Area_Type"})
    # Determine which area types appear for each state
    coverage = (
        df_f.groupby('State')['Area_Type']
        .apply(lambda x: sorted(set(x)))
        .reset_index(name='Area_Types')
    )
    # Print nicely
    print("Area‑Type Coverage Diagnostic (Female observations)")
    print("State\tArea_Types")
    for _, row in coverage.iterrows():
        print(f"{row['State']}\t{', '.join(row['Area_Types'])}")

if __name__ == "__main__":
    main()
