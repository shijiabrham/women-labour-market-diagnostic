# Implementation Plan – Q9 State‑Level Labour‑Market Pattern Analysis

## Goal Description
Analyse descriptive labour‑market patterns across Indian States/UTs using the validated results from Q5 (LFPR), Q6 (WPR), Q7 (Unemployment Rate) and Q8 (LFPR change 2017‑2023). No rankings, performance labels, or composite scores will be produced. The output will be:
- `outputs/phase_4_eda/q9_state_labour_market_patterns.csv` – consolidated state‑level table with all indicators and pattern group assignments.
- `outputs/phase_4_eda/q9_state_labour_market_patterns_validation.md` – independent validation against source Q5‑Q8 files.
- `outputs/phase_4_eda/q9_state_labour_market_patterns_analysis.md` – narrative summary of observed patterns, data limitations, and exploratory associations.

## User Review Required
- **Result CSV name** (default above). Please confirm or suggest an alternative.
- **Pattern‑group column names** to be added to the result CSV (e.g., `LFPR_WPR_Pattern_Group`, `LFPR_Unemployment_Pattern_Group`, `LFPR_Change_Pattern_Group`). Confirm if these are acceptable.
- **Number of groups**: we propose using median‑split based categories (above/below median) for each pairwise comparison, and three‑tier for LFPR change (increase, decrease, stable). If you prefer different thresholds, let us know.

> [!IMPORTANT] Please approve the filenames, column names, and grouping methodology before we proceed.

## Open Questions
1. Should we include a numeric *group index* (e.g., 1/2) or keep only the textual descriptor?
2. For the LFPR change pattern, do you want a separate “stable” category (absolute change ≤ 0.1 percentage‑points) or just “increase”/“decrease”?
3. Do you want the result CSV to retain the original alphabetical ordering of states, or any other ordering? (No ranking will be implied.)

## Proposed Changes & Workflow
---
### 1. Verify source files exist and can be read
- Check existence of the four validated CSVs (`q5_dataset_1_eda_result.csv`, `q6_dataset_1_eda_result.csv`, `q7_state_unemployment_rate.csv`, `q8_state_lfpr_change.csv`).
- Load each with the standard `csv.DictReader` (no external libraries).

### 2. Confirm consistent State/UT coverage
- Extract the set of State names from each file.
- Ensure all four sets contain exactly the 36 States/UTs.
- Report any mismatches as an error (stop for review).

### 3. Consolidate data
Create a master table with one row per State containing:
| State | LFPR_All_Years | WPR_All_Years | Unemp_All_Years | LFPR_2017 | LFPR_2023 | LFPR_Absolute_Change | LFPR_Percentage_Change | LFPR_Valid_2017_Obs | LFPR_Valid_2023_Obs | LFPR_Missing_2017_Count | LFPR_Missing_2023_Count |
Values are taken directly from the respective result files (already rounded to three decimals). Missing counts are taken from Q8.

### 4. Descriptive statistics (distribution)
- Compute mean, median, min, max, and inter‑quartile range for each numeric column across the 36 states (using simple Python arithmetic).
- Store these stats for inclusion in the validation markdown.

### 5. Correlation (exploratory association)
- Compute Pearson correlation coefficients for:
  - LFPR vs WPR
  - LFPR vs Unemployment Rate
  - WPR vs Unemployment Rate
  - LFPR_2017 vs LFPR_2023
  - LFPR_Absolute_Change vs WPR
These correlations will be reported strictly as exploratory descriptive associations; no inference of causality or statistical significance will be claimed.

### 6. Pattern grouping methodology
**a. LFPR‑WPR pattern**
- Compute median of `LFPR_All_Years` and median of `WPR_All_Years` across states.
- Assign each state to one of four descriptive categories:
  1. **Above-median LFPR / Above-median WPR** (both ≥ median)
  2. **Above-median LFPR / Below-median WPR** (LFPR ≥ median, WPR < median)
  3. **Below-median LFPR / Above-median WPR** (LFPR < median, WPR ≥ median)
  4. **Below-median LFPR / Below-median WPR** (both < median)
