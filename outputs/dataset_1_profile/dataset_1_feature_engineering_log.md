# Dataset 1 Feature Engineering Log

## Features created
- `Year_Numeric`: integer extracted from `Year`.
- `Female_Flag`: 1 for Female, 0 for Male/Persons.
- `Education_Level_Order`: ordinal mapping of detailed education levels; aggregate categories set to NaN.
- `Education_Category_Type`: "Detailed" for the eight detailed levels, "Aggregate" for "Secondary & Above" and "All".
- `Indicator_Availability_Flag`: 1 when LFPR, WPR and Unemployment Rate are all present, else 0.

## Validation results
- Row count unchanged (22,650): PASS
- Original 9 columns unchanged: PASS
- Education_Level_Order contains 8 distinct ordered values: PASS
- Aggregate categories correctly labelled: PASS
- Existing missing‑indicator rows (all three indicators missing) count = 30: PASS
- No unexpected missing values in new features: PASS

All checks passed; feature‑engineered dataset written to:
- `/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic/outputs/dataset_1_profile/feature_engineered_dataset_1.csv`