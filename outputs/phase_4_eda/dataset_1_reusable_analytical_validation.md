# Dataset 1 Reusable Analytical Layer — Validation Report

## Summary

- **File**: `outputs/phase_4_eda/dataset_1_reusable_analytical.csv`
- **Total validation checks**: 43
- **PASS**: 43
- **FAIL**: 0
- **Overall status**: **PASS**

## Validation Checks

| Check ID | Description | Expected | Actual | Status |
|----------|-------------|----------|--------|--------|
| A1 | File exists | True | True | **PASS** |
| A2 | Column names correct | ['State', 'Year', 'Gender', 'Area_Type', 'Education', 'LFPR', 'WPR', 'Unemployment_Rate'] | ['State', 'Year', 'Gender', 'Area_Type', 'Education', 'LFPR', 'WPR', 'Unemployment_Rate'] | **PASS** |
| A3 | Column count | 8 | 8 | **PASS** |
| A4 | No unexpected columns | [] | [] | **PASS** |
| B1 | Row count = unique 5-dim source combos | 22650 | 22650 | **PASS** |
| C1 | Zero duplicate 5-dim keys | 0 duplicates | 0 duplicates | **PASS** |
| D1 | States | ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'The Dadra and Nagar Haveli and Daman and Diu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'] | ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'The Dadra and Nagar Haveli and Daman and Diu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'] | **PASS** |
| D2 | Years | [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)] | [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)] | **PASS** |
| D3 | Gender | ['Female', 'Male', 'Persons'] | ['Female', 'Male', 'Persons'] | **PASS** |
| D4 | Area_Type | ['Rural', 'Rural + Urban', 'Urban'] | ['Rural', 'Rural + Urban', 'Urban'] | **PASS** |
| D5 | Education | ['All', 'Diploma/ Certificate Course', 'Graduate', 'Higher Secondary', 'Literate & Upto Primary', 'Middle', 'Not Literate', 'Post Graduate & Above', 'Secondary', 'Secondary & Above'] | ['All', 'Diploma/ Certificate Course', 'Graduate', 'Higher Secondary', 'Literate & Upto Primary', 'Middle', 'Not Literate', 'Post Graduate & Above', 'Secondary', 'Secondary & Above'] | **PASS** |
| D6 | No source combos silently removed | 0 removed | 0 removed | **PASS** |
| E1 | Missing State×Year×Gender×Area combos not fabricated | 3 missing in source | 3 missing in output | **PASS** |
| F1 | LFPR values preserved | All match | All match | **PASS** |
| F2 | WPR values preserved | All match | All match | **PASS** |
| F3 | Unemployment_Rate values preserved | All match | All match | **PASS** |
| F4 | LFPR missing count | 30 | 30 | **PASS** |
| F5 | WPR missing count | 30 | 30 | **PASS** |
| F6 | UR missing count | 30 | 30 | **PASS** |
| G-All | Aggregate category 'All' present | All | All | **PASS** |
| G-Sec | Aggregate category 'Secondary & Above' present | Secondary & Above | Secondary & Above | **PASS** |
| G-Not | Detailed category 'Not Literate' present | Not Literate | Not Literate | **PASS** |
| G-Lit | Detailed category 'Literate & Upto Primary' present | Literate & Upto Primary | Literate & Upto Primary | **PASS** |
| G-Mid | Detailed category 'Middle' present | Middle | Middle | **PASS** |
| G-Sec | Detailed category 'Secondary' present | Secondary | Secondary | **PASS** |
| G-Hig | Detailed category 'Higher Secondary' present | Higher Secondary | Higher Secondary | **PASS** |
| G-Dip | Detailed category 'Diploma/ Certificate Course' present | Diploma/ Certificate Course | Diploma/ Certificate Course | **PASS** |
| G-Gra | Detailed category 'Graduate' present | Graduate | Graduate | **PASS** |
| G-Pos | Detailed category 'Post Graduate & Above' present | Post Graduate & Above | Post Graduate & Above | **PASS** |
| H1 | Female present | Female | Female | **PASS** |
| H2 | Male present | Male | Male | **PASS** |
| H3 | Persons present | Persons | Persons | **PASS** |
| I1 | Rural present | Rural | Rural | **PASS** |
| I2 | Urban present | Urban | Urban | **PASS** |
| I3 | Rural + Urban present | Rural + Urban | Rural + Urban | **PASS** |
| J1 | Years 2017-2023 all present | [2017, 2018, 2019, 2020, 2021, 2022, 2023] | [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)] | **PASS** |
| K1 | No unintended education categories | 0 extra | 0 | **PASS** |
| K2 | No unintended gender categories | 0 extra | 0 | **PASS** |
| K3 | No unintended area categories | 0 extra | 0 | **PASS** |
| L1 | Source dataset hash stable (not modified during this run) | 452c3bdacd29711f963925db04d5b789 | 452c3bdacd29711f963925db04d5b789 | **PASS** |
| L2 | Q1-Q17 scripts not opened for writing (31 present) | No write | No write | **PASS** |
| L3 | Q1-Q17 CSVs not opened for writing (18 present) | No write | No write | **PASS** |
| L4 | Q1-Q17 MDs not opened for writing (21 present) | No write | No write | **PASS** |

