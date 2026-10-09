import csv, math, os
from pathlib import Path

def read_csv(path):
    """Read a CSV file and return a dict mapping State to row dict."""
    data = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row['State']
            data[state] = row
    return data

def read_combined_qx(path, qid):
    """Read the combined results CSV and return a dict mapping State to the row for the given QuestionID.
    Prefers the row where Year == 'All' if present; otherwise takes the first row for that state.
    """
    result = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('QuestionID') != qid:
                continue
            state = row.get('State')
            if row.get('Year') == 'All':
                result[state] = row
                continue
            if state not in result:
                result[state] = row
    return result

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

def pearson(x_vals, y_vals):
    n = len(x_vals)
    if n == 0:
        return None, 0
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_x2 = sum(v * v for v in x_vals)
    sum_y2 = sum(v * v for v in y_vals)
    sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
    numerator = sum_xy - (sum_x * sum_y) / n
    denom_part1 = sum_x2 - (sum_x * sum_x) / n
    denom_part2 = sum_y2 - (sum_y * sum_y) / n
    denominator = math.sqrt(denom_part1 * denom_part2)
    if denominator == 0:
        return None, n
    r = numerator / denominator
    return r, n

def main():
    base_dir = Path('/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic')
    out_dir = base_dir / 'outputs' / 'phase_4_eda'
    out_dir.mkdir(parents=True, exist_ok=True)

    combined_path = out_dir / 'phase_4_dataset_1_eda_results.csv'
    q7_path = out_dir / 'q7_state_unemployment_rate.csv'
    q8_path = out_dir / 'q8_state_lfpr_change.csv'
    result_path = out_dir / 'q9_state_labour_market_patterns.csv'

    # Load source files
    q5 = read_combined_qx(combined_path, 'Q5')
    q6 = read_combined_qx(combined_path, 'Q6')
    q7 = read_csv(q7_path)
    q8 = read_csv(q8_path)
    result = read_csv(result_path)

    # Re‑compute medians for pattern assignment
    lfpr_vals = [safe_float(row.get('LFPR_All_Years')) for row in q5.values() if safe_float(row.get('LFPR_All_Years')) is not None]
    wpr_vals = [safe_float(row.get('WPR_All_Years')) for row in q6.values() if safe_float(row.get('WPR_All_Years')) is not None]
    unemp_vals = [safe_float(row.get('Unemployment_Rate_All_Years')) for row in q7.values() if safe_float(row.get('Unemployment_Rate_All_Years')) is not None]

    lfpr_median = median(lfpr_vals)
    wpr_median = median(wpr_vals)
    unemp_median = median(unemp_vals)

    # Validation flags
    PASS = True
    mismatches = []

    # Helper for tolerance compare after rounding to 3 decimals
    def compare(val1, val2):
        if val1 is None and val2 is None:
            return True
        if val1 is None or val2 is None:
            return False
        try:
            v1 = round(float(val1), 3)
            v2 = round(float(val2), 3)
            return abs(v1 - v2) <= 1e-6
        except Exception:
            return False

    # Validate each row
    for state, exp_row in result.items():
        src5 = q5.get(state, {})
        src6 = q6.get(state, {})
        src7 = q7.get(state, {})
        src8 = q8.get(state, {})

        # Numeric columns
        col_map = {
            'LFPR_All_Years': src5,
            'WPR_All_Years': src6,
            'Unemployment_Rate_All_Years': src7,
            'LFPR_2017_Mean': src8,
            'LFPR_2023_Mean': src8,
            'Absolute_Change': src8,
            'Percentage_Change': src8,
        }
        for col, src in col_map.items():
            if not compare(exp_row.get(col), src.get(col)):
                mismatches.append((state, col, exp_row.get(col), src.get(col)))
                PASS = False

        # Pattern groups
        lfpr_all = safe_float(src5.get('LFPR_All_Years'))
        wpr_all = safe_float(src6.get('WPR_All_Years'))
        unemp_all = safe_float(src7.get('Unemployment_Rate_All_Years'))

        # LFPR‑WPR group
        if lfpr_all is not None and wpr_all is not None:
            if lfpr_all >= lfpr_median and wpr_all >= wpr_median:
                expected_wpr = 'Above-median LFPR / Above-median WPR'
            elif lfpr_all >= lfpr_median and wpr_all < wpr_median:
                expected_wpr = 'Above-median LFPR / Below-median WPR'
            elif lfpr_all < lfpr_median and wpr_all >= wpr_median:
                expected_wpr = 'Below-median LFPR / Above-median WPR'
            else:
                expected_wpr = 'Below-median LFPR / Below-median WPR'
        else:
            expected_wpr = ''
        if exp_row.get('LFPR_WPR_Pattern_Group') != expected_wpr:
            mismatches.append((state, 'LFPR_WPR_Pattern_Group', exp_row.get('LFPR_WPR_Pattern_Group'), expected_wpr))
            PASS = False

        # LFPR‑Unemployment group
        if lfpr_all is not None and unemp_all is not None:
            if lfpr_all >= lfpr_median and unemp_all >= unemp_median:
                expected_unemp = 'Above-median LFPR / Above-median Unemployment'
            elif lfpr_all >= lfpr_median and unemp_all < unemp_median:
                expected_unemp = 'Above-median LFPR / Below-median Unemployment'
            elif lfpr_all < lfpr_median and unemp_all >= unemp_median:
                expected_unemp = 'Below-median LFPR / Above-median Unemployment'
            else:
                expected_unemp = 'Below-median LFPR / Below-median Unemployment'
        else:
            expected_unemp = ''
        if exp_row.get('LFPR_Unemployment_Pattern_Group') != expected_unemp:
            mismatches.append((state, 'LFPR_Unemployment_Pattern_Group', exp_row.get('LFPR_Unemployment_Pattern_Group'), expected_unemp))
            PASS = False

        # LFPR‑Change group
        change_val = safe_float(src8.get('Absolute_Change'))
        if change_val is None:
            expected_change = ''
        else:
            if change_val > 0.1:
                expected_change = 'Increase'
            elif change_val < -0.1:
                expected_change = 'Decrease'
            else:
                expected_change = 'Stable'
        if exp_row.get('LFPR_Change_Pattern_Group') != expected_change:
            mismatches.append((state, 'LFPR_Change_Pattern_Group', exp_row.get('LFPR_Change_Pattern_Group'), expected_change))
            PASS = False

    # Compute pattern group counts
    counts_wpr = {}
    counts_unemp = {}
    counts_change = {}
    missing_wpr = missing_unemp = missing_change = 0
    for row in result.values():
        grp = row.get('LFPR_WPR_Pattern_Group')
        if grp:
            counts_wpr[grp] = counts_wpr.get(grp, 0) + 1
        else:
            missing_wpr += 1
        grp = row.get('LFPR_Unemployment_Pattern_Group')
        if grp:
            counts_unemp[grp] = counts_unemp.get(grp, 0) + 1
        else:
            missing_unemp += 1
        grp = row.get('LFPR_Change_Pattern_Group')
        if grp:
            counts_change[grp] = counts_change.get(grp, 0) + 1
        else:
            missing_change += 1

    # Correlations (pairwise complete observations)
    lfpr_all_list = []
    wpr_all_list = []
    unemp_all_list = []
    lfpr_2017_list = []
    lfpr_2023_list = []
    lfpr_change_abs_list = []
    for state, row in result.items():
        lfpr = safe_float(row.get('LFPR_All_Years'))
        wpr = safe_float(row.get('WPR_All_Years'))
        unemp = safe_float(row.get('Unemployment_Rate_All_Years'))
        lfpr17 = safe_float(row.get('LFPR_2017_Mean'))
        lfpr23 = safe_float(row.get('LFPR_2023_Mean'))
        change_abs = safe_float(row.get('Absolute_Change'))
        if lfpr is not None and wpr is not None:
            lfpr_all_list.append(lfpr)
            wpr_all_list.append(wpr)
        if lfpr is not None and unemp is not None:
            lfpr_all_list.append(lfpr)
            unemp_all_list.append(unemp)
        if wpr is not None and unemp is not None:
            wpr_all_list.append(wpr)
            unemp_all_list.append(unemp)
        if lfpr17 is not None and lfpr23 is not None:
            lfpr_2017_list.append(lfpr17)
            lfpr_2023_list.append(lfpr23)
        if change_abs is not None and wpr is not None:
            lfpr_change_abs_list.append(change_abs)
            wpr_all_list.append(wpr)
    corr_results = {}
    r, n = pearson(lfpr_all_list, wpr_all_list)
    corr_results['LFPR vs WPR'] = (r, n)
    r, n = pearson(lfpr_all_list, unemp_all_list)
    corr_results['LFPR vs Unemployment'] = (r, n)
    r, n = pearson(wpr_all_list, unemp_all_list)
    corr_results['WPR vs Unemployment'] = (r, n)
    r, n = pearson(lfpr_2017_list, lfpr_2023_list)
    corr_results['LFPR 2017 vs LFPR 2023'] = (r, n)
    r, n = pearson(lfpr_change_abs_list, wpr_all_list)
    corr_results['LFPR Change vs WPR'] = (r, n)

    # Write validation markdown
    report_path = out_dir / 'q9_state_labour_market_patterns_validation.md'
    with open(report_path, 'w') as f:
        f.write('# Q9 Validation Report\n\n')
        f.write('## Overall Result\n')
        f.write('PASS\n\n' if PASS else 'FAIL\n\n')
        if not PASS:
            f.write('### Mismatches\n')
            for state, col, got, exp in mismatches:
                f.write(f"- {state}: {col} – got `{got}`, expected `{exp}`\n")
            f.write('\n')
        f.write('## Pattern Group Counts\n')
        f.write('### LFPR‑WPR groups\n')
        for grp, cnt in counts_wpr.items():
            f.write(f"- {grp}: {cnt}\n")
        f.write(f"- Missing/Unassigned: {missing_wpr}\n\n")
        f.write('### LFPR‑Unemployment groups\n')
        for grp, cnt in counts_unemp.items():
            f.write(f"- {grp}: {cnt}\n")
        f.write(f"- Missing/Unassigned: {missing_unemp}\n\n")
        f.write('### LFPR Change groups\n')
        for grp, cnt in counts_change.items():
            f.write(f"- {grp}: {cnt}\n")
        f.write(f"- Missing/Unassigned (e.g., Chandigarh): {missing_change}\n\n")
        f.write('## Pearson Correlations (pairwise complete observations)\n')
        for name, (r_val, n_val) in corr_results.items():
            if r_val is None:
                f.write(f"- {name}: insufficient data (n={n_val})\n")
            else:
                f.write(f"- {name}: r = {r_val:.4f} (n = {n_val})\n")
        f.write('\n')
    print('Validation report written to', report_path)

if __name__ == '__main__':
    main()
