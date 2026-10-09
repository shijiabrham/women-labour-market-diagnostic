#!/usr/bin/env python3
"""
q17_state_education_labour_market_change.py

Compute change metrics for LFPR, WPR, and Unemployment Rate between 2017 and 2023
using the Q14-Q16 outputs.
"""
import os
import pandas as pd

def pivot_indicator(df, value_col):
    # Keep only year rows (exclude All_Years)
    df_year = df[df['All_Years'] == False]
    # Pivot to have separate columns for 2017 and 2023 values and missing counts
    pivot = df_year.pivot_table(
        index=['Country', 'State', 'Education'],
        columns='Year',
        values=[value_col, 'Missing_Count'],
        aggfunc='first'
    )
    # Flatten MultiIndex columns
    pivot.columns = ['_'.join([str(col[0]), str(col[1])]) for col in pivot.columns]
    # Ensure the expected columns exist; fill missing with None
    for col in [f"{value_col}_2017", f"{value_col}_2023", f"Missing_Count_2017", f"Missing_Count_2023"]:
        if col not in pivot.columns:
            pivot[col] = None
    return pivot.reset_index()

def compute_change(df, indicator_name):
    # df has columns: Country, State, Education, Value_2017, Value_2023, Missing_Count_2017, Missing_Count_2023
    df = df.copy()
    df['Value_2017'] = df[f"{indicator_name}_2017"]
    df['Value_2023'] = df[f"{indicator_name}_2023"]
    df['Absolute_Change'] = df['Value_2023'] - df['Value_2017']
    # Percentage change with guard against division by zero or missing
    def pct(row):
        v2017 = row['Value_2017']
        v2023 = row['Value_2023']
        if pd.isna(v2017) or v2017 == 0:
            return None
        return ((v2023 - v2017) / v2017) * 100
    df['Percentage_Change'] = df.apply(pct, axis=1)
    # Keep required columns
    out = df[['Country', 'State', 'Education', 'Value_2017', 'Value_2023',
               'Absolute_Change', 'Percentage_Change',
               'Missing_Count_2017', 'Missing_Count_2023']].copy()
    out['Indicator'] = indicator_name
    # Reorder columns
    out = out[['Country', 'State', 'Education', 'Indicator', 'Value_2017', 'Value_2023',
               'Absolute_Change', 'Percentage_Change', 'Missing_Count_2017', 'Missing_Count_2023']]
    return out

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    phase_dir = os.path.join(base_dir, 'phase_4_eda')
    # Load Q14-Q16 CSVs
    q14_path = os.path.join(phase_dir, 'q14_state_education_lfpr.csv')
    q15_path = os.path.join(phase_dir, 'q15_state_education_wpr.csv')
    q16_path = os.path.join(phase_dir, 'q16_state_education_unemployment.csv')
    q14 = pd.read_csv(q14_path)
    q15 = pd.read_csv(q15_path)
    q16 = pd.read_csv(q16_path)
    # Pivot each indicator to get 2017/2023 values
    lfpr_pivot = pivot_indicator(q14, 'LFPR')
    wpr_pivot = pivot_indicator(q15, 'WPR')
    ur_pivot = pivot_indicator(q16, 'Unemployment_Rate')
    # Compute changes
    lfpr_change = compute_change(lfpr_pivot, 'LFPR')
    wpr_change = compute_change(wpr_pivot, 'WPR')
    ur_change = compute_change(ur_pivot, 'Unemployment_Rate')
    # Concatenate results
    result = pd.concat([lfpr_change, wpr_change, ur_change], ignore_index=True, sort=False)
    # Output path
    out_path = os.path.join(phase_dir, 'q17_state_education_labour_market_change.csv')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == '__main__':
    main()
