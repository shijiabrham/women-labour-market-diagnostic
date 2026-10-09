# Dataset 1 Data Profile — Corrected Diagnostic (Task 1A Re-audit)
> Re-generated: 2026-09-24 | Source: `plfs_labour_market_outcomes_by_education_gender_area.csv`  
> Dataset 2 was NOT loaded or inspected at any stage of this audit.


## Dataset Overview
| Item | Value |
|------|-------|
| File name | `plfs_labour_market_outcomes_by_education_gender_area.csv` |
| File path | `/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic/data/raw/dataset_1/plfs_labour_market_outcomes_by_education_gender_area.csv` |
| Rows | 22,650 |
| Columns | 9 |
| Country field value | ['India'] |
| Geographical field | `State` — 36 distinct states/UTs |
| Year field | `Year` — 7 distinct PLFS-year labels |
| Indicators present | LFPR, WPR, Unemployment Rate |
| Complete-row duplicates | 0 |

## Field Inventory
| field_name                                                                                                                                | pandas_dtype   | role                          |   non_null_count |   missing_count |   missing_pct |   unique_count | example_values                                                                                                                                  |
|:------------------------------------------------------------------------------------------------------------------------------------------|:---------------|:------------------------------|-----------------:|----------------:|--------------:|---------------:|:------------------------------------------------------------------------------------------------------------------------------------------------|
| Country                                                                                                                                   | object         | identifier/dimension          |            22650 |               0 |        0      |              1 | India                                                                                                                                           |
| State                                                                                                                                     | object         | identifier/dimension          |            22650 |               0 |        0      |             36 | Andaman and Nicobar Islands; Andhra Pradesh; Arunachal Pradesh; Assam; Bihar                                                                    |
| Year                                                                                                                                      | object         | identifier/dimension          |            22650 |               0 |        0      |              7 | PLFS Year (Jul - Jun), 2023; PLFS Year (Jul - Jun), 2022; PLFS Year (Jul - Jun), 2021; PLFS Year (Jul - Jun), 2020; PLFS Year (Jul - Jun), 2019 |
| Type Of Areas                                                                                                                             | object         | identifier/dimension          |            22650 |               0 |        0      |              3 | Rural; Urban; Rural + Urban                                                                                                                     |
| Gender                                                                                                                                    | object         | identifier/dimension          |            22650 |               0 |        0      |              3 | Male; Female; Persons                                                                                                                           |
| Education Level                                                                                                                           | object         | identifier/dimension          |            22650 |               0 |        0      |             10 | Not Literate; Literate & Upto Primary; Middle; Secondary; Higher Secondary                                                                      |
| Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 | float64        | indicator/measure (numerical) |            22620 |              30 |        0.1325 |           1101 | 76.7; 87.0; 89.7; 58.8; 78.3                                                                                                                    |
| Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1        | float64        | indicator/measure (numerical) |            22620 |              30 |        0.1325 |           1100 | 76.7; 87.0; 88.0; 58.8; 71.3                                                                                                                    |
| Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1              | float64        | indicator/measure (numerical) |            22620 |              30 |        0.1325 |            731 | 0.0; 1.9; 9.0; 0.7; 35.7                                                                                                                        |

## Missing Values by Field
| field_name                                                                                                                                |   non_null_count |   missing_count |   missing_pct |
|:------------------------------------------------------------------------------------------------------------------------------------------|-----------------:|----------------:|--------------:|
| Country                                                                                                                                   |            22650 |               0 |        0      |
| State                                                                                                                                     |            22650 |               0 |        0      |
| Year                                                                                                                                      |            22650 |               0 |        0      |
| Type Of Areas                                                                                                                             |            22650 |               0 |        0      |
| Gender                                                                                                                                    |            22650 |               0 |        0      |
| Education Level                                                                                                                           |            22650 |               0 |        0      |
| Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 |            22620 |              30 |        0.1325 |
| Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1        |            22620 |              30 |        0.1325 |
| Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1              |            22620 |              30 |        0.1325 |

**Interpretation:** Missingness is confined to the three indicator columns. All five dimension/identifier fields are complete (0 missing).

