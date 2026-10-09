# Dataset 2 – Missing‑Value Diagnosis

## A. Missing counts by Year × Industry Division Type

| Year | Industry Division Type | Total Rows | Estimated Persons Missing | Sample Number Missing | Both Missing | Pattern |
|------|-----------------------|------------|---------------------------|-----------------------|--------------|---------|
| PLFS Year (Jul - Jun), 2017 | (014, 016, 017 , 02-99) | 2592 | 2592 | 2592 | 2592 | structural |
| PLFS Year (Jul - Jun), 2017 | (05-99) | 2592 | 2592 | 2592 | 2592 | structural |
| PLFS Year (Jul - Jun), 2022 | (05-99) | 2592 | 2592 | 0 | 0 | structural |
| PLFS Year (Jul - Jun), 2023 | (05-99) | 2568 | 2568 | 0 | 0 | structural |

## B. Extension of missingness across other dimensions

For each Year‑Industry block, we compare the number of distinct combinations of State, Type Of Areas, Gender, and Enterprise Type present in the missing rows versus the total possible combinations in that block.

| Year | Industry Division Type | Missing Combos | Total Combos | Extension
|------|-----------------------|----------------|--------------|----------|
| PLFS Year (Jul - Jun), 2017 | (014, 016, 017 , 02-99) | 2592 | 2592 | covers all |
| PLFS Year (Jul - Jun), 2017 | (05-99) | 2592 | 2592 | covers all |
| PLFS Year (Jul - Jun), 2022 | (05-99) | 2592 | 2592 | covers all |
| PLFS Year (Jul - Jun), 2023 | (05-99) | 2568 | 2568 | covers all |

## C. Summary of pattern types

- Structural blocks (missing across all State/Area/Gender/Enterprise combos): 4
- Partial blocks (missing for a subset of combos): 0
- Isolated rows (missing in a single combination): 0

## D. Co‑occurrence of missing fields

| Missing type | Row count |
|--------------|-----------|
| Both Estimated & Sample missing | 5184 |
| Only Estimated Persons missing | 5160 |
| Only Sample Number missing | 0 |

## E. Conclusion

Missing values are predominantly organized in structural blocks: for certain Year‑Industry Division Type combinations, *all* State/Area/Gender/Enterprise entries are missing for both Estimated Persons and Sample Number.
Both numeric fields tend to be missing together; rows where only one of the two is missing are rare.

