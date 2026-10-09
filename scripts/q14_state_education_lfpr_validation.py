#!/usr/bin/env python3
"""
q14_state_education_lfpr_validation.py

Validate the Q14 LFPR output CSV.
"""
import os
import pandas as pd

def main():
    # Adjust base directory to workspace root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = os.path.join(base_dir, 'outputs', 'phase_4_eda', 'q14_state_education_lfpr.csv')
    out_path = os.path.join(base_dir, 'outputs', 'phase_4_eda', 'q14_state_education_lfpr_validation.md')
    # Expected columns
    expected_cols = ["Country", "State", "Education", "Year", "LFPR", "Missing_Count", "All_Years"]
    report = []
    if not os.path.isfile(csv_path):
        report.append(f"- **FAIL**: File not found at `{csv_path}`")
    else:
        df = pd.read_csv(csv_path)
        # Column order check
        if list(df.columns) != expected_cols:
            report.append(f"- **FAIL**: Columns mismatch. Expected {expected_cols}, got {list(df.columns)}")
        else:
            report.append("- **PASS**: Column order correct.")
        # Load source to compute combos
        src_path = os.path.join(base_dir, 'outputs', 'dataset_1_profile', 'feature_engineered_dataset_1.csv')
        src = pd.read_csv(src_path)
        female = src[src['Gender'] == 'Female']
        edu_col = 'Education Level'
        combos = female[['State', edu_col]].drop_duplicates()
        num_states = combos['State'].nunique()
        num_edu = combos[edu_col].nunique()
        years = range(2017, 2024)
        expected_rows = num_states * num_edu * len(years) + num_states * num_edu  # All_Years rows
        actual_rows = len(df)
        if actual_rows != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows}, got {actual_rows}")
        else:
            report.append("- **PASS**: Row count correct.")
        # Uniqueness check for State/Education/Year where All_Years is False
        dup = df[df['All_Years'] == False].duplicated(subset=['State', 'Education', 'Year']).any()
        if dup:
            report.append("- **FAIL**: Duplicate State/Education/Year rows found.")
        else:
            report.append("- **PASS**: No duplicate State/Education/Year rows.")
        # Missing count column exists
        if 'Missing_Count' in df.columns:
            report.append("- **PASS**: Missing_Count column present.")
        else:
            report.append("- **FAIL**: Missing_Count column missing.")
        # Rounding check (three decimals) for LFPR values that are not null
        if df['LFPR'].dropna().apply(lambda x: len(str(x).split('.')[-1]) <= 3).all():
            report.append("- **PASS**: LFPR values rounded to three decimals.")
        else:
            report.append("- **FAIL**: LFPR rounding issue.")
    # Write report
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write("# Q14 LFPR Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == '__main__':
    main()