## Year Field — Corrected Coverage (Check 2)
**Exact field name:** `Year`  
**Pandas dtype:** `object` (string/object — PLFS-year labels)  
**Missing values:** 0  
**Unique PLFS-year labels:** 7  
**Earliest:** `PLFS Year (Jul - Jun), 2017`  
**Latest:** `PLFS Year (Jul - Jun), 2023`

**All PLFS-year labels and record counts:**
| PLFS Year Label             |   Record Count |
|:----------------------------|---------------:|
| PLFS Year (Jul - Jun), 2017 |           3240 |
| PLFS Year (Jul - Jun), 2018 |           3240 |
| PLFS Year (Jul - Jun), 2019 |           3240 |
| PLFS Year (Jul - Jun), 2020 |           3240 |
| PLFS Year (Jul - Jun), 2021 |           3240 |
| PLFS Year (Jul - Jun), 2022 |           3210 |
| PLFS Year (Jul - Jun), 2023 |           3240 |

> **Correction from previous diagnostic:** The Year field does NOT contain simple calendar-year integers. It contains PLFS-year labels of the form `'PLFS Year (Jul - Jun), YYYY'`, covering the period **PLFS 2017 through PLFS 2023** (7 distinct survey years). The previous diagnostic incorrectly parsed this field numerically and reported only one year ('2021').

## Geographical Coverage (Check 3)
**Exact geography field:** `State`  
**Distinct states/UTs:** 36  
**'India' national aggregate present in `State` field:** False  
**Country field:** `Country` — values: ['India']

**All states/UTs and record counts:**
| State/UT                                     |   Record Count |
|:---------------------------------------------|---------------:|
| Andaman and Nicobar Islands                  |            630 |
| Andhra Pradesh                               |            630 |
| Arunachal Pradesh                            |            630 |
| Assam                                        |            630 |
| Bihar                                        |            630 |
| Chandigarh                                   |            630 |
| Chhattisgarh                                 |            630 |
| Delhi                                        |            630 |
| Goa                                          |            630 |
| Gujarat                                      |            630 |
| Haryana                                      |            630 |
| Himachal Pradesh                             |            630 |
| Jammu and Kashmir                            |            630 |
| Jharkhand                                    |            630 |
| Karnataka                                    |            630 |
| Kerala                                       |            630 |
| Ladakh                                       |            630 |
| Lakshadweep                                  |            620 |
| Madhya Pradesh                               |            630 |
| Maharashtra                                  |            630 |
| Manipur                                      |            630 |
| Meghalaya                                    |            630 |
| Mizoram                                      |            630 |
| Nagaland                                     |            630 |
| Odisha                                       |            630 |
| Puducherry                                   |            610 |
| Punjab                                       |            630 |
| Rajasthan                                    |            630 |
| Sikkim                                       |            630 |
| Tamil Nadu                                   |            630 |
| Telangana                                    |            630 |
| The Dadra and Nagar Haveli and Daman and Diu |            630 |
| Tripura                                      |            630 |
| Uttar Pradesh                                |            630 |
| Uttarakhand                                  |            630 |
| West Bengal                                  |            630 |

> National 'India' aggregate: NOT present in the State field. 'India' appears only in the `Country` field. State-level coverage only.

## Dimension Validation (Check 4)

### Gender
**Field:** `Gender` | dtype: `object` | Missing: 0
| Category   |   Record Count |
|:-----------|---------------:|
| Female     |           7550 |
| Male       |           7560 |
| Persons    |           7540 |

### Education Level
**Field:** `Education Level` | dtype: `object` | Missing: 0
| Category                    |   Record Count |
|:----------------------------|---------------:|
| All                         |           2265 |
| Diploma/ Certificate Course |           2265 |
| Graduate                    |           2265 |
| Higher Secondary            |           2265 |
| Literate & Upto Primary     |           2265 |
| Middle                      |           2265 |
| Not Literate                |           2265 |
| Post Graduate & Above       |           2265 |
| Secondary                   |           2265 |
| Secondary & Above           |           2265 |

### Type Of Areas
**Field:** `Type Of Areas` | dtype: `object` | Missing: 0
| Category      |   Record Count |
|:--------------|---------------:|
| Rural         |           7560 |
| Rural + Urban |           7530 |
| Urban         |           7560 |

