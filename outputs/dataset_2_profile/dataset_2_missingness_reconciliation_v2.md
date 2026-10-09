# Dataset 2 – Missing‑Value Reconciliation (v2)

## Overall verification

| Metric | Expected | Actual | Result |
|--------|----------|--------|--------|
| Total rows | 31080 | 31080 | PASS |
| Estimated Persons missing | 10344 | 10344 | PASS |
| Sample Number missing | 5184 | 5184 | PASS |
| Sum(both + only Est + only Samp) | 10344 | 10344 | PASS |

## A. Missingness by Year × Industry Division Type

| Year | Industry Division Type | Total Rows | Missing Rows | Missing % | Est Missing | Samp Missing | Both Missing | Only Est Missing | Only Samp Missing |
|------|-----------------------|------------|--------------|----------|------------|--------------|--------------|------------------|-------------------|
| PLFS Year (Jul - Jun), 2017 | (014, 016, 017 , 02-99) | 2592 | 2592 | 100.00% | 2592 | 2592 | 2592 | 0 | 0 |
| PLFS Year (Jul - Jun), 2017 | (05-99) | 2592 | 2592 | 100.00% | 2592 | 2592 | 2592 | 0 | 0 |
| PLFS Year (Jul - Jun), 2018 | (014, 016, 017 , 02-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2018 | (05-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2019 | (014, 016, 017 , 02-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2019 | (05-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2020 | (014, 016, 017 , 02-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2020 | (05-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2021 | (014, 016, 017 , 02-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2021 | (05-99) | 2592 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 |
| PLFS Year (Jul - Jun), 2022 | (05-99) | 2592 | 2592 | 100.00% | 2592 | 0 | 0 | 2592 | 0 |
| PLFS Year (Jul - Jun), 2023 | (05-99) | 2568 | 2568 | 100.00% | 2568 | 0 | 0 | 2568 | 0 |

## B. Summary of co‑occurrence across all data

| Co‑occurrence type | Row count |
|---------------------|-----------|
| Both fields missing | 5184 |
| Only Estimated Persons missing | 5160 |
| Only Sample Number missing | 0 |

The table above lists every Year‑Industry block present in the data, the total rows in that block, the number of rows with any missing indicator, and the breakdown of missingness.

**All calculations are derived directly from the cleaned dataset; no prior reports were consulted.**
