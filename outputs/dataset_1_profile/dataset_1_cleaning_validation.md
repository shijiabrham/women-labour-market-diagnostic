# Dataset 1 Cleaning Validation Report

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Row count | Expected: 22650 | Actual: 22650 | PASS |
| Column count | Expected: 9 | Actual: 9 | PASS |
| Column names/order | Expected: ['Country', 'State', 'Year', 'Type Of Areas', 'Gender', 'Education Level', 'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1', 'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1', 'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1'] | Actual: ['Country', 'State', 'Year', 'Type Of Areas', 'Gender', 'Education Level', 'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1', 'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1', 'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1'] | PASS |
| Category sets (State,Year,Gender,Education Level,Type Of Areas) | Expected: identical | Actual: identical | PASS |
| Year coverage | Expected: {'PLFS Year (Jul - Jun), 2018', 'PLFS Year (Jul - Jun), 2021', 'PLFS Year (Jul - Jun), 2017', 'PLFS Year (Jul - Jun), 2019', 'PLFS Year (Jul - Jun), 2023', 'PLFS Year (Jul - Jun), 2020', 'PLFS Year (Jul - Jun), 2022'} | Actual: {'PLFS Year (Jul - Jun), 2018', 'PLFS Year (Jul - Jun), 2021', 'PLFS Year (Jul - Jun), 2017', 'PLFS Year (Jul - Jun), 2019', 'PLFS Year (Jul - Jun), 2023', 'PLFS Year (Jul - Jun), 2020', 'PLFS Year (Jul - Jun), 2022'} | PASS |
| Missing Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 | Expected: 30 | Actual: 30 | PASS |
| Missing Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 | Expected: 30 | Actual: 30 | PASS |
| Missing Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 | Expected: 30 | Actual: 30 | PASS |
| Duplicate rows (cleaned) | Expected: 0 | Actual: 0 | PASS |
| Numeric values unchanged | Expected: yes | Actual: yes | PASS |

Task 1B Dataset 1 cleaning validation: **PASS**.
