#!/usr/bin/env python3
"""
Area-Type Coverage Diagnostic (no pandas).
Prints a table of each State and which Area_Type categories are present in the female subset of the dataset.
"""
import csv, os, sys

def main():
    # Path to source dataset
    data_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "dataset_1_profile", "feature_engineered_dataset_1.csv")
    if not os.path.isfile(data_path):
        print(f"Source dataset not found at {data_path}")
        sys.exit(1)
    combos = {}
    with open(data_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Gender') != 'Female':
                continue
            state = row.get('State')
            area = row.get('Type Of Areas')
            if not state or not area:
                continue
            combos.setdefault(state, set()).add(area)
    # Print diagnostic
    print("Area‑Type Coverage Diagnostic (Female observations)")
    print("State\tArea_Types")
    for state in sorted(combos):
        types = ", ".join(sorted(combos[state]))
        print(f"{state}\t{types}")

if __name__ == "__main__":
    main()
