# Dataset 1 Technical Cleaning Log

- Loading raw CSV from /Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic/data/raw/dataset_1/plfs_labour_market_outcomes_by_education_gender_area.csv
- Loaded 22,650 rows and 9 columns.
- Column 'Country': trimmed whitespace from 0 entries.
- Column 'State': trimmed whitespace from 0 entries.
- Column 'Year': trimmed whitespace from 0 entries.
- Column 'Type Of Areas': trimmed whitespace from 0 entries.
- Column 'Gender': trimmed whitespace from 0 entries.
- Column 'Education Level': trimmed whitespace from 0 entries.
- Column 'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': converted to numeric, introduced 30 NaNs (including blanks and malformed values).
- Column 'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': converted to numeric, introduced 30 NaNs (including blanks and malformed values).
- Column 'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': converted to numeric, introduced 30 NaNs (including blanks and malformed values).
- Column 'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1' had 1 original non‑numeric entries (e.g., ['nan']...).
- Column 'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1' had 1 original non‑numeric entries (e.g., ['nan']...).
- Column 'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1' had 1 original non‑numeric entries (e.g., ['nan']...).
- Saved cleaned dataset to /Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic/outputs/dataset_1_profile/cleaned_dataset_1.csv.