## Indicator Validation (Check 5)
| Indicator                              | Exact Field Name                                                                                                                          | Data Type   |   Non-null Count |   Missing Count |   Missing % |   Zero Count |   Minimum |   Maximum |    Mean |   Median |   Below 0 |   Above 100 |
|:---------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:------------|-----------------:|----------------:|------------:|-------------:|----------:|----------:|--------:|---------:|----------:|------------:|
| Labour Force Participation Rate (LFPR) | Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 | float64     |            22620 |              30 |      0.1325 |          296 |         0 |       100 | 56.5707 |    58.7  |         0 |           0 |
| Working Population Ratio (WPR)         | Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1        | float64     |            22620 |              30 |      0.1325 |          342 |         0 |       100 | 51.2949 |    52.85 |         0 |           0 |
| Unemployment Rate                      | Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1              | float64     |            22620 |              30 |      0.1325 |         3849 |         0 |       100 |  9.0593 |     5.2  |         0 |           0 |

**Unit confirmation:** All three field names include the metadata substring `UOM:%(Percentage)), Scaling Factor:1`, confirming a **0–100 percentage scale** with scaling factor 1. No values fall below 0 or above 100.

## LFPR vs WPR Consistency Investigation (Check 6)
| Comparison | Count |
|------------|-------|
| Rows where LFPR > WPR | 18623 |
| Rows where WPR > LFPR | 1 |
| Rows where LFPR == WPR | 3996 |
| LFPR mean (all rows) | 56.5707 |
| WPR mean (all rows)  | 51.2949 |

**Mean LFPR and WPR by Gender:**
| Gender   |   Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 |   Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 |
|:---------|--------------------------------------------------------------------------------------------------------------------------------------------:|-------------------------------------------------------------------------------------------------------------------------------------:|
| Female   |                                                                                                                                      36.031 |                                                                                                                               31.063 |
| Male     |                                                                                                                                      75.894 |                                                                                                                               70.385 |
| Persons  |                                                                                                                                      57.763 |                                                                                                                               52.413 |

**Observation:** When WPR > LFPR for a given row this is potentially inconsistent with conventional labour-market definitions (LFPR ≥ WPR is expected). However, this may reflect aggregate or combined categories (e.g., 'Persons', 'All', 'Rural + Urban'). **This is flagged for further investigation.** No data has been altered.

**Sample rows where WPR > LFPR:**
| State      | Year                        | Gender   | Education Level   | Type Of Areas   |   Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 |   Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1 |
|:-----------|:----------------------------|:---------|:------------------|:----------------|--------------------------------------------------------------------------------------------------------------------------------------------:|-------------------------------------------------------------------------------------------------------------------------------------:|
| Chandigarh | PLFS Year (Jul - Jun), 2022 | Male     | Not Literate      | Rural           |                                                                                                                                           0 |                                                                                                                                  100 |

## Duplicates and Candidate Key (Check 8)
**Complete-row duplicates:** 0  
**Candidate key:** `State × Year × Gender × Education Level × Type Of Areas`  
**Duplicate combinations on candidate key:** 0  
**Unique combinations:** 22,650  
**Candidate key is unique:** True

## Structural Coverage (Check 9)

### State × Year record counts (36 States × 7 PLFS years)
| State                                        |   PLFS Year (Jul - Jun), 2017 |   PLFS Year (Jul - Jun), 2018 |   PLFS Year (Jul - Jun), 2019 |   PLFS Year (Jul - Jun), 2020 |   PLFS Year (Jul - Jun), 2021 |   PLFS Year (Jul - Jun), 2022 |   PLFS Year (Jul - Jun), 2023 |
|:---------------------------------------------|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|
| Andaman and Nicobar Islands                  |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Andhra Pradesh                               |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Arunachal Pradesh                            |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Assam                                        |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Bihar                                        |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Chandigarh                                   |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Chhattisgarh                                 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Delhi                                        |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Goa                                          |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Gujarat                                      |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Haryana                                      |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Himachal Pradesh                             |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Jammu and Kashmir                            |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Jharkhand                                    |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Karnataka                                    |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Kerala                                       |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Ladakh                                       |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Lakshadweep                                  |                            90 |                            90 |                            90 |                            90 |                            90 |                            80 |                            90 |
| Madhya Pradesh                               |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Maharashtra                                  |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Manipur                                      |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Meghalaya                                    |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Mizoram                                      |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Nagaland                                     |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Odisha                                       |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Puducherry                                   |                            90 |                            90 |                            90 |                            90 |                            90 |                            70 |                            90 |
| Punjab                                       |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Rajasthan                                    |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Sikkim                                       |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Tamil Nadu                                   |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Telangana                                    |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| The Dadra and Nagar Haveli and Daman and Diu |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Tripura                                      |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Uttar Pradesh                                |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| Uttarakhand                                  |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |
| West Bengal                                  |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |                            90 |

### Gender × Year
| Gender   |   PLFS Year (Jul - Jun), 2017 |   PLFS Year (Jul - Jun), 2018 |   PLFS Year (Jul - Jun), 2019 |   PLFS Year (Jul - Jun), 2020 |   PLFS Year (Jul - Jun), 2021 |   PLFS Year (Jul - Jun), 2022 |   PLFS Year (Jul - Jun), 2023 |
|:---------|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|
| Female   |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1070 |                          1080 |
| Male     |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |
| Persons  |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1060 |                          1080 |

### Education Level × Year
| Education Level             |   PLFS Year (Jul - Jun), 2017 |   PLFS Year (Jul - Jun), 2018 |   PLFS Year (Jul - Jun), 2019 |   PLFS Year (Jul - Jun), 2020 |   PLFS Year (Jul - Jun), 2021 |   PLFS Year (Jul - Jun), 2022 |   PLFS Year (Jul - Jun), 2023 |
|:----------------------------|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|
| All                         |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Diploma/ Certificate Course |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Graduate                    |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Higher Secondary            |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Literate & Upto Primary     |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Middle                      |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Not Literate                |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Post Graduate & Above       |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Secondary                   |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |
| Secondary & Above           |                           324 |                           324 |                           324 |                           324 |                           324 |                           321 |                           324 |

### Type Of Areas × Year
| Type Of Areas   |   PLFS Year (Jul - Jun), 2017 |   PLFS Year (Jul - Jun), 2018 |   PLFS Year (Jul - Jun), 2019 |   PLFS Year (Jul - Jun), 2020 |   PLFS Year (Jul - Jun), 2021 |   PLFS Year (Jul - Jun), 2022 |   PLFS Year (Jul - Jun), 2023 |
|:----------------|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|
| Rural           |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |
| Rural + Urban   |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1050 |                          1080 |
| Urban           |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |                          1080 |

> **PLFS 2022 structural note:** Some counts in PLFS 2022 are slightly lower (e.g., 1070 instead of 1080 for Female, 1060 for Persons, 321 instead of 324 for Education categories, 1050 for Rural + Urban). This asymmetry should be investigated — it may reflect legitimate data availability or a data completeness issue for that year.

## Category Interpretation (Check 10)
The following categories are observed in the raw data and recorded as-is. Their exact definitional scope should be confirmed from the PLFS documentation.
| Field | Category | Observation |
|-------|----------|-------------|
| Gender | `Persons` | Likely an aggregate across Male + Female; definitional scope to be confirmed |
| Education Level | `All` | Likely an aggregate across all education categories; to be confirmed |
| Education Level | `Secondary & Above` | Likely an aggregate group; overlaps with specific secondary categories |
| Type Of Areas | `Rural + Urban` | Likely combined (national) aggregate; to be confirmed |

## Candidate Analytical Key
**Key:** `State × Year × Gender × Education Level × Type Of Areas`  
**Duplicate combinations:** 0  
**Unique combinations:** 22,650  
**Result:** The candidate key is **unique** — each row is distinguishable by this 5-dimension combination.

## Dataset 1 Analytical Scope
**Dimensions available:** State (36), PLFS Year (7: 2017–2023), Gender (3), Education Level (10), Type Of Areas (3).

**Comparisons Dataset 1 can potentially support:**
- LFPR / WPR / Unemployment Rate by Gender across PLFS years
- LFPR / WPR / Unemployment Rate by Education Level across PLFS years
- Rural vs Urban vs Rural+Urban comparisons for all three indicators
- State-level variation in indicators across years
- Trend analysis across 7 PLFS years (2017–2023)

**What Dataset 1 cannot establish by itself:**
- Industry or enterprise-type breakdowns (requires Dataset 2)
- Absolute employment numbers (Dataset 1 reports rates, not headcounts)
- Causal factors behind trends