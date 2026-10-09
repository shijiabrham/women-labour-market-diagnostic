#!/usr/bin/env python3
"""
q17_state_education_labour_market_change_validation.py

Validate the Q17 change output CSV against Q14-Q16.
"""
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'phase_4_eda'))
    csv_path = os.path.join(base_dir, 'q17_state_education_labour_market_change.csv')
    out_path = os.path.join(base_dir, 'q17_state_education_labour_market_change_validation.md')
    expected_cols = ["Country", "State", "Education", "Indicator", "Value_2017", "Value_2023", "Absolute_Change", "Percentage_Change", "Missing_Count_2017", "Missing_Count_2023"]
    report = []
    if not os.path.isfile(csv_path):
        report.append(f"- **FAIL**: File not found at `{csv_path}`")
    else:
        df = pd.read_csv(csv_path)
        if list(df.columns) != expected_cols:
            report.append(f"- **FAIL**: Columns mismatch. Expected {expected_cols}, got {list(df.columns)}")
        else:
            report.append("- **PASS**: Column order correct.")
        # Load source to compute combos
        src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'dataset_1_profile', 'feature_engineered_dataset_1.csv'))
        src = pd.read_csv(src_path)
        female = src[src['Gender'] == 'Female']
        edu_col = 'Education Level'
        combos = female[['State', edu_col]].drop_duplicates()
        num_states = combos['State'].nunique()
        num_edu = combos[edu_col].nunique()
        expected_rows = num_states * num_edu * 3  # three indicators
        actual_rows = len(df)
        if actual_rows != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows}, got {actual_rows}")
        else:
            report.append("- **PASS**: Row count correct.")
        # Cross‑check endpoint values against Q14‑Q16
        # Load the three source CSVs
        q14 = pd.read_csv(os.path.join(base_dir, 'q14_state_education_lfpr.csv'))
        q15 = pd.read_csv(os.path.join(base_dir, 'q15_state_education_wpr.csv'))
        q16 = pd.read_csv(os.path.join(base_dir, 'q16_state_education_unemployment.csv'))
        # Helper to extract 2017/2023 values
        def extract_vals(df, value_col):
            df_year = df[df['All_Years'] == False]
            piv = df_year.pivot_table(index=['Country', 'State', 'Education'], columns='Year', values=[value_col, 'Missing_Count'], aggfunc='first')
            piv.columns = ['_'.join([str(c[0]), str(c[1])]) for c in piv.columns]
            for col in [f"{value_col}_2017", f"{value_col}_2023", f"Missing_Count_2017", f"Missing_Count_2023"]:
                if col not in piv.columns:
                    piv[col] = None
            return piv.reset_index()
        lfpr_vals = extract_vals(q14, 'LFPR')
        wpr_vals = extract_vals(q15, 'WPR')
        ur_vals = extract_vals(q16, 'Unemployment_Rate')
        # Merge with change df for each indicator
        for ind, src_vals in [('LFPR', lfpr_vals), ('WPR', wpr_vals), ('Unemployment_Rate', ur_vals)]:
            sub = df[df['Indicator'] == ind]
            merged = sub.merge(src_vals, on=['Country', 'State', 'Education'], how='left')
            mismatches = (merged['Value_2017'] != merged[f"{ind}_2017"]).sum() + (merged['Value_2023'] != merged[f"{ind}_2023"]).sum()
            if mismatches == 0:
                report.append(f"- **PASS**: {ind} endpoint values match source CSVs.")
            else:
                report.append(f"- **FAIL**: {ind} endpoint value mismatches: {mismatches} issues.")
    # Write report
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write("# Q17 Labour‑Market Change Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == '__main__':
    main()
