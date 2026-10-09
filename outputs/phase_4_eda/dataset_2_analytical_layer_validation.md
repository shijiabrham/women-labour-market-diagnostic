# Dataset 2 — Reusable Analytical Layer Validation

**Project:** Women's Labour Market Diagnostic in India  
**Output file:** `outputs/phase_4_eda/dataset_2_reusable_analytical.csv`  
**Build script:** `scripts/dataset_2_analytical_layer.py`  
**Date:** 2026-10-02  

---

## Source

| Item | Value |
|------|-------|
| Source file | `outputs/dataset_2_profile/feature_engineered_dataset_2.csv` |
| Source rows | 31,080 |
| Source columns | 21 |
| Source MD5 (pre-build) | `bdc38216521c532872123be94c9fc1cc` |
| Source MD5 (post-build) | `bdc38216521c532872123be94c9fc1cc` |
| Source modified | **No** |

---

## Transformations Applied

| # | Transformation | Detail |
|---|---------------|--------|
| 1 | Column selection | 6 dimensions + 1 measure selected from 21 source columns |
| 2 | Column renaming | Clean analytical names applied (see mapping below) |
| 3 | Year representation | `Year_Numeric` (integer, e.g. 2017) used instead of raw range string |
| 4 | Industry label standardisation | `(014, 016, 017 , 02-99)` → `(014, 016, 017, 02-99)` — irregular internal whitespace removed; 12,960 rows affected; category meaning unchanged |

### Column mapping

| Feature-engineered column | Analytical column |
|---------------------------|------------------|
| `State` | `State` |
| `Year_Numeric` | `Year` |
| `Gender` | `Gender` |
| `Type Of Areas` | `Area_Type` |
| `Industry Division Type` | `Industry_Division_Type` |
| `Enterprise Type` | `Enterprise_Type` |
| `Persons_Engaged_Percentage_Numeric` | `Percentage_Engaged` |

### Columns NOT carried forward (intentional)

`Estimated Persons`, `Sample Number Of Workers`, `Female_Flag`, `Rural_Flag`, `Industry_Division_Count`, `Industry_Is_MultiDivision`, `Industry_Group_Type`, `Industry_Percentage_Availability_Flag`, `Estimated_Persons_Availability_Flag`, `Sample_Number_Of_Workers_Availability_Flag`, `Structural_Missingness_Flag`, `Country`, raw `Year` string

---

## Output Schema

| Column | Type | Description |
|--------|------|-------------|
| `State` | object | 36 States/UTs |
| `Year` | int64 | 2017–2023 |
| `Gender` | object | Female, Male, Persons |
| `Area_Type` | object | Rural, Urban, Rural + Urban |
| `Industry_Division_Type` | object | `(05-99)`, `(014, 016, 017, 02-99)` |
| `Enterprise_Type` | object | 8 enterprise categories |
| `Percentage_Engaged` | float64 | Persons engaged (%) — sourced directly |

---

## Validation Results — 22 / 22 PASS

| # | Check | Result |
|---|-------|--------|
| 1 | Row count = 31,080 | ✅ PASS |
| 2 | Exactly 7 columns | ✅ PASS |
| 3 | Zero duplicate analytical keys | ✅ PASS |
| 4 | State count = 36 | ✅ PASS |
| 5 | Years = [2017, 2018, 2019, 2020, 2021, 2022, 2023] | ✅ PASS |
| 6 | Gender = [Female, Male, Persons] | ✅ PASS |
| 7 | Area = [Rural, Rural + Urban, Urban] | ✅ PASS |
| 8 | Industry count = 2 | ✅ PASS |
| 9 | Industry label whitespace standardised | ✅ PASS |
| 10 | Enterprise count = 8 | ✅ PASS |
| 11 | Percentage_Engaged — zero missing | ✅ PASS |
| 12 | Percentage_Engaged in [0, 100] | ✅ PASS |
| 13 | `(014, 016, 017, 02-99)` absent in 2022–2023 (structural) | ✅ PASS |
| 14 | `(05-99)` present in all 7 years | ✅ PASS |
| 15 | No Estimated_Persons column | ✅ PASS |
| 16 | No Sample_Number_Of_Workers column | ✅ PASS |
| 17 | Percentage_Engaged values match source exactly | ✅ PASS |
| 18 | Year column is integer dtype (int64) | ✅ PASS |
| 19 | 2017–2021 each have 5,184 rows | ✅ PASS |
| 20 | 2022 has 2,592 rows | ✅ PASS |
| 21 | 2023 has 2,568 rows | ✅ PASS |
| 22 | No Q27–Q32 columns | ✅ PASS |

---

## Dimension Coverage

### Year row counts

| Year | Rows | Note |
|------|------|------|
| 2017 | 5,184 | Both industry types present |
| 2018 | 5,184 | Both industry types present |
| 2019 | 5,184 | Both industry types present |
| 2020 | 5,184 | Both industry types present |
| 2021 | 5,184 | Both industry types present |
| 2022 | 2,592 | `(014, 016, 017, 02-99)` structurally absent |
| 2023 | 2,568 | `(014, 016, 017, 02-99)` structurally absent |

### Industry × Year coverage

| Industry Division Type | 2017–2021 | 2022 | 2023 |
|------------------------|-----------|------|------|
| `(05-99)` | Present | Present | Present |
| `(014, 016, 017, 02-99)` | Present | **Absent** | **Absent** |

Structural absence preserved as-sourced. No imputation applied.

---

## Confirmed Source Grain

```
State × Year × Gender × Area_Type × Industry_Division_Type × Enterprise_Type
```

- 31,080 unique keys = 31,080 rows
- **0 duplicate analytical keys**

---

## Analytical Architecture Boundary

| Layer | Source | Status |
|-------|--------|--------|
| Raw source | `data/raw/dataset_2/...csv` | Read-only — diagnostic only |
| Feature-engineered | `outputs/dataset_2_profile/feature_engineered_dataset_2.csv` | Read-only — preparation only |
| **Reusable analytical CSV** | `outputs/phase_4_eda/dataset_2_reusable_analytical.csv` | **← Analytical boundary** |
| Dataset 2 analytical engine | reads reusable CSV only | Not yet built |
| Dataset 2 insights | reads engine output | Not yet built |
| Dataset 2 narratives | reads insight output | Not yet built |

---

## Known Methodological Constraints

1. **Industry granularity:** Only 2 broad PLFS groupings — no detailed sector analysis
2. **Temporal imbalance:** `(014, 016, 017, 02-99)` absent 2022–2023 — not imputed
3. **Source aggregates preserved:** `Rural + Urban`, `Persons`, enterprise categories — never reconstructed
4. **Zero values valid:** 5,116 rows have `Percentage_Engaged = 0.0` — genuine observations
5. **Percentage sourced directly:** Not derived from `Estimated Persons` or `Sample Number Of Workers`

---

## Protection Confirmations

| Item | Status |
|------|--------|
| `feature_engineered_dataset_2.csv` source — not modified | ✅ MD5 unchanged |
| Raw Dataset 2 source — not modified | ✅ |
| Q27–Q32 analytical CSVs — not created | ✅ |
| Dataset 1 files — not modified | ✅ |
| New packages installed | ✅ None |

---

*Validation passed: 22 / 22. Output file confirmed.*
