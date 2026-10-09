#!/usr/bin/env python3
"""
q13_state_area_labour_market_change.py

Compute absolute and percentage change (2017 → 2023) for LFPR, WPR, and Unemployment Rate
per State × Area_Type.
Outputs a CSV with columns:
Country,State,Area_Type,Indicator,Absolute_Change,Percentage_Change,Missing_Count_2017,Missing_Count_2023
"""
import os
import pandas as pd

def load_indicator(csv_path, value_col):
    df = pd.read_csv(csv_path)
    # Ensure All_Years is boolean (handle string representations)
    if df['All_Years'].dtype != bool:
        df['All_Years'] = df['All_Years'].astype(str).str.lower().map({'true': True, 'false': False})
    # Keep only 2017 and 2023 rows, exclude aggregate "All_Years" rows
    df = df[(df['Year'].astype(str).isin(['2017', '2023'])) & (df['All_Years'] == False)]
    # Retain needed columns
    df = df[['Country', 'State', 'Area_Type', 'Year', value_col, 'Missing_Count']]
    return df

def pivot_dataframe(df, value_col):
    # Pivot so that years become separate columns for both the value and missing count
    pivoted = df.pivot_table(
        index=['Country', 'State', 'Area_Type'],
        columns='Year',
        values=[value_col, 'Missing_Count'],
        aggfunc='first'
    )
    # Flatten MultiIndex columns to strings like "LFPR_2017"
    pivoted.columns = [f"{col[0]}_{col[1]}" for col in pivoted.columns]
    return pivoted.reset_index()

def compute_change(df, indicator_name):
    # df contains columns: Country, State, Area_Type, <indicator>_2017, <indicator>_2023,
    # Missing_Count_2017, Missing_Count_2023
    # Preserve endpoint values
    df['Value_2017'] = df[f"{indicator_name}_2017"]
    df['Value_2023'] = df[f"{indicator_name}_2023"]
    # Compute absolute change
    df['Absolute_Change'] = df['Value_2023'] - df['Value_2017']
    # Percentage change, handling division by zero or missing safely
    def pct(row):
        base = row['Value_2017']
        if pd.isna(base) or base == 0:
            return None
        return (row['Absolute_Change'] / base) * 100
    df['Percentage_Change'] = df.apply(pct, axis=1)
    # Missing counts are already present as columns Missing_Count_2017 and Missing_Count_2023
    # Assemble output with required columns and order
    out = df[['Country', 'State', 'Area_Type',
              'Value_2017', 'Value_2023',
              'Absolute_Change', 'Percentage_Change',
              'Missing_Count_2017', 'Missing_Count_2023']].copy()
    out['Indicator'] = indicator_name
    out = out[['Country', 'State', 'Area_Type', 'Indicator',
               'Value_2017', 'Value_2023',
               'Absolute_Change', 'Percentage_Change',
               'Missing_Count_2017', 'Missing_Count_2023']]
    return out

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'phase_4_eda'))
    lfpr_path = os.path.join(base_dir, 'q10_state_area_lfpr.csv')
    wpr_path = os.path.join(base_dir, 'q11_state_area_wpr.csv')
    ur_path = os.path.join(base_dir, 'q12_state_area_unemployment.csv')

    lfpr = load_indicator(lfpr_path, 'LFPR')
    wpr = load_indicator(wpr_path, 'WPR')
    ur = load_indicator(ur_path, 'Unemployment_Rate')

    lfpr_p = pivot_dataframe(lfpr, 'LFPR')
    wpr_p = pivot_dataframe(wpr, 'WPR')
    ur_p = pivot_dataframe(ur, 'Unemployment_Rate')

    lfpr_change = compute_change(lfpr_p, 'LFPR')
    wpr_change = compute_change(wpr_p, 'WPR')
    ur_change = compute_change(ur_p, 'Unemployment_Rate')

    result = pd.concat([lfpr_change, wpr_change, ur_change], ignore_index=True)
    out_path = os.path.join(base_dir, 'q13_state_area_labour_market_change.csv')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result.to_csv(out_path, index=False, float_format='%.3f')

if __name__ == '__main__':
    main()
