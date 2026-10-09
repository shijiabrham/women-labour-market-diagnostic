#!/usr/bin/env python3
"""
q13_state_area_labour_market_change_validation.py

Validate the Q13 change CSV against expected schema, row counts, and endpoint values.
"""
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'phase_4_eda'))
    q13_path = os.path.join(base_dir, 'q13_state_area_labour_market_change.csv')
    out_path = os.path.join(base_dir, 'q13_state_area_labour_market_change_validation.md')
    # Expected columns including endpoint values
    expected_cols = ["Country", "State", "Area_Type", "Indicator",
                    "Value_2017", "Value_2023",
                    "Absolute_Change", "Percentage_Change",
                    "Missing_Count_2017", "Missing_Count_2023"]
    report = []
    if not os.path.isfile(q13_path):
        report.append(f"- **FAIL**: File not found at `{q13_path}`")
    else:
        df = pd.read_csv(q13_path)
        # Column order check
        if list(df.columns) != expected_cols:
            report.append(f"- **FAIL**: Columns mismatch. Expected {expected_cols}, got {list(df.columns)}")
        else:
            report.append("- **PASS**: Column order correct.")
        # Determine actual combos from source dataset
        source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'dataset_1_profile', 'feature_engineered_dataset_1.csv'))
        source_df = pd.read_csv(source_path)
        female_df = source_df[source_df['Gender'] == 'Female']
        combos = female_df[['State', 'Type Of Areas']].drop_duplicates()
        num_states = combos['State'].nunique()
        area_types = combos['Type Of Areas'].unique()
        num_area_types = len(area_types)
        expected_rows = num_states * num_area_types * 3  # three indicators
        actual_rows = len(df)
        if actual_rows != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows}, got {actual_rows}")
        else:
            report.append("- **PASS**: Row count correct.")
        # Verify endpoint values against Q10‑Q12 CSVs
        indicator_files = {
            "LFPR": os.path.join(base_dir, 'q10_state_area_lfpr.csv'),
            "WPR": os.path.join(base_dir, 'q11_state_area_wpr.csv'),
            "Unemployment_Rate": os.path.join(base_dir, 'q12_state_area_unemployment.csv')
        }
        pivots = {}
        for ind, path in indicator_files.items():
            raw = pd.read_csv(path)
            raw = raw[raw['All_Years'] == False]
            p = raw.pivot_table(index=['Country', 'State', 'Area_Type'], columns='Year', values=ind, aggfunc='first')
            p.columns = [f"Value_{col}" for col in p.columns]
            pivots[ind] = p.reset_index()
        # Check each row
        for _, row in df.iterrows():
            ind = row['Indicator']
            exp_df = pivots[ind]
            match = exp_df[(exp_df['Country'] == row['Country']) & (exp_df['State'] == row['State']) & (exp_df['Area_Type'] == row['Area_Type'])]
            if match.empty:
                report.append(f"- **FAIL**: No source match for {ind} {row['State']} {row['Area_Type']}")
                continue
            val_2017 = match['Value_2017'].values[0]
            val_2023 = match['Value_2023'].values[0]
            if not pd.isna(val_2017) and not pd.isna(row['Value_2017']):
                if abs(val_2017 - row['Value_2017']) > 0.001:
                    report.append(f"- **FAIL**: Value_2017 mismatch for {ind} {row['State']} {row['Area_Type']}: expected {val_2017:.3f}, got {row['Value_2017']:.3f}")
            if not pd.isna(val_2023) and not pd.isna(row['Value_2023']):
                if abs(val_2023 - row['Value_2023']) > 0.001:
                    report.append(f"- **FAIL**: Value_2023 mismatch for {ind} {row['State']} {row['Area_Type']}: expected {val_2023:.3f}, got {row['Value_2023']:.3f}")
        if not any('FAIL' in r for r in report):
            report.append("- **PASS**: Endpoint values verified against source CSVs.")
    # Write report
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write("# Q13 Labour‑Market Change Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == '__main__':
    main()
