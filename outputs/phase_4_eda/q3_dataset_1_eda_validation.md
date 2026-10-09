# Q3 – Female Unemployment Rate – Validation Report

## Source integrity
- Source exists: outputs/dataset_1_profile/feature_engineered_dataset_1.csv
- Row count: 22650 (expected 22650)
- Column count: 14 (expected 14)
- SHA‑256: 86fbca6d038de1139df8f21fa326338cdd8e25df8d5f5247ad655e655a0c005b

- Filtered female rows: 7550
- Valid UR observations: 7540
- Missing UR observations: 10

## Per‑year statistics (as written)

| Year | Filtered | Valid | Mean | Median | Min | Max | Std | Missing |
|------|--------:|------:|-----:|-------:|----:|----:|----:|--------:|
| 2017 | 7550 | 1080 | 15.89 | 10.3 | 0.0 | 100.0 | 18.658 | 0 |
| 2018 | 7550 | 1080 | 14.073 | 7.6 | 0.0 | 100.0 | 17.762 | 0 |
| 2019 | 7550 | 1080 | 11.434 | 4.8 | 0.0 | 100.0 | 16.342 | 0 |
| 2020 | 7550 | 1080 | 10.026 | 3.35 | 0.0 | 100.0 | 14.239 | 0 |
| 2021 | 7550 | 1080 | 10.911 | 4.6 | 0.0 | 100.0 | 16.023 | 0 |
| 2022 | 7550 | 1070 | 9.161 | 3.15 | 0.0 | 100.0 | 13.811 | 0 |
| 2023 | 7550 | 1070 | 9.831 | 3.7 | 0.0 | 100.0 | 14.257 | 10 |

## Overall statistics

- Filtered female rows: 7550
- Valid UR observations: 7540
- Missing UR observations: 10
- Mean: 11.624
- Median: 4.9
- Minimum: 0.0
- Maximum: 100.0
- Population SD: 16.133

## Independent validation comparison

| Metric | Result File | Independent | Difference | Status |
|--------|------------:|------------:|-----------:|--------|
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 15.89 | 15.89 | 0.0 | PASS |
| Median | 10.3 | 10.3 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 18.658 | 18.658 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 14.073 | 14.073 | 0.0 | PASS |
| Median | 7.6 | 7.6 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 17.762 | 17.762 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 11.434 | 11.434 | 0.0 | PASS |
| Median | 4.8 | 4.8 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 16.342 | 16.342 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 10.026 | 10.026 | 0.0 | PASS |
| Median | 3.35 | 3.35 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 14.239 | 14.239 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1080 | 1080 | 0.0 | PASS |
| Mean | 10.911 | 10.911 | 0.0 | PASS |
| Median | 4.6 | 4.6 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 16.023 | 16.023 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1070 | 1070 | 0.0 | PASS |
| Mean | 9.161 | 9.161 | 0.0 | PASS |
| Median | 3.15 | 3.15 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 13.811 | 13.811 | 0.0 | PASS |
| Missing_Count | 0 | 0 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 1070 | 1070 | 0.0 | PASS |
| Mean | 9.831 | 9.831 | 0.0 | PASS |
| Median | 3.7 | 3.7 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 14.257 | 14.257 | 0.0 | PASS |
| Missing_Count | 10 | 10 | 0.0 | PASS |
| Filtered_Row_Count | 7550 | 7550 | 0.0 | PASS |
| Valid_Observation_Count | 7540 | 7540 | 0.0 | PASS |
| Mean | 11.624 | 11.624 | 0.0 | PASS |
| Median | 4.9 | 4.9 | 0.0 | PASS |
| Minimum | 0.0 | 0.0 | 0.0 | PASS |
| Maximum | 100.0 | 100.0 | 0.0 | PASS |
| Population_Standard_Deviation | 16.133 | 16.133 | 0.0 | PASS |
| Missing_Count | 10 | 10 | 0.0 | PASS |

## Final status

**PASS**
