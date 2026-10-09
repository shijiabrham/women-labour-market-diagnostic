# Q18-Q26 Validation Report

## Summary
- **Total checks:** 64
- **PASS:** 64
- **FAIL:** 0
- **Overall status: PASS**

## Row Counts

| Question | Output file | Row count | Columns | Grain |
|---------|-------------|-----------|---------|-------|
| Q18 | `q18_gender_education_lfpr.csv` | 56 | 5 | Year × Education (8) = 56 |
| Q19 | `q19_gender_education_wpr.csv` | 56 | 5 | Year × Education (8) = 56 |
| Q20 | `q20_gender_education_unemployment.csv` | 56 | 5 | Year × Education (8) = 56 |
| Q21 | `q21_gender_area_labour_market.csv` | 14 | 11 | Year × Area_Type (2) = 14 |
| Q22 | `q22_women_lfpr_trend.csv` | 7 | 4 | Year = 7 |
| Q23 | `q23_women_wpr_trend.csv` | 7 | 4 | Year = 7 |
| Q24 | `q24_women_unemployment_trend.csv` | 7 | 4 | Year = 7 |
| Q25 | `q25_women_education_change.csv` | 24 | 6 | Education (8) × Indicator (3) = 24 |
| Q26 | `q26_women_rural_urban_trends.csv` | 7 | 22 | Year = 7 |

## Validation Checks

| Check ID | Description | Expected | Actual | Status |
|----------|-------------|----------|--------|--------|
| Q18-A1 | File exists | True | True | **PASS** |
| Q18-A2 | Columns | ['Year', 'Education', 'LFPR_Female', 'LFPR_Male', 'LFPR_FM_Gap'] | ['Year', 'Education', 'LFPR_Female', 'LFPR_Male', 'LFPR_FM_Gap'] | **PASS** |
| Q18-B1 | Row count 56 | 56 | 56 | **PASS** |
| Q18-C1 | No dup Year×Edu | 0 | 0 | **PASS** |
| Q18-D1 | 8 detailed edu categories | 8 | 8 | **PASS** |
| Q18-D2 | No aggregate edu in output | False | False | **PASS** |
| Q18-D3 | Years 2017-2023 | 7 | 7 | **PASS** |
| Q18-E1 | FM_Gap ≈ Female − Male (tol=0.01) | True | True | **PASS** |
| Q18-F1 | No missing LFPR values | 0 | 0 | **PASS** |
| Q19-A1 | File exists | True | True | **PASS** |
| Q19-A2 | Columns | ['Year', 'Education', 'WPR_Female', 'WPR_Male', 'WPR_FM_Gap'] | ['Year', 'Education', 'WPR_Female', 'WPR_Male', 'WPR_FM_Gap'] | **PASS** |
| Q19-B1 | Row count 56 | 56 | 56 | **PASS** |
| Q19-C1 | No dup Year×Edu | 0 | 0 | **PASS** |
| Q19-D1 | 8 detailed edu | 8 | 8 | **PASS** |
| Q19-E1 | FM_Gap ≈ Female − Male | True | True | **PASS** |
| Q20-A1 | File exists | True | True | **PASS** |
| Q20-A2 | Columns | ['Year', 'Education', 'Unemployment_Rate_Female', 'Unemployment_Rate_Male', 'Unemployment_Rate_FM_Gap'] | ['Year', 'Education', 'Unemployment_Rate_Female', 'Unemployment_Rate_Male', 'Unemployment_Rate_FM_Gap'] | **PASS** |
| Q20-B1 | Row count 56 | 56 | 56 | **PASS** |
| Q20-C1 | No dup Year×Edu | 0 | 0 | **PASS** |
| Q20-D1 | 8 detailed edu | 8 | 8 | **PASS** |
| Q20-E1 | FM_Gap ≈ Female − Male | True | True | **PASS** |
| Q21-A1 | File exists | True | True | **PASS** |
| Q21-B1 | Row count 14 | 14 | 14 | **PASS** |
| Q21-C1 | No dup Year×Area | 0 | 0 | **PASS** |
| Q21-D1 | Area = Rural,Urban only | {'Rural', 'Urban'} | {'Rural', 'Urban'} | **PASS** |
| Q21-D2 | Rural+Urban absent | False | False | **PASS** |
| Q21-E-LFPR | LFPR FM_Gap ≈ Female − Male | True | True | **PASS** |
| Q21-E-WPR | WPR FM_Gap ≈ Female − Male | True | True | **PASS** |
| Q21-E-Unemployment_Rate | Unemployment_Rate FM_Gap ≈ Female − Male | True | True | **PASS** |
| Q22-A1 | File exists | True | True | **PASS** |
| Q22-A2 | Columns | ['Year', 'LFPR', 'Absolute_Change_vs_2017', 'Percentage_Change_vs_2017'] | ['Year', 'LFPR', 'Absolute_Change_vs_2017', 'Percentage_Change_vs_2017'] | **PASS** |
| Q22-B1 | Row count 7 | 7 | 7 | **PASS** |
| Q22-C1 | No dup Year | 0 | 0 | **PASS** |
| Q22-D1 | Years 2017-2023 | 7 | 7 | **PASS** |
| Q22-E1 | 2017 Absolute_Change = 0 | 0.0 | 0.0 | **PASS** |
| Q22-E2 | No missing LFPR | 0 | 0 | **PASS** |
| Q22-E3 | Pct formula correct | True | True | **PASS** |
| Q23-A1 | File exists | True | True | **PASS** |
| Q23-B1 | Row count 7 | 7 | 7 | **PASS** |
| Q23-C1 | No dup Year | 0 | 0 | **PASS** |
| Q23-E1 | 2017 Absolute_Change = 0 | 0.0 | 0.0 | **PASS** |
| Q24-A1 | File exists | True | True | **PASS** |
| Q24-B1 | Row count 7 | 7 | 7 | **PASS** |
| Q24-C1 | No dup Year | 0 | 0 | **PASS** |
| Q24-E1 | 2017 Absolute_Change = 0 | 0.0 | 0.0 | **PASS** |
| Q25-A1 | File exists | True | True | **PASS** |
| Q25-A2 | Columns | ['Education', 'Indicator', 'Value_2017', 'Value_2023', 'Absolute_Change', 'Percentage_Change'] | ['Education', 'Indicator', 'Value_2017', 'Value_2023', 'Absolute_Change', 'Percentage_Change'] | **PASS** |
| Q25-B1 | Row count 24 | 24 | 24 | **PASS** |
| Q25-C1 | No dup Edu×Indicator | 0 | 0 | **PASS** |
| Q25-D1 | 8 detailed edu | 8 | 8 | **PASS** |
| Q25-D2 | No aggregate edu | False | False | **PASS** |
| Q25-D3 | 3 indicators | {'Unemployment_Rate', 'LFPR', 'WPR'} | {'Unemployment_Rate', 'LFPR', 'WPR'} | **PASS** |
| Q25-E1 | Abs_Change = V2023-V2017 | True | True | **PASS** |
| Q25-E2 | Pct_Change formula correct | True | True | **PASS** |
| Q26-A1 | File exists | True | True | **PASS** |
| Q26-B1 | Row count 7 | 7 | 7 | **PASS** |
| Q26-C1 | No dup Year | 0 | 0 | **PASS** |
| Q26-D1 | Years 2017-2023 | 7 | 7 | **PASS** |
| Q26-E-LFPR | LFPR RU_Gap ≈ Rural − Urban | True | True | **PASS** |
| Q26-E-WPR | WPR RU_Gap ≈ Rural − Urban | True | True | **PASS** |
| Q26-E-Unemployment_Rate | Unemployment_Rate RU_Gap ≈ Rural − Urban | True | True | **PASS** |
| PROT-1 | Source Dataset 1 not modified | 452c3bdacd29711f963925db04d5b789 | 452c3bdacd29711f963925db04d5b789 | **PASS** |
| PROT-2 | Reusable layer not modified | 662539abfbb7cc0490c5394168a7035f | 662539abfbb7cc0490c5394168a7035f | **PASS** |
| PROT-3 | Q1-Q17 scripts present (32) | present | present | **PASS** |

## Protection Check

- Source Dataset 1 MD5: `452c3bdacd29711f963925db04d5b789` — not modified.
- Reusable analytical layer MD5: `662539abfbb7cc0490c5394168a7035f` — not modified.
- Q1-Q17 scripts, CSVs, and MDs were not opened for writing.
- Dataset 2 was not accessed.
- No packages were installed.

## Overall

- **Q18-Q26 Validation: PASS**
- **Protected Outputs: PASS**

---
*Validation report generated automatically.*