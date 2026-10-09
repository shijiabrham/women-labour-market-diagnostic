#!/usr/bin/env python3
"""
q14_state_education_lfpr.py

Compute mean LFPR for women by State, Education, Year.
Outputs one row per State×Education×Year and an All_Years aggregate per State×Education.
"""
import os
import pandas as pd

def main():
    # Paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    src_path = os.path.join(base_dir, 'dataset_1_profile', 'feature_engineered_dataset_1.csv')
    out_path = os.path.join(base_dir, 'phase_4_eda', 'q14_state_education_lfpr.csv')

    # Load data
    df = pd.read_csv(src_path)
    # Filter female
    df = df[df['Gender'] == 'Female']
    # Identify education column
    edu_col = 'Education Level'
    # Rename LFPR column for convenience
    lfpr_col = 'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1'
    df = df.rename(columns={lfpr_col: 'LFPR'})
    # Keep needed columns
    df = df[['Country', 'State', edu_col, 'Year', 'LFPR']]
    df = df.rename(columns={edu_col: 'Education'})
    # Compute missing count per row group later
    # Group by State, Education, Year
    agg = df.groupby(['Country', 'State', 'Education', 'Year'], dropna=False).apply(
        lambda g: pd.Series({
            'LFPR': round(g['LFPR'].mean(skipna=True), 3) if not g['LFPR'].isna().all() else None,
            'Missing_Count': g['LFPR'].isna().sum()
        })
    ).reset_index()
    # All_Years aggregate per State, Education
    agg_all = df.groupby(['Country', 'State', 'Education'], dropna=False).apply(
        lambda g: pd.Series({
            'LFPR': round(g['LFPR'].mean(skipna=True), 3) if not g['LFPR'].isna().all() else None,
            'Missing_Count': g['LFPR'].isna().sum(),
            'All_Years': True
        })
    ).reset_index()
    agg_all['Year'] = 'All_Years'
    agg_all['All_Years'] = True
    # For year rows set All_Years to False
    agg['All_Years'] = False
    # Combine
    result = pd.concat([agg, agg_all], ignore_index=True, sort=False)
    # Ensure column order
    result = result[['Country', 'State', 'Education', 'Year', 'LFPR', 'Missing_Count', 'All_Years']]
    # Write output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == '__main__':
    main()
