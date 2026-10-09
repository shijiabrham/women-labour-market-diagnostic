#!/usr/bin/env python3
"""
q15_state_education_wpr.py

Compute mean Working Population Rate (WPR) for women by State, Education, Year.
Outputs one row per State×Education×Year and an All_Years aggregate per State×Education.
"""
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    src_path = os.path.join(base_dir, 'dataset_1_profile', 'feature_engineered_dataset_1.csv')
    out_path = os.path.join(base_dir, 'phase_4_eda', 'q15_state_education_wpr.csv')

    df = pd.read_csv(src_path)
    df = df[df['Gender'] == 'Female']
    edu_col = 'Education Level'
    wpr_col = 'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1'
    df = df.rename(columns={wpr_col: 'WPR'})
    df = df[['Country', 'State', edu_col, 'Year', 'WPR']]
    df = df.rename(columns={edu_col: 'Education'})
    agg = df.groupby(['Country', 'State', 'Education', 'Year'], dropna=False).apply(
        lambda g: pd.Series({
            'WPR': round(g['WPR'].mean(skipna=True), 3) if not g['WPR'].isna().all() else None,
            'Missing_Count': g['WPR'].isna().sum()
        })
    ).reset_index()
    agg_all = df.groupby(['Country', 'State', 'Education'], dropna=False).apply(
        lambda g: pd.Series({
            'WPR': round(g['WPR'].mean(skipna=True), 3) if not g['WPR'].isna().all() else None,
            'Missing_Count': g['WPR'].isna().sum(),
            'All_Years': True
        })
    ).reset_index()
    agg_all['Year'] = 'All_Years'
    agg_all['All_Years'] = True
    agg['All_Years'] = False
    result = pd.concat([agg, agg_all], ignore_index=True, sort=False)
    result = result[['Country', 'State', 'Education', 'Year', 'WPR', 'Missing_Count', 'All_Years']]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == '__main__':
    main()
