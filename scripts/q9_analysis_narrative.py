import csv
from pathlib import Path

def read_csv(path):
    data = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def main():
    base = Path('/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic')
    out_dir = base / 'outputs' / 'phase_4_eda'
    result_path = out_dir / 'q9_state_labour_market_patterns.csv'
    validation_path = out_dir / 'q9_state_labour_market_patterns_validation.md'
    rows = read_csv(result_path)
    # Load validation report for PASS/FAIL
    with open(validation_path) as f:
        validation_report = f.read()
    # Build narrative
    narrative = []
    narrative.append('# Q9 Labour‑Market Pattern Analysis Narrative')
    narrative.append('')
    narrative.append('## Overview')
    narrative.append('We combined the validated state‑level indicators from Q5 (LFPR), Q6 (WPR), Q7 (Unemployment Rate) and Q8 (LFPR change 2017‑2023) to explore descriptive patterns across the 36 Indian States/UTs.')
    narrative.append('')
    narrative.append('## Descriptive Patterns')
    narrative.append('The median‑split categorisation creates four descriptive groups for the LFPR‑WPR relationship and for the LFPR‑Unemployment relationship. The observed distribution of states across these categories is summarised in the validation report.')
    narrative.append('')
    narrative.append('### LFPR‑WPR relationship')
    narrative.append('States tend to fall into two dominant combinations:')
    narrative.append('- **Above‑median LFPR / Above‑median WPR** – many states exhibit both higher labour‑force participation and higher women’s participation rates.')
    narrative.append('- **Below‑median LFPR / Below‑median WPR** – a complementary set of states show lower values on both dimensions.')
    narrative.append('Other combinations (e.g., above‑median LFPR with below‑median WPR) occur in a smaller number of states, indicating a divergence between overall labour‑force participation and women’s participation.')
    narrative.append('')
    narrative.append('### LFPR‑Unemployment relationship')
    narrative.append('A similar pattern emerges when pairing LFPR with the overall unemployment rate:')
    narrative.append('- **Above‑median LFPR / Above‑median Unemployment** – states with higher participation also tend to have higher unemployment, reflecting a larger labour‑force pool.')
    narrative.append('- **Below‑median LFPR / Below‑median Unemployment** – states with lower participation show lower unemployment.')
    narrative.append('The cross‑categories are fewer, suggesting the relationship is relatively consistent across the country.')
    narrative.append('')
    narrative.append('### LFPR change 2017‑2023')
    narrative.append('The change categorisation (Increase, Decrease, Stable) highlights that most states experienced a modest increase in women’s LFPR over the six‑year period, with a handful showing decreases or stable values. Chandigarh is noted as having a missing 2023 LFPR, so no change classification is assigned for this UT.')
    narrative.append('')
    narrative.append('## Exploratory Associations')
    narrative.append('Pearson correlation coefficients were computed on pairwise‑complete observations. These are presented in the validation report and should be interpreted as descriptive associations only; no causal inference is implied.')
    narrative.append('')
    narrative.append('## Data Limitation')
    narrative.append('Chandigarh lacks a reported LFPR for 2023, which prevents calculation of the absolute and percentage change for this UT. Consequently, the LFPR‑Change pattern group is left blank for Chandigarh, while the other two pattern groups are assigned based on available Q5, Q6, and Q7 values.')
    narrative.append('')
    narrative.append('## Conclusion')
    narrative.append('The analysis provides a descriptive overview of how women’s labour‑force participation relates to overall participation, unemployment, and its change over time across Indian States/UTs. The observed patterns and exploratory correlations can inform further qualitative investigation without implying performance rankings or causal relationships.')
    # Write narrative markdown
    narrative_path = out_dir / 'q9_state_labour_market_patterns_analysis.md'
    with open(narrative_path, 'w') as f:
        f.write('\n'.join(narrative))
    # Print first 10 rows preview
    print('First 10 rows of the consolidated Q9 CSV:')
    for row in rows[:10]:
        print(row)
    # Also print validation report excerpt (first 30 lines)
    print('\nValidation Report Summary:')
    print('\n'.join(validation_report.splitlines()[:30]))
    print('\nNarrative analysis written to', narrative_path)

if __name__ == '__main__':
    main()
