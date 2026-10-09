# Implementation Plan – Task 4.4 Education Profile

## Goal Description
Analyze women's labour‑market outcomes by education level using Dataset 1. Produce Q14‑Q17 outputs, validation reports, and a narrative that includes diagnostics of education categories, coverage, and sample rows.

## User Review Required
[!IMPORTANT]
- The plan creates new analysis scripts (`q14_state_education_lfpr.py`, `q15_state_education_wpr.py`, `q16_state_education_unemployment.py`, `q17_state_education_labour_market_change.py`) and corresponding validation scripts.
- No existing Q5‑Q13 files will be modified.
- The eight detailed education categories are treated as the progression; `Secondary & Above` and `All` remain separate aggregate categories.
- Q14‑Q16 perform mean aggregation per State × Education × Year, preserving missing counts.
- Q17 computes changes using the regenerated Q14‑Q16 outputs.

## Open Questions
[!WARNING]
- None; the specifications are complete.

## Proposed Changes
---
### New Analysis Scripts
#### [NEW] `scripts/q14_state_education_lfpr.py`
- Load `outputs/dataset_1_profile/feature_engineered_dataset_1.csv`.
- Filter rows where `Gender == Female`.
- Identify the education column (`Education Level`).
- Aggregate LFPR (column `Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`) by `State`, `Education`, `Year` using mean.
- Compute `Missing_Count` per group.
- Append an `All_Years` row per `State` × `Education` (mean across years).
- Output CSV `outputs/phase_4_eda/q14_state_education_lfpr.csv` with columns:
  `Country,State,Education,Year,LFPR,Missing_Count,All_Years`.

#### [NEW] `scripts/q15_state_education_wpr.py`
- Same workflow as Q14 but for the WPR column `Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`.

#### [NEW] `scripts/q16_state_education_unemployment.py`
- Same workflow as Q14 but for the unemployment column `Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`.

#### [NEW] `scripts/q17_state_education_labour_market_change.py`
- Load the three Q14‑Q16 CSVs.
- Pivot each to have `Value_2017` and `Value_2023` columns for each `State` × `Education`.
- Merge the three pivoted tables on `Country`, `State`, `Education`.
- For each indicator compute:
  - `Absolute_Change = Value_2023 - Value_2017`
  - `Percentage_Change = ((Value_2023 - Value_2017) / Value_2017) * 100` (null if `Value_2017` is 0 or missing).
- Preserve `Missing_Count_2017` and `Missing_Count_2023` from the source CSVs.
- Output CSV `outputs/phase_4_eda/q17_state_education_labour_market_change.csv` with columns in this order:
  `Country,State,Education,Indicator,Value_2017,Value_2023,Absolute_Change,Percentage_Change,Missing_Count_2017,Missing_Count_2023`.

### New Validation Scripts
#### [NEW] `scripts/q14_state_education_lfpr_validation.py`
- Verify column names and order.
- Determine actual `State × Education` combos from the source after filtering gender.
- Expected rows = combos × years (2017‑2023) + combos (All_Years aggregates).
- Check uniqueness of `State × Education × Year`.
- Ensure missing‑count column exists and three‑decimal rounding.
- Write markdown report `outputs/phase_4_eda/q14_state_education_lfpr_validation.md`.

#### [NEW] `scripts/q15_state_education_wpr_validation.py`
- Same checks for the WPR output.

#### [NEW] `scripts/q16_state_education_unemployment_validation.py`
- Same checks for the unemployment output.

#### [NEW] `scripts/q17_state_education_labour_market_change_validation.py`
- Verify column order includes the endpoint columns.
- Expected rows = combos × 3 indicators (no yearly rows).
- Cross‑check `Value_2017`/`Value_2023` against the corresponding Q14‑Q16 CSVs.
- Validate `Absolute_Change` and `Percentage_Change` calculations, including zero‑division handling.
- Report PASS/FAIL in `outputs/phase_4_eda/q17_state_education_labour_market_change_validation.md`.

### Narrative Script
#### [NEW] `scripts/task_4_4_education_profile_analysis_narrative.py`
- Perform the **education‑category diagnostic**:
  * Identify the exact education column name.
  * List all unique education categories (both detailed and aggregate).
  * Count detailed categories (expected eight).
  * Confirm presence/absence of `Secondary & Above` and `All`.
  * Report year‑wise coverage for each category (2017‑2023).
  * Report State × Education combos present.
  * Detect missing or duplicate `State × Education × Year` observations.
- Summarize diagnostic results.
- Append first 10 rows of each Q14‑Q17 CSV.
- Include row and column counts for each output.
- Clearly separate the eight detailed categories from the two aggregates.
- Write markdown to `outputs/phase_4_eda/task_4_4_education_profile_analysis.md`.

### Execution Order (as requested)
1. Run the education‑category diagnostic (embedded in the narrative script).
2. Generate Q14 output → validate Q14.
3. Generate Q15 output → validate Q15.
4. Generate Q16 output → validate Q16.
5. Generate Q17 output using Q14‑Q16 → validate Q17.
6. Generate the narrative markdown.
7. Stop and present diagnostics, sample rows, and validation reports.

## Verification Plan
- After each script execution, its validation markdown will be inspected for PASS/FAIL.
- The narrative will be reviewed to ensure it contains all required diagnostics, sample rows, and counts.
- No modifications will be made to any protected Q5‑Q13 files.
---
**Please review this implementation plan and confirm to proceed.**
