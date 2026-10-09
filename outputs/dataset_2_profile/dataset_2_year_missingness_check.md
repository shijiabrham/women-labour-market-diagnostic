# Dataset 2 – Year‑Level Missingness Verification

## 1. Dataset Year Coverage
- Unique years found: PLFS Year (Jul - Jun), 2017, PLFS Year (Jul - Jun), 2018, PLFS Year (Jul - Jun), 2019, PLFS Year (Jul - Jun), 2020, PLFS Year (Jul - Jun), 2021, PLFS Year (Jul - Jun), 2022, PLFS Year (Jul - Jun), 2023
- Record count per year: {'PLFS Year (Jul - Jun), 2017': 5184, 'PLFS Year (Jul - Jun), 2018': 5184, 'PLFS Year (Jul - Jun), 2019': 5184, 'PLFS Year (Jul - Jun), 2020': 5184, 'PLFS Year (Jul - Jun), 2021': 5184, 'PLFS Year (Jul - Jun), 2022': 2592, 'PLFS Year (Jul - Jun), 2023': 2568}
- All seven expected years present: YES

## 2. Year‑Level Missingness (numeric fields)

| PLFS Year | Total Rows | % Field Missing Count | % Field Missing % | Estimated Persons Missing Count | Estimated Persons Missing % | Sample Workers Missing Count | Sample Workers Missing % |
|------------|-----------:|----------------------:|-----------------:|------------------------------:|---------------------------:|----------------------------:|--------------------------:|
| PLFS Year (Jul - Jun), 2017 | 5184 | 0 | 0.0 | 5184 | 100.0 | 5184 | 100.0 |
| PLFS Year (Jul - Jun), 2018 | 5184 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2019 | 5184 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2020 | 5184 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2021 | 5184 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2022 | 2592 | 0 | 0.0 | 2592 | 100.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2023 | 2568 | 0 | 0.0 | 2568 | 100.0 | 0 | 0.0 |

## 3. Missingness Pattern by Year (three numeric fields)

| PLFS Year | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|------------|----:|----:|----:|----:|----:|----:|----:|----:|
| PLFS Year (Jul - Jun), 2017 | 0 | 0 | 0 | 5184 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2018 | 5184 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2019 | 5184 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2020 | 5184 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2021 | 5184 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2022 | 0 | 0 | 2592 | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2023 | 0 | 0 | 2568 | 0 | 0 | 0 | 0 | 0 |

## 4. Records with ≥ 1 Missing Numeric Field (per year)

| PLFS Year | Records with ≥1 missing numeric field | % of year rows affected |
|------------|------------------------------------:|-----------------------:|
| PLFS Year (Jul - Jun), 2017 | 5184 | 100.0 |
| PLFS Year (Jul - Jun), 2018 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2019 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2020 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2021 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2022 | 2592 | 100.0 |
| PLFS Year (Jul - Jun), 2023 | 2568 | 100.0 |

## 5. Reconciliation Checks
- CHECK A (total rows = 31 080): PASS
- CHECK B (Estimated Persons missing = 10 344): PASS
- CHECK B (Sample Workers missing = 5 184): PASS
- CHECK C (Percentage field missing = 0): PASS
- CHECK D (records with any numeric missing = 10 344): PASS
- CHECK F (pattern counts sum to yearly totals): PASS

## 6. Confirmation of Previously Observed Pattern
- Prior statement that missingness occurs only in 2017, 2022, 2023: TRUE

Dataset 2 contains seven PLFS years, 2017–2023. Missingness in the numeric fields is concentrated in 2017, 2022 and 2023, while 2018–2021 have no missing values in these fields.

---

**Confirmed Findings**
- All seven PLFS years are present.
- Percentage field has zero missing values.
- Missingness is limited to Estimated Persons and Sample Workers, concentrated in 2017, 2022 and 2023.

**Unresolved Questions**
- Why the two count fields are missing for many records in the indicated years (to be investigated in later tasks).