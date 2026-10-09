# Final reproducibility & consistency check – Dataset 1

| Check | Expected | Actual | Status |
|-------|---------:|-------:|--------|
| Rows | 22650 | 22650 | PASS |
| Columns | 9 | 9 | PASS |
| Structural missing combinations | 30 | 30 | PASS |
| Missing LFPR records | 30 | 30 | PASS |
| Missing WPR records | 30 | 30 | PASS |
| Missing UR records | 30 | 30 | PASS |
| Chandigarh 2023 Rural NULL records | 30 | 30 | PASS |
| WPR > LFPR rows | 1 | 1 | PASS |
| Values outside 0‑100 | 0 | 0 | PASS |
| Complete‑row duplicates | 0 | 0 | PASS |
| Candidate‑key duplicates | 0 | 0 | PASS |

## Additional checks

- Unique States/UTs: 36 (expected 36) -> PASS
- PLFS years cover 2017‑2023: PASS
- Intersection of structural missing combos with indicator‑missing records: 0 (expected 0) -> PASS

**Task 1A Dataset 1 Diagnostic is reproducible and internally consistent. Task 1A is complete and ready for closure.**

STOP