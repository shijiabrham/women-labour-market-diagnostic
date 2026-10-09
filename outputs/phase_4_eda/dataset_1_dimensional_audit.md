# Dataset 1 Dimensional Audit

## 1. Source Dataset Information
- Path: `/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic/outputs/dataset_1_profile/feature_engineered_dataset_1.csv`
- Rows: 22650
- Columns: 14
- Column names:
  - `Country`
  - `State`
  - `Year`
  - `Type Of Areas`
  - `Gender`
  - `Education Level`
  - `Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`
  - `Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`
  - `Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`
  - `Year_Numeric`
  - `Female_Flag`
  - `Education_Level_Order`
  - `Education_Category_Type`
  - `Indicator_Availability_Flag`
- Dataset type: Feature‑engineered Dataset 1 (derived from raw Dataset 1)
- No additional preprocessing applied for this audit.

## 2. Column Mapping
- State: `State`
- Year (raw): `Year` → numeric `YearNum`
- Gender: `Gender`
- Area Type: `Type Of Areas`
- Education Level: `Education Level`
- LFPR: `Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`
- WPR: `Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`
- Unemployment Rate: `Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1`

## 3. Gender Diagnostic
| Gender | Row count | States covered | Years covered |
|--------|----------:|----------------:|--------------:|
| Female | 7550 | 36 | 7 |
| Male | 7560 | 36 | 7 |
| Persons | 7540 | 36 | 7 |

### Gender coverage details
- **Female** in 36/36 states, years [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)].
- **Male** in 36/36 states, years [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)].
- **Persons** in 36/36 states, years [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)].

## 4. Area‑Type Diagnostic
| Area Type | Row count | States covered | Years covered |
|-----------|----------:|----------------:|--------------:|
| Rural | 7560 | 36 | 7 |
| Rural + Urban | 7530 | 36 | 7 |
| Urban | 7560 | 36 | 7 |

- Unique States: 36
- Unique Area Types: 3
- Observed State×Area combos: 108
- Missing State×Area combos: 0

## 5. Year Diagnostic
- Minimum year: 2017
- Maximum year: 2023
- Unique years: [np.int64(2017), np.int64(2018), np.int64(2019), np.int64(2020), np.int64(2021), np.int64(2022), np.int64(2023)]
- Row count by year: {"2017": 3240, "2018": 3240, "2019": 3240, "2020": 3240, "2021": 3240, "2022": 3210, "2023": 3240}
- Missing years in full range [2017, 2018, 2019, 2020, 2021, 2022, 2023]: []

## 6. State Diagnostic
- Number of unique States/UTs: 36
- States list (alphabetical):
  - Andaman and Nicobar Islands
  - Andhra Pradesh
  - Arunachal Pradesh
  - Assam
  - Bihar
  - Chandigarh
  - Chhattisgarh
  - Delhi
  - Goa
  - Gujarat
  - Haryana
  - Himachal Pradesh
  - Jammu and Kashmir
  - Jharkhand
  - Karnataka
  - Kerala
  - Ladakh
  - Lakshadweep
  - Madhya Pradesh
  - Maharashtra
  - Manipur
  - Meghalaya
  - Mizoram
  - Nagaland
  - Odisha
  - Puducherry
  - Punjab
  - Rajasthan
  - Sikkim
  - Tamil Nadu
  - Telangana
  - The Dadra and Nagar Haveli and Daman and Diu
  - Tripura
  - Uttar Pradesh
  - Uttarakhand
  - West Bengal

| State | Row count | Missing years | Missing genders | Missing area types |
|-------|----------:|--------------:|----------------:|-------------------:|
| Andaman and Nicobar Islands | 630 | [] | [] | [] |
| Andhra Pradesh | 630 | [] | [] | [] |
| Arunachal Pradesh | 630 | [] | [] | [] |
| Assam | 630 | [] | [] | [] |
| Bihar | 630 | [] | [] | [] |
| Chandigarh | 630 | [] | [] | [] |
| Chhattisgarh | 630 | [] | [] | [] |
| Delhi | 630 | [] | [] | [] |
| Goa | 630 | [] | [] | [] |
| Gujarat | 630 | [] | [] | [] |
| Haryana | 630 | [] | [] | [] |
| Himachal Pradesh | 630 | [] | [] | [] |
| Jammu and Kashmir | 630 | [] | [] | [] |
| Jharkhand | 630 | [] | [] | [] |
| Karnataka | 630 | [] | [] | [] |
| Kerala | 630 | [] | [] | [] |
| Ladakh | 630 | [] | [] | [] |
| Lakshadweep | 620 | [] | [] | [] |
| Madhya Pradesh | 630 | [] | [] | [] |
| Maharashtra | 630 | [] | [] | [] |
| Manipur | 630 | [] | [] | [] |
| Meghalaya | 630 | [] | [] | [] |
| Mizoram | 630 | [] | [] | [] |
| Nagaland | 630 | [] | [] | [] |
| Odisha | 630 | [] | [] | [] |
| Puducherry | 610 | [] | [] | [] |
| Punjab | 630 | [] | [] | [] |
| Rajasthan | 630 | [] | [] | [] |
| Sikkim | 630 | [] | [] | [] |
| Tamil Nadu | 630 | [] | [] | [] |
| Telangana | 630 | [] | [] | [] |
| The Dadra and Nagar Haveli and Daman and Diu | 630 | [] | [] | [] |
| Tripura | 630 | [] | [] | [] |
| Uttar Pradesh | 630 | [] | [] | [] |
| Uttarakhand | 630 | [] | [] | [] |
| West Bengal | 630 | [] | [] | [] |

## 7. State × Year Coverage
- Possible combos (States × Years): 252
- Observed combos: 252
- Missing combos: 0
- Duplicate rows: 22398
- Max duplicate count: 90

## 8. State × Year × Gender Coverage
- Observed combos: 756
- Missing combos: 0
- Duplicate rows: 21894
- Max duplicate count: 30

## 9. State × Year × Area_Type Coverage
- Observed combos: 756
- Missing combos: 0
- Duplicate rows: 21894
- Max duplicate count: 30

## 10. State × Year × Gender × Area_Type Coverage
- Observed combos: 2265
- Missing combos: 3
  - Example missing: ('Lakshadweep', np.int64(2022), 'Persons', 'Rural + Urban')
- Duplicate rows: 20385
- Max duplicate count: 10

## 11. Education Diagnostic
- Unique education categories (10):
  - All
  - Diploma/ Certificate Course
  - Graduate
  - Higher Secondary
  - Literate & Upto Primary
  - Middle
  - Not Literate
  - Post Graduate & Above
  - Secondary
  - Secondary & Above
- Detailed categories (7): ['Diploma/ Certificate Course', 'Graduate', 'Higher Secondary', 'Literate & Upto Primary', 'Middle', 'Not Literate', 'Secondary']
- Aggregate categories (3): ['All', 'Post Graduate & Above', 'Secondary & Above']

## 12. Duplicate Diagnostic
| Level | Unique keys | Duplicate keys | Rows in duplicates | Max dup count | Example keys (up to 5) |
|-------|------------:|---------------:|-------------------:|--------------:|-----------------------|
| State×Year | 252 | 252 | 22650 | 90 | {('Andaman and Nicobar Islands', 2017): 90, ('Andaman and Nicobar Islands', 2018): 90, ('Andaman and Nicobar Islands', 2019): 90, ('Andaman and Nicobar Islands', 2020): 90, ('Andaman and Nicobar Islands', 2021): 90} |
| State×Year×Gender | 756 | 756 | 22650 | 30 | {('Andaman and Nicobar Islands', 2017, 'Female'): 30, ('Andaman and Nicobar Islands', 2017, 'Male'): 30, ('Andaman and Nicobar Islands', 2017, 'Persons'): 30, ('Andaman and Nicobar Islands', 2018, 'Female'): 30, ('Andaman and Nicobar Islands', 2018, 'Male'): 30} |
| State×Year×Area | 756 | 756 | 22650 | 30 | {('Andaman and Nicobar Islands', 2017, 'Rural'): 30, ('Andaman and Nicobar Islands', 2017, 'Rural + Urban'): 30, ('Andaman and Nicobar Islands', 2017, 'Urban'): 30, ('Andaman and Nicobar Islands', 2018, 'Rural'): 30, ('Andaman and Nicobar Islands', 2018, 'Rural + Urban'): 30} |
| State×Year×Gender×Area | 2265 | 2265 | 22650 | 10 | {('Andaman and Nicobar Islands', 2017, 'Female', 'Rural'): 10, ('Andaman and Nicobar Islands', 2017, 'Female', 'Rural + Urban'): 10, ('Andaman and Nicobar Islands', 2017, 'Female', 'Urban'): 10, ('Andaman and Nicobar Islands', 2017, 'Male', 'Rural'): 10, ('Andaman and Nicobar Islands', 2017, 'Male', 'Rural + Urban'): 10} |
| State×Year×Gender×Area×Education | 22650 | 0 | 0 | 0 | {} |

## 13. Indicator Coverage
- **LFPR** missing: 30 rows (0.13%).
  - By Year: {"2017": 0, "2018": 0, "2019": 0, "2020": 0, "2021": 0, "2022": 0, "2023": 30}
  - By Gender: {"Female": 10, "Male": 10, "Persons": 10}
  - By Area: {"Rural": 30, "Rural + Urban": 0, "Urban": 0}
  - By Education: {"All": 3, "Diploma/ Certificate Course": 3, "Graduate": 3, "Higher Secondary": 3, "Literate & Upto Primary": 3, "Middle": 3, "Not Literate": 3, "Post Graduate & Above": 3, "Secondary": 3, "Secondary & Above": 3}
- **WPR** missing: 30 rows (0.13%).
  - By Year: {"2017": 0, "2018": 0, "2019": 0, "2020": 0, "2021": 0, "2022": 0, "2023": 30}
  - By Gender: {"Female": 10, "Male": 10, "Persons": 10}
  - By Area: {"Rural": 30, "Rural + Urban": 0, "Urban": 0}
  - By Education: {"All": 3, "Diploma/ Certificate Course": 3, "Graduate": 3, "Higher Secondary": 3, "Literate & Upto Primary": 3, "Middle": 3, "Not Literate": 3, "Post Graduate & Above": 3, "Secondary": 3, "Secondary & Above": 3}
- **Unemployment_Rate** missing: 30 rows (0.13%).
  - By Year: {"2017": 0, "2018": 0, "2019": 0, "2020": 0, "2021": 0, "2022": 0, "2023": 30}
  - By Gender: {"Female": 10, "Male": 10, "Persons": 10}
  - By Area: {"Rural": 30, "Rural + Urban": 0, "Urban": 0}
  - By Education: {"All": 3, "Diploma/ Certificate Course": 3, "Graduate": 3, "Higher Secondary": 3, "Literate & Upto Primary": 3, "Middle": 3, "Not Literate": 3, "Post Graduate & Above": 3, "Secondary": 3, "Secondary & Above": 3}

## 14. Reusable Analytical Structure Assessment
- Exact one‑observation combos: 22650
- Multiple‑observation combos (need aggregation): 0
- Missing combos: 0
- Conflicting indicator values among duplicates: 0

## 15. Question‑Support Assessment
- **State / Year profile**: Supported with aggregation
- **Gender**: Supported with aggregation
- **Area**: Supported with aggregation
- **Education**: Supported with coverage limitations
- **Gender × Area**: Supported with aggregation
- **Gender × Education**: Supported with coverage limitations
- **Area × Education**: Supported with coverage limitations
- **Gender × Area × Education**: Supported with coverage limitations
- **State × Gender**: Supported with aggregation
- **State × Area**: Supported with aggregation
- **State × Education**: Supported with coverage limitations
- **Year × Gender**: Supported with aggregation
- **Year × Area**: Supported with aggregation
- **Year × Education**: Supported with coverage limitations

## 16. Architecture Recommendation
- Feasibility: Feasible.
- Recommended dimensions: State, YearNum, Gender, Area_Type, Education Level.
- Recommended indicators: LFPR, WPR, Unemployment Rate.
- Aggregation: mean (or weighted average if scaling factors exist).
- Duplicate handling: retain duplicate counts for quality tracking; aggregate as above.
- Missing values: keep as NaN; downstream analyses must handle them.
- Education handling: keep all detailed categories; aggregates can be derived when needed.
- Rural + Urban: retain as explicit Area_Type where present; do not fabricate.
- Gender "Persons": retain alongside Female and Male.
- Existing Q1–Q17 outputs remain unchanged.

---
*Audit generated automatically.*