- Column name: `LFPR_WPR_Pattern_Group`.

**b. LFPR‑Unemployment pattern**
- Use the same LFPR median split and median of `Unemp_All_Years`.
- Four categories analogous to (a) with column name `LFPR_Unemployment_Pattern_Group`.

**c. LFPR change pattern**
- Define three categories based on `LFPR_Absolute_Change`:
  - **Increase**: absolute change > 0.1 pp
  - **Decrease**: absolute change < -0.1 pp
  - **Stable**: -0.1 ≤ change ≤ 0.1 pp
- Column name: `LFPR_Change_Pattern_Group`.
All thresholds are transparent and data‑derived; they will be documented in the validation markdown.

### 7. Identify meaningful pattern observations
- Review the resulting pattern groups and note any combinations that appear across multiple states and differ from the most common combination in the dataset.
- Report the observation for Chandigarh explicitly as a data limitation: the 2023 LFPR is missing, so no pattern assignment is made for this state.
- No language describing states as high‑performing, low‑performing, best, worst, etc., will be used.

### 8. Write result CSV
- Columns (in this order):
```
State,LFPR_All_Years,WPR_All_Years,Unemployment_Rate_All_Years,LFPR_2017,LFPR_2023,LFPR_Absolute_Change,LFPR_Percentage_Change,LFPR_Valid_2017_Obs,LFPR_Valid_2023_Obs,LFPR_Missing_2017_Count,LFPR_Missing_2023_Count,LFPR_WPR_Pattern_Group,LFPR_Unemployment_Pattern_Group,LFPR_Change_Pattern_Group
```
- Values are written as strings; numeric columns retain three‑decimal rounding.
- File path: `outputs/phase_4_eda/q9_state_labour_market_patterns.csv`.

### 9. Validation script
- Re‑load the four source CSVs and recompute every column of the result CSV (including pattern assignments) directly.
- Use tolerance ≤ 1e‑6 for numeric comparisons (after rounding to three decimals).
- Verify that no state is omitted, that missing counts match, and that pattern assignments follow the described methodology.
- Produce a markdown report (`q9_state_labour_market_patterns_validation.md`) with:
  * Overall PASS/FAIL.
  * Any mismatched rows or columns.
  * Summary of descriptive statistics and correlations (to show they were computed correctly).

### 10. Narrative analysis markdown
- Summarize the major observable patterns, e.g.:
  * Typical relationship between LFPR and WPR (e.g., many states show both above‑median or both below‑median values).
  * Typical relationship between LFPR and unemployment (e.g., many states show above‑median LFPR with above‑median unemployment).
  * Distribution of LFPR change (overall increase, notable decreases, stable cases).
  * Explicit note that Chandigarh’s 2023 LFPR is missing, representing a data limitation.
- Language will remain descriptive and avoid any performance ranking or causal claims.
- File path: `outputs/phase_4_eda/q9_state_labour_market_patterns_analysis.md`.

### 11. Sample output for review (pre‑finalisation)
- Print to stdout the first ten rows of the consolidated table (alphabetical order).
- Print the descriptive distribution statistics, correlation coefficients, and a concise summary of identified pattern groups with counts.
- Print the validation PASS/FAIL status.

### 12. Execution Plan
1. After your approval of filenames, column names, and grouping methodology, we will:
   - Write the consolidation script (`scripts/q9_consolidate_patterns.py`).
   - Write the validation script (`scripts/q9_consolidate_patterns_validation.py`).
   - Write the narrative analysis script (`scripts/q9_analysis_narrative.py`).
2. Execute the consolidation script to produce the result CSV and sample output.
3. Execute the validation script; ensure PASS.
4. Execute the narrative script to generate the analysis markdown.
5. Present the sample output, validation summary, and narrative for final sign‑off.
6. Mark the task complete.

---
**STOP** – Await your confirmation before any code is written or executed.
