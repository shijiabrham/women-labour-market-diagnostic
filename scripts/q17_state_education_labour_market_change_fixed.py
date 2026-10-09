#!/usr/bin/env python3
"""
Generate Q17 change output with endpoint values for each indicator (LFPR, WPR, Unemployment_Rate).
"""
import os
import pandas as pd

def extract_endpoint(df, value_col):
    # Filter out All_Years rows
    df_year = df[df['All_Years'] == False]
    # Pivot to get 2017 and 2023 values and missing counts
    piv = df_year.pivot_table(index=['Country', 'State', 'Education'], columns='Year', values=[value_col, 'Missing_Count'], aggfunc='first')
    # Flatten MultiIndex columns
    piv.columns = ['_'.join([str(c[0]), str(c[1])]) for c in piv.columns]
    # Ensure required columns exist
    for col in [f"{value_col}_2017", f"{value_col}_2023", "Missing_Count_2017", "Missing_Count_2023"]:
        if col not in piv.columns:
            piv[col] = None
    return piv.reset_index()

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs', 'phase_4_eda'))
    # Load source indicator files
    q14 = pd.read_csv(os.path.join(base_dir, 'q14_state_education_lfpr.csv'))
    q15 = pd.read_csv(os.path.join(base_dir, 'q15_state_education_wpr.csv'))
    q16 = pd.read_csv(os.path.join(base_dir, 'q16_state_education_unemployment.csv'))
    # Extract endpoint values for each indicator
    lfpr_vals = extract_endpoint(q14, 'LFPR')
    wpr_vals = extract_endpoint(q15, 'WPR')
    ur_vals = extract_endpoint(q16, 'Unemployment_Rate')
    # Prepare a list to collect rows
    rows = []
    indicators = {
        'LFPR': lfpr_vals,
        'WPR': wpr_vals,
        'Unemployment_Rate': ur_vals,
    }
    for ind, src in indicators.items():
        for _, row in src.iterrows():
            val_2017 = row.get(f"{ind}_2017")
            val_2023 = row.get(f"{ind}_2023")
            # Compute changes handling missing values
            if pd.isna(val_2017) or pd.isna(val_2023):
                abs_change = None
                perc_change = None
            else:
                abs_change = val_2023 - val_2017
                perc_change = ((abs_change) / val_2017 * 100) if val_2017 != 0 else None
            rows.append({
                'Country': row['Country'],
                'State': row['State'],
                'Education': row['Education'],
                'Indicator': ind,
                'Value_2017': val_2017,
                'Value_2023': val_2023,
                'Absolute_Change': abs_change,
                'Percentage_Change': perc_change,
                'Missing_Count_2017': row.get('Missing_Count_2017'),
                'Missing_Count_2023': row.get('Missing_Count_2023'),
            })
    out_df = pd.DataFrame(rows)
    # Ensure column order
    out_df = out_df[[
        'Country', 'State', 'Education', 'Indicator',
        'Value_2017', 'Value_2023', 'Absolute_Change', 'Percentage_Change',
        'Missing_Count_2017', 'Missing_Count_2023'
    ]]
    out_path = os.path.join(base_dir, 'q17_state_education_labour_market_change.csv')
    out_df.to_csv(out_path, index=False)
    print(f"Generated Q17 with {len(out_df)} rows at {out_path}")

if __name__ == "__main__":
    main()
