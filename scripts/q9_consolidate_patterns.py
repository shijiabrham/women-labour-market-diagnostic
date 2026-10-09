import csv, math, os, sys
from pathlib import Path

def read_csv(path):
    data = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row['State']
            data[state] = row
    return data

def safe_float(val):
    try:
        return float(val)
    except Exception:
        return None

def median(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0:
        return None
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0

def main():
    base_dir = Path('/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic')
    out_dir = base_dir / 'outputs' / 'phase_4_eda'
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load Q5 and Q6 from combined results CSV
    combined_path = out_dir / 'phase_4_dataset_1_eda_results.csv'
    q5 = {}
    q6 = {}
    with open(combined_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get('QuestionID')
            state = row.get('State')
            if qid == 'Q5':
                if row.get('Year') == 'All' or state not in q5:
                    q5[state] = row
            elif qid == 'Q6':
                if row.get('Year') == 'All' or state not in q6:
                    q6[state] = row

    q7_path = out_dir / 'q7_state_unemployment_rate.csv'
    q8_path = out_dir / 'q8_state_lfpr_change.csv'
    q7 = read_csv(q7_path)
    q8 = read_csv(q8_path)

    # Gather all states
    all_states = set(q5) | set(q6) | set(q7) | set(q8)

    rows = []
    lfpr_vals = []
    wpr_vals = []
    unemp_vals = []
    for state in sorted(all_states):
        row = {'State': state}
        row['LFPR_All_Years'] = q5.get(state, {}).get('LFPR_All_Years')
        row['WPR_All_Years'] = q6.get(state, {}).get('WPR_All_Years')
        row['Unemployment_Rate_All_Years'] = q7.get(state, {}).get('Unemployment_Rate_All_Years')
        q8row = q8.get(state, {})
        for col in ['LFPR_2017_Mean','LFPR_2023_Mean','Absolute_Change','Percentage_Change','Valid_2017_Observation_Count','Valid_2023_Observation_Count','Missing_2017_Count','Missing_2023_Count']:
            row[col] = q8row.get(col)
        rows.append(row)
        lfpr = safe_float(row['LFPR_All_Years'])
        wpr = safe_float(row['WPR_All_Years'])
        unemp = safe_float(row['Unemployment_Rate_All_Years'])
        if lfpr is not None:
            lfpr_vals.append(lfpr)
        if wpr is not None:
            wpr_vals.append(wpr)
        if unemp is not None:
            unemp_vals.append(unemp)

    lfpr_median = median(lfpr_vals)
    wpr_median = median(wpr_vals)
    unemp_median = median(unemp_vals)

    # Assign pattern groups
    for row in rows:
        lfpr = safe_float(row['LFPR_All_Years'])
        wpr = safe_float(row['WPR_All_Years'])
        unemp = safe_float(row['Unemployment_Rate_All_Years'])
        # LFPR-WPR pattern group
        if lfpr is not None and wpr is not None:
            if lfpr >= lfpr_median and wpr >= wpr_median:
                row['LFPR_WPR_Pattern_Group'] = 'Above-median LFPR / Above-median WPR'
            elif lfpr >= lfpr_median and wpr < wpr_median:
                row['LFPR_WPR_Pattern_Group'] = 'Above-median LFPR / Below-median WPR'
            elif lfpr < lfpr_median and wpr >= wpr_median:
                row['LFPR_WPR_Pattern_Group'] = 'Below-median LFPR / Above-median WPR'
            else:
                row['LFPR_WPR_Pattern_Group'] = 'Below-median LFPR / Below-median WPR'
        else:
            row['LFPR_WPR_Pattern_Group'] = ''
        # LFPR-Unemployment pattern group
        if lfpr is not None and unemp is not None:
            if lfpr >= lfpr_median and unemp >= unemp_median:
                row['LFPR_Unemployment_Pattern_Group'] = 'Above-median LFPR / Above-median Unemployment'
            elif lfpr >= lfpr_median and unemp < unemp_median:
                row['LFPR_Unemployment_Pattern_Group'] = 'Above-median LFPR / Below-median Unemployment'
            elif lfpr < lfpr_median and unemp >= unemp_median:
                row['LFPR_Unemployment_Pattern_Group'] = 'Below-median LFPR / Above-median Unemployment'
            else:
                row['LFPR_Unemployment_Pattern_Group'] = 'Below-median LFPR / Below-median Unemployment'
        else:
            row['LFPR_Unemployment_Pattern_Group'] = ''
        # LFPR Change pattern group
        change = safe_float(row.get('Absolute_Change'))
        if change is None:
            row['LFPR_Change_Pattern_Group'] = ''
        else:
            if change > 0.1:
                row['LFPR_Change_Pattern_Group'] = 'Increase'
            elif change < -0.1:
                row['LFPR_Change_Pattern_Group'] = 'Decrease'
            else:
                row['LFPR_Change_Pattern_Group'] = 'Stable'

    out_path = out_dir / 'q9_state_labour_market_patterns.csv'
    fieldnames = ['State','LFPR_All_Years','WPR_All_Years','Unemployment_Rate_All_Years','LFPR_2017_Mean','LFPR_2023_Mean','Absolute_Change','Percentage_Change','Valid_2017_Observation_Count','Valid_2023_Observation_Count','Missing_2017_Count','Missing_2023_Count','LFPR_WPR_Pattern_Group','LFPR_Unemployment_Pattern_Group','LFPR_Change_Pattern_Group']
    with open(out_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            for col in ['LFPR_All_Years','WPR_All_Years','Unemployment_Rate_All_Years','LFPR_2017_Mean','LFPR_2023_Mean','Absolute_Change','Percentage_Change']:
                val = safe_float(row.get(col))
                if val is not None:
                    row[col] = f"{val:.3f}"
            writer.writerow({k: row.get(k, '') for k in fieldnames})
    print('First 10 rows of consolidated Q9 CSV:')
    for r in rows[:10]:
        print(r)

if __name__ == '__main__':
    main()
