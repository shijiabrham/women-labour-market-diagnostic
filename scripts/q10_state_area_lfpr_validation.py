#!/usr/bin/env python3
"""
q10_state_area_lfpr_validation.py

Validate the Q10 LFPR CSV against the source dataset's actual State × Area_Type coverage.
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
    # Paths
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q10_state_area_lfpr.csv"))
    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv"))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "phase_4_eda", "q10_state_area_lfpr_validation.md"))
    expected_cols = ["Country", "State", "Area_Type", "Year", "LFPR", "Missing_Count", "All_Years"]
    report = []
    # Load source coverage
    source_combos = get_source_coverage(source_path)
    expected_rows = len(source_combos) * 8  # 7 years + All_Years per combo
    # Validate CSV existence
    if not os.path.isfile(csv_path):
        report.append(f"- **FAIL**: Q10 CSV not found at `{csv_path}`")
    else:
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        header = rows[0]
        data_rows = rows[1:]
        # Column check
        if header != expected_cols:
            report.append(f"- **FAIL**: Column mismatch. Expected {expected_cols}, got {header}")
        else:
            report.append("- **PASS**: Column order correct.")
        # Row count check
        if len(data_rows) != expected_rows:
            report.append(f"- **FAIL**: Row count mismatch. Expected {expected_rows} (based on actual source combos), got {len(data_rows)}")
        else:
            report.append("- **PASS**: Row count matches actual source coverage.")
        # Check for any combos missing in CSV
        csv_combos = set()
        for row in data_rows:
            state, area = row[1], row[2]
            csv_combos.add((state, area))
        missing_combos = source_combos - csv_combos
        extra_combos = csv_combos - source_combos
        if missing_combos:
            report.append(f"- **FAIL**: Missing State/Area combos in Q10: {sorted(missing_combos)}")
        else:
            report.append("- **PASS**: No missing State/Area combos.")
        if extra_combos:
            report.append(f"- **FAIL**: Unexpected extra State/Area combos in Q10: {sorted(extra_combos)}")
        else:
            report.append("- **PASS**: No unexpected combos.")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("# Q10 LFPR Validation Report\n\n")
        f.write("\n".join(report))
        f.write("\n")

if __name__ == "__main__":
    main()
