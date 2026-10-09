#!/usr/bin/env python3
"""
q11_state_area_wpr_validation.py

Validate the Q11 WPR CSV against the source dataset's actual State × Area_Type coverage.
Writes a markdown report (PASS/FAIL) to the validation file.
"""
import os, csv

def get_source_coverage(source_path):
    combos = set()
    with open(source_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Gender') != 'Female':
                continue
            state = row.get('State')
            area = row.get('Type Of Areas')
            if state and area:
                combos.add((state, area))
    return combos

def main():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q11_state_area_wpr.csv"))
    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv"))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q11_state_area_wpr_validation.md"))
    expected_cols = ["Country", "State", "Area_Type", "Year", "WPR", "Missing_Count", "All_Years"]
    report = []
    source_combos = get_source_coverage(source_path)
    expected_rows = len(source_combos) * 8
    if not os.path.isfile(csv_path):
        report.append(f"- **FAIL**: Q11 CSV not found at `{csv_path}`")
    else:
        with open(csv_path, newline='') as f:
            rows = list(csv.reader(f))
        header = rows[0]
        data_rows = rows[1:]
        if header != expected_cols:
            report.append(f"- **FAIL**: Column mismatch. Expected {expected_cols}, got {header}")
        else:
            report.append("- **PASS**: Column order correct.")
        if len(data_rows) != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows} (based on actual source combos), got {len(data_rows)}")
        else:
            report.append("- **PASS**: Row count matches actual source coverage.")
        csv_combos = set((row[1], row[2]) for row in data_rows)
        missing = source_combos - csv_combos
        extra = csv_combos - source_combos
        if missing:
            report.append(f"- **FAIL**: Missing State/Area combos in Q11: {sorted(missing)}")
        else:
            report.append("- **PASS**: No missing State/Area combos.")
        if extra:
            report.append(f"- **FAIL**: Unexpected extra State/Area combos in Q11: {sorted(extra)}")
        else:
            report.append("- **PASS**: No unexpected combos.")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("# Q11 WPR Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == "__main__":
    main()
