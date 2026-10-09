#!/usr/bin/env python3
"""
q12_state_area_unemployment_validation.py

Validate the Q12 Unemployment CSV without external dependencies.
Writes a markdown report (PASS/FAIL) to the validation file.
"""
import os, csv

def main():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q12_state_area_unemployment.csv"))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q12_state_area_unemployment_validation.md"))
    expected_cols = ["Country", "State", "Area_Type", "Year", "Unemployment_Rate", "Missing_Count", "All_Years"]
    report = []
    if not os.path.isfile(csv_path):
        report.append(f"- **FAIL**: File not found at `{csv_path}`")
    else:
        with open(csv_path, newline='') as f:
            rows = list(csv.reader(f))
        header = rows[0]
        data = rows[1:]
        if header != expected_cols:
            report.append(f"- **FAIL**: Columns mismatch. Expected {expected_cols}, got {header}")
        else:
            report.append("- **PASS**: Column order correct.")
        expected_rows = 36 * 3 * 8
        if len(data) != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows}, got {len(data)}")
        else:
            report.append("- **PASS**: Row count correct.")
        agg_count = sum(1 for r in data if r[6].strip().lower() in ("true", "1"))
        if agg_count != 36 * 3:
            report.append(f"- **FAIL**: Unexpected number of aggregate rows. Expected {36*3}, got {agg_count}")
        else:
            report.append("- **PASS**: Aggregate rows count correct.")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("# Q12 Unemployment Rate Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == "__main__":
    main()
