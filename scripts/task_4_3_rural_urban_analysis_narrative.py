#!/usr/bin/env python3
"""
task_4_3_rural_urban_analysis_narrative.py

Generate the final Task 4.3 narrative markdown.
It reads the Q10‑Q13 CSVs, extracts first 10 rows, counts, coverage diagnostic (captured from stdout of the diagnostic script), and writes a markdown report.
"""
import pandas as pd, subprocess, os, sys

def read_csv_summary(csv_path, n=10):
    df = pd.read_csv(csv_path)
    header = list(df.columns)
    rows = df.head(n).to_csv(index=False, line_terminator='\n')
    return header, rows, len(df), len(df.columns)

def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda"))
    files = {
        "Q10 LFPR": os.path.join(base, "q10_state_area_lfpr.csv"),
        "Q11 WPR": os.path.join(base, "q11_state_area_wpr.csv"),
        "Q12 Unemployment": os.path.join(base, "q12_state_area_unemployment.csv"),
        "Q13 Change": os.path.join(base, "q13_state_area_labour_market_change.csv"),
    }
    report_lines = ["# Task 4.3 – Rural‑Urban Labour‑Market Profile\n"]
    # Run the coverage diagnostic and capture its stdout
    diag_cmd = ["python3", "scripts/area_type_coverage_diagnostic.py"]
    try:
        diag_output = subprocess.check_output(diag_cmd, cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), text=True)
        report_lines.append("## Area‑Type Coverage Diagnostic\n")
        report_lines.append("```")
        report_lines.append(diag_output.strip())
        report_lines.append("```")
    except Exception as e:
        report_lines.append(f"*Failed to run coverage diagnostic: {e}*")
    # For each CSV, add summary
    for title, path in files.items():
        if not os.path.isfile(path):
            report_lines.append(f"## {title}\n*File not found: {path}*\n")
            continue
        header, rows, row_cnt, col_cnt = read_csv_summary(path)
        report_lines.append(f"## {title}\n")
        report_lines.append(f"- Path: `{path}`\n- Rows: {row_cnt}\n- Columns: {col_cnt}\n- Columns list: {', '.join(header)}\n")
        report_lines.append("### First 10 rows\n")
        report_lines.append("```")
        report_lines.append(rows.strip())
        report_lines.append("```)\n")
    # Write markdown
    out_path = os.path.abspath(os.path.join(base, "task_4_3_rural_urban_analysis.md"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(report_lines))
    print(f"Narrative written to {out_path}")

if __name__ == "__main__":
    main()
