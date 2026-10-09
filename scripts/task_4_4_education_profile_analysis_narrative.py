#!/usr/bin/env python3
"""
task_4_4_education_profile_analysis_narrative.py

Generate a markdown narrative summarizing the education‑profile diagnostics,
including coverage, sample rows, and row/column counts for Q14‑Q17.
"""
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    phase_dir = os.path.join(base_dir, 'phase_4_eda')
    src_path = os.path.join(base_dir, 'dataset_1_profile', 'feature_engineered_dataset_1.csv')
    # Load source
    src = pd.read_csv(src_path)
    female = src[src['Gender'] == 'Female']
    edu_col = 'Education Level'
    # Diagnostics
    edu_categories = female[edu_col].unique()
    num_categories = len(edu_categories)
    # Count State x Education combos
    combos = female[['State', edu_col]].drop_duplicates()
    num_states = combos['State'].nunique()
    num_combos = len(combos)
    years = sorted(female['Year'].unique())
    # Prepare report sections
    report = []
    report.append("# Education Profile Diagnostic Report\n")
    report.append(f"- Unique education categories (including aggregates): {num_categories}\n  - {', '.join(sorted(edu_categories))}\n")
    report.append(f"- Number of States/UTs represented: {num_states}\n")
    report.append(f"- State × Education combinations present: {num_combos}\n")
    report.append(f"- Years covered in source data (female subset): {', '.join(map(str, years))}\n")
    # For each Q14‑Q17 output, add summary
    files = {
        'Q14 LFPR': 'q14_state_education_lfpr.csv',
        'Q15 WPR': 'q15_state_education_wpr.csv',
        'Q16 Unemployment': 'q16_state_education_unemployment.csv',
        'Q17 Change': 'q17_state_education_labour_market_change.csv'
    }
    for title, fname in files.items():
        path = os.path.join(phase_dir, fname)
        if not os.path.isfile(path):
            report.append(f"- **WARN**: {title} output not found at `{path}`")
            continue
        df = pd.read_csv(path)
        rows, cols = df.shape
        report.append(f"## {title} Output\n")
        report.append(f"- Rows: {rows}, Columns: {cols}\n")
        report.append(f"- Columns: {', '.join(df.columns)}\n")
        # Show first 5 rows as sample
        sample = df.head(5).to_markdown(index=False)
        report.append(f"\nSample rows (first 5):\n\n{sample}\n")
    # Write markdown
    out_path = os.path.join(phase_dir, 'task_4_4_education_profile_analysis.md')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write('\n'.join(report))

if __name__ == '__main__':
    main()