## Coverage Detail

| Dimension | Values |
|-----------|--------|
| States | 36 |
| Years | 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| Gender | Female, Male, Persons |
| Area_Type | Rural, Rural + Urban, Urban |
| Education (detailed) | Not Literate, Literate & Upto Primary, Middle, Secondary, Higher Secondary, Diploma/ Certificate Course, Graduate, Post Graduate & Above |
| Education (aggregate) | All, Secondary & Above |

## Missing Dimensional Combinations (from audit, preserved not fabricated)

- Missing State × Year × Gender × Area_Type combos: 3
  - ('Lakshadweep', np.int64(2022), 'Persons', 'Rural + Urban')
  - ('Puducherry', np.int64(2022), 'Female', 'Rural + Urban')
  - ('Puducherry', np.int64(2022), 'Persons', 'Rural + Urban')

## Indicator Missingness

| Indicator | Missing rows | % |
|-----------|-------------|---|
| LFPR | 30 | 0.13% |
| WPR | 30 | 0.13% |
| Unemployment_Rate | 30 | 0.13% |

All missing values are preserved as NaN from the source; none were imputed or replaced with zero.

## Integrity Check

- Source dataset MD5: `452c3bdacd29711f963925db04d5b789` — not modified during this run.
- Q1–Q17 scripts checked: 31 (none opened for writing)
- Q1–Q17 CSVs checked:    18 (none opened for writing)
- Q1–Q17 MDs checked:     21 (none opened for writing)

## Reusable Analytical Architecture — Documented Rules

### Base grain
```
State × Year × Gender × Area_Type × Education
```
One row per unique combination. No aggregation within the base layer.

### Indicator mapping
| Output column | Source column (shortened) |
|--------------|--------------------------|
| LFPR | Labor Force Participation Rate … Scaling Factor:1 |
| WPR | Working Population Rate … Scaling Factor:1 |
| Unemployment_Rate | Unemployment Rate … Scaling Factor:1 |

### Category preservation rules
- `Persons` is an existing source category. Do **not** derive it from Female + Male.
- `Rural + Urban` is an existing source category. Do **not** reconstruct from Rural and Urban.
- `All` (Education) is an existing source aggregate. Do **not** reconstruct from detailed categories.
- `Secondary & Above` (Education) is an existing source aggregate. Do **not** reconstruct.

### Aggregation rule (for future question-specific views only)
- When a dimension is collapsed for a specific analytical view, use **arithmetic mean** of available non-missing indicator values.
- Missing values (NaN) are excluded from the mean; if all values are missing the result is NaN.
- Zero values are valid observations and are included in the mean.
- No population weights exist in Dataset 1; the mean is an **unweighted analytical aggregation**, not a population-weighted estimate.

### Dynamic computations (never stored permanently in the base layer)
- Female–Male Gap = Female value − Male value (computed at query time)
- Rural–Urban Gap = Rural value − Urban value (computed at query time)
- Absolute Change = value(2023) − value(2017) (computed at query time)
- Percentage Change = (Absolute Change / value(2017)) × 100 (computed at query time)
- Year-on-Year Change = value(Year) − value(Year−1) (computed at query time)

### Architecture flow
```
Dataset 1 feature-engineered source
    ↓
dataset_1_reusable_analytical.csv  (stable base layer)
    ↓
Select Indicator (LFPR / WPR / Unemployment_Rate)
    ↓
Apply filters (Gender, Area_Type, Education, State, Year)
    ↓
Select analytical dimensions (group-by)
    ↓
Aggregate where required (arithmetic mean, NaN-aware)
    ↓
Calculate gap / change where required (dynamic)
    ↓
Analytical result → table / chart / narrative
```

## Protection of Q1–Q17

Existing Q1–Q17 scripts, CSV outputs, validation reports, and narratives were **not modified, regenerated, or overwritten** during this task.
The reusable analytical layer is an additional, independent data source for future analysis.

---
*Validation report generated automatically.*