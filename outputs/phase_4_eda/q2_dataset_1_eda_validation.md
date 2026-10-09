# Q2 – Female Working Population Rate – Validation Report

## Source integrity
- Source exists: outputs/dataset_1_profile/feature_engineered_dataset_1.csv
- Row count: 22650 (expected 22650)
- Column count: 14 (expected 14)
- SHA‑256: 86fbca6d038de1139df8f21fa326338cdd8e25df8d5f5247ad655e655a0c005b

- Filtered female rows: 7550
- Valid WPR observations: 7540
- Missing WPR observations: 10

## Per‑year statistics (as written)

| Year | Filtered | Valid | Mean | Median | Min | Max | Std | Missing |
|------|--------:|------:|-----:|-------:|----:|----:|----:|--------:|
| 2017 | 7550 | 1080 | 23.945 | 19.35 | 0.0 | 100.0 | 17.993 | 0 |
| 2018 | 7550 | 1080 | 25.659 | 22.15 | 0.0 | 100.0 | 18.22 | 0 |
| 2019 | 7550 | 1080 | 30.295 | 26.175 | 0.0 | 100.0 | 19.066 | 0 |
| 2020 | 7550 | 1080 | 31.454 | 27.1 | 0.0 | 100.0 | 19.362 | 0 |
| 2021 | 7550 | 1080 | 31.306 | 28.55 | 0.0 | 100.0 | 18.87 | 0 |
| 2022 | 7550 | 1070 | 35.576 | 32.6 | 0.0 | 100.0 | 20.514 | 0 |
| 2023 | 7550 | 1070 | 39.328 | 36.35 | 0.0 | 100.0 | 20.249 | 10 |

## Overall statistics

- Filtered female rows: 7550
- Valid WPR observations: 7540
- Missing WPR observations: 10
- Mean: 31.063
- Median: 27.1
- Minimum: 0.0
- Maximum: 100.0
- Population SD: 19.818

## Independent validation comparison

| Metric | Result File | Independent | Difference | Status |
|--------|------------:|------------:|-----------:|--------|
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 23.945 | 23.945 | 0.0 | PASS |
| Median | 19.35 | 19.35 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 17.993 | 17.993 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 25.659 | 25.659 | 0.0 | PASS |
| Median | 22.15 | 22.15 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 18.22 | 18.22 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 30.295 | 30.295 | 0.0 | PASS |
| Median | 26.175 | 26.175 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 19.066 | 19.066 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 31.454 | 31.454 | 0.0 | PASS |
| Median | 27.1 | 27.1 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 19.362 | 19.362 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 31.306 | 31.306 | 0.0 | PASS |
| Median | 28.55 | 28.55 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 18.87 | 18.87 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1070 | 1070 | 0.0 | PASS |
| Mean | 35.576 | 35.576 | 0.0 | PASS |
| Median | 32.6 | 32.6 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 20.514 | 20.514 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1070 | 1070 | 0.0 | PASS |
| Mean | 39.328 | 39.328 | 0.0 | PASS |
| Median | 36.35 | 36.35 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 20.249 | 20.249 | 0.0 | PASS |
| Missing_Count | 10 | 10 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 7540 | 7540 | 0.0 | PASS |
| Mean | 31.063 | 31.063 | 0.0 | PASS |
| Median | 27.1 | 27.1 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 19.818 | 19.818 | 0.0 | PASS |
| Missing_Count | 10 | 10 | 0.0 | PASS |

## Final status

**PASS**
