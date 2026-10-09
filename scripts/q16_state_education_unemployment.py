#!/usr/bin/env python3
"""
q16_state_education_unemployment.py

Compute mean Unemployment Rate for women by State, Education, Year.
Outputs one row per State×Education×Year and an All_Years aggregate per State×Education.
"""
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    src_path = os.path.join(base_dir, 'dataset_1_profile', 'feature_engineered_dataset_1.csv')
    out_path = os.path.join(base_dir, 'phase_4_eda', 'q16_state_education_unemployment.csv')

    df = pd.read_csv(src_path)
    df = df[df['Gender'] == 'Female']
    edu_col = 'Education Level'
    ur_col = 'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1'
    df = df.rename(columns={ur_col: 'Unemployment_Rate'})
    df = df[['Country', 'State', edu_col, 'Year', 'Unemployment_Rate']]
    df = df.rename(columns={edu_col: 'Education'})
    agg = df.groupby(['Country', 'State', 'Education', 'Year'], dropna=False).apply(
        lambda g: pd.Series({
            'Unemployment_Rate': round(g['Unemployment_Rate'].mean(skipna=True), 3) if not g['Unemployment_Rate'].isna().all() else None,
            'Missing_Count': g['Unemployment_Rate'].isna().sum()
        })
    ).reset_index()
    agg_all = df.groupby(['Country', 'State', 'Education'], dropna=False).apply(
        lambda g: pd.Series({
            'Unemployment_Rate': round(g['Unemployment_Rate'].mean(skipna=True), 3) if not g['Unemployment_Rate'].isna().all() else None,
            'Missing_Count': g['Unemployment_Rate'].isna().sum(),
            'All_Years': True
        })
    ).reset_index()
    agg_all['Year'] = 'All_Years'
    agg_all['All_Years'] = True
    agg['All_Years'] = False
    result = pd.concat([agg, agg_all], ignore_index=True, sort=False)
    result = result[['Country', 'State', 'Education', 'Year', 'Unemployment_Rate', 'Missing_Count', 'All_Years']]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == '__main__':
    main()
