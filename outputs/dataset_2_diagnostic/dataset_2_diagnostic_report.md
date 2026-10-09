# Dataset 2 Diagnostic Report

**Project:** Women's Labour Market Diagnostic in India  
**Dataset:** Persons Engaged in Industry Groups by Enterprise Type — PLFS  
**Task:** Phase 1 — Dataset Diagnostic & Source Integrity  
**Diagnostic date:** 2026-10-02  
**Status:** READ-ONLY diagnostic. Source not modified.

---

## 1. Source File

| Item | Value |
|------|-------|
| **Exact path** | `data/raw/dataset_2/Persons Engaged in Industry by Enterprise Type – PLFS Year.csv` |
| **Rows** | 31,080 |
| **Columns** | 10 |
| **Source MD5 unchanged** | ✅ True |

---

## 2. Exact Schema

| # | Column name (exact) | Dtype | Missing | Missing % |
|---|---------------------|-------|---------|-----------|
| 1 | `Country` | object | 0 | 0.000% |
| 2 | `State` | object | 0 | 0.000% |
| 3 | `Year` | object | 0 | 0.000% |
| 4 | `Type Of Areas` | object | 0 | 0.000% |
| 5 | `Industry Division Type` | object | 0 | 0.000% |
| 6 | `Gender` | object | 0 | 0.000% |
| 7 | `Enterprise Type` | object | 0 | 0.000% |
| 8 | `Persons Engaged In The Industry Groups By Enterprise Type (%) (UOM:%(Percentage)), Scaling Factor:1` | float64 | 0 | 0.000% |
| 9 | `Estimated Persons (UOM:Number), Scaling Factor:100` | float64 | 10,344 | 33.282% |
| 10 | `Sample Number Of Workers In The Enterprise (UOM:Number), Scaling Factor:1` | float64 | 5,184 | 16.680% |

---

## 3. Core Dimensions — Exact Values

### Country
Single value: `India` (31,080 rows). Not analytically useful as a dimension.

### Year
**Format:** Range strings, e.g. `"PLFS Year (Jul - Jun), 2017"` — consistent across all rows.

| Year value | Rows |
|-----------|------|
| PLFS Year (Jul - Jun), 2017 | 5,184 |
| PLFS Year (Jul - Jun), 2018 | 5,184 |
| PLFS Year (Jul - Jun), 2019 | 5,184 |
| PLFS Year (Jul - Jun), 2020 | 5,184 |
| PLFS Year (Jul - Jun), 2021 | 5,184 |
| PLFS Year (Jul - Jun), 2022 | 2,592 |
| PLFS Year (Jul - Jun), 2023 | 2,568 |

> [!IMPORTANT]
> **2022 and 2023 have fewer rows than earlier years (2,592 and 2,568 vs 5,184).** This is approximately half the rows. The reduction is structural — likely one Industry Division Type is absent in 2022–2023. This must be investigated during cleaning and feature engineering. Do not treat the lower row counts as missing data or impute.

Expected years 2017–2023: **All present.** No year gaps.

### Gender

| Value | Rows |
|-------|------|
| Female | 10,360 |
| Male | 10,360 |
| Persons | 10,360 |

Exactly balanced. Matches Dataset 1 gender categories.

### Type Of Areas

| Value | Rows |
|-------|------|
| Urban | 10,368 |
| Rural + Urban | 10,368 |
| Rural | 10,344 |

> [!NOTE]
> Rural has 24 fewer rows than Urban and Rural + Urban. This matches the 3 missing State × Year × Gender × Area combinations identified in the coverage diagnostic.

Exact match with Dataset 1 area categories (`Rural`, `Urban`, `Rural + Urban`).

### Industry Division Type

| Value | Rows |
|-------|------|
| `(05-99)` | 18,120 |
| `(014, 016, 017 , 02-99)` | 12,960 |

> [!IMPORTANT]
> **Two Industry Division Types are present.** The prior project inspection had noted only `(05-99)`. The actual source contains both `(05-99)` and `(014, 016, 017 , 02-99)`. These are broad PLFS industry groupings, not detailed industry categories. Industry-level analysis (Q27, Q31, Q32) is possible only at this two-category level.
>
> Note also that `(014, 016, 017 , 02-99)` contains an irregular space before `02-99`. This should be noted for cleaning.

### Enterprise Type

| Value | Rows |
|-------|------|
| Proprietary and Partnership | 3,885 |
| Govt./ Local Body/ Public Sector Enterprises | 3,885 |
| Autonomous Bodies | 3,885 |
| Public/ Private Limited Company | 3,885 |
| Cooperative Societies | 3,885 |
| Trust/ Other Non Profit inst | 3,885 |
| Employer's Households | 3,885 |
| Others | 3,885 |

**8 enterprise categories, exactly balanced at 3,885 rows each.**

---

## 4. Year Coverage

- Years present: 2017, 2018, 2019, 2020, 2021, 2022, 2023
- All expected years: **Present**
- Year format: Range strings, all consistent (`PLFS Year (Jul - Jun), YYYY`)
- Year format types detected: One format only — no inconsistency
- Structural note: 2022 and 2023 have approximately half the rows of 2017–2021, attributable to `(014, 016, 017 , 02-99)` being absent in those years

---

## 5. Geographic Coverage

- **States/UTs present:** 36
- **State × Year coverage:** 252 combinations observed out of 252 theoretical (36 × 7) — **100% coverage**
- **Missing State × Year combinations:** None
- All 36 states match Dataset 1 states exactly — **common states: 36, unique to either dataset: 0**

---

## 6. Area Coverage

| Metric | Value |
|--------|-------|
| Area categories | Rural, Urban, Rural + Urban |
| Rural rows | 10,344 |
| Urban rows | 10,368 |
| Rural + Urban rows | 10,368 |
| Rural shortfall | 24 rows (3 missing State × Year × Gender combinations) |

Area category labels exactly match Dataset 1. No transformation required for compatibility.

---

## 7. Gender Coverage

- Categories: Female, Male, Persons — exactly balanced (10,360 each)
- Gender × Year: All years covered for all genders
- Gender × State: All 36 states covered for all genders
- Gender × Area: All area types covered for all genders
- Exact match with Dataset 1 gender categories

---

## 8. Industry Coverage

| Dimension | Value |
|-----------|-------|
| Unique Industry Division Types | **2** |
| Category 1 | `(05-99)` — 18,120 rows |
| Category 2 | `(014, 016, 017 , 02-99)` — 12,960 rows |
| Industry-level detail | Broad groupings only — not detailed NIC/ISIC categories |

> [!WARNING]
> These are PLFS aggregated industry bands, not individual industry sectors. Industry × Year coverage shows that `(014, 016, 017, 02-99)` is present only in 2017–2021, absent from 2022–2023. This is the root cause of the lower row counts in those years. **Do not impute absent industry-year combinations.**

---

## 9. Enterprise Coverage

- **8 enterprise type categories** (exact labels above)
- All 8 present in all years, all genders, all area types
- Exactly 3,885 rows per enterprise type — perfectly balanced
- Enterprise × Industry: Both industry types have all 8 enterprise categories

---

## 10. Primary Measure Diagnostic

**Column:** `Persons Engaged In The Industry Groups By Enterprise Type (%) (UOM:%(Percentage)), Scaling Factor:1`

| Statistic | Value |
|-----------|-------|
| dtype | float64 |
| Missing | 0 (0.000%) |
| Min | 0.0 |
| Max | 100.0 |
| Mean | 12.500% |
| Median | 1.800% |
| Std | 21.150 |
| Zero values | 5,116 |
| Negative values | 0 |
| Values > 100 | 0 |
| Values in [0, 100] | 31,080 (100%) |

> [!NOTE]
> All values are within the valid percentage range [0, 100]. No out-of-range anomalies. Zero values (5,116 = 16.5%) represent genuine observations where no persons were engaged in that enterprise type — treat as valid, not missing.
>
> The high median (1.8%) vs mean (12.5%) and high std (21.2) indicate a strongly right-skewed distribution consistent with enterprise-type concentration.

---

## 11. Secondary Measure Diagnostics

### Estimated Persons (UOM:Number, Scaling Factor:100)
| Statistic | Value |
|-----------|-------|
| dtype | float64 |
| Missing | 10,344 (33.3%) |
| Min | non-missing values present |
| Note | Do NOT reconstruct or use to derive the primary % measure |

### Sample Number Of Workers In The Enterprise (UOM:Number, Scaling Factor:1)
| Statistic | Value |
|-----------|-------|
| dtype | float64 |
| Missing | 5,184 (16.7%) |
| Note | Do NOT reconstruct or use to derive the primary % measure |

---

## 12. Missingness Findings

| Column | Missing | Missing % |
|--------|---------|-----------|
| Country | 0 | 0.000% |
| State | 0 | 0.000% |
| Year | 0 | 0.000% |
| Type Of Areas | 0 | 0.000% |
| Industry Division Type | 0 | 0.000% |
| Gender | 0 | 0.000% |
| Enterprise Type | 0 | 0.000% |
| Primary measure (%) | 0 | 0.000% |
| Estimated Persons | 10,344 | **33.282%** |
| Sample Number Of Workers | 5,184 | **16.680%** |

**Primary measure has no missing values.** Missingness is confined to the two secondary numeric measures and appears structurally linked to the Industry Division Type × Year coverage pattern.

---

## 13. Duplicate Findings

- **Fully duplicate rows:** 0
- **Duplicate analytical keys:** 0 at the full grain (see below)

---

## 14. Grain Findings

| Key combination | Unique keys | Rows | Duplicate keys | Max rows/key | Is unique |
|----------------|-------------|------|----------------|--------------|-----------|
| State | 36 | 31,080 | 31,044 | 864 | No |
| State × Year | 252 | 31,080 | 30,828 | 144 | No |
| State × Year × Gender | 756 | 31,080 | 30,324 | 48 | No |
| State × Year × Gender × Type Of Areas | 2,265 | 31,080 | 28,815 | 16 | No |
| State × Year × Gender × Type Of Areas × Industry Division Type | 3,885 | 31,080 | 27,195 | 8 | No |
| **State × Year × Gender × Type Of Areas × Industry Division Type × Enterprise Type** | **31,080** | **31,080** | **0** | **1** | **✅ Yes** |

**Confirmed source grain:**
```
State × Year × Gender × Type Of Areas × Industry Division Type × Enterprise Type
```
One row per unique six-dimensional combination. No duplicates at this grain.

---

## 15. Cross-Dimension Coverage

| Key combination | Present | Theoretical max | Missing | Coverage |
|----------------|---------|-----------------|---------|----------|
| State × Year | 252 | 252 | 0 | 100.00% |
| State × Year × Gender | 756 | 756 | 0 | 100.00% |
| State × Year × Gender × Area | 2,265 | 2,268 | **3** | 99.87% |
| State × Year × Gender × Area × Enterprise | 18,120 | 18,144 | **24** | 99.87% |
| State × Year × Gender × Area × Industry | 3,885 | 4,536 | **651** | 85.65% |

> [!IMPORTANT]
> The 651 missing State × Year × Gender × Area × Industry combinations are structural — `(014, 016, 017 , 02-99)` is absent from 2022 and 2023 for all states, genders, and areas. These are **not random missing values** — they are a dataset coverage boundary. Do not impute.

---

## 16. Source Integrity Findings

| Check | Result |
|-------|--------|
| Fully duplicate rows | 0 — **PASS** |
| Whitespace in categorical columns | None detected — **PASS** |
| Empty strings | None detected — **PASS** |
| Null-like string representations | None detected — **PASS** |
| Year format consistency | All rows use `PLFS Year (Jul - Jun), YYYY` — **PASS** |
| Numeric values in range [0, 100] for primary measure | 100% — **PASS** |
| Negative values in primary measure | 0 — **PASS** |
| Values > 100 in primary measure | 0 — **PASS** |
| Irregular spacing in Industry Division Type | `(014, 016, 017 , 02-99)` contains space before `02-99` — **NOTE for cleaning** |

---

## 17. Dataset 1 Compatibility

| Dimension | D1 values | D2 values | Compatible |
|-----------|-----------|-----------|------------|
| States | 36 | 36 | ✅ All 36 match exactly |
| Years | 2017–2023 | 2017–2023 | ✅ All 7 match |
| Gender | Female, Male, Persons | Female, Male, Persons | ✅ Exact match |
| Area categories | Rural, Urban, Rural + Urban | Rural, Urban, Rural + Urban | ✅ Exact match |

**No transformation required** on shared dimensions for Dataset 1 / Dataset 2 integration. Both datasets use identical state names, year ranges, gender labels, and area labels.

---

## 18. Q27–Q32 Feasibility Assessment

| Q | Question | Required | Source support | Limitation |
|---|----------|----------|----------------|------------|
| **Q27** | Women's employment distribution across Industry Division Types | Gender=Female, Industry, primary % | 2 industry categories present | **Partial only** — broad groupings `(05-99)` and `(014, 016, 017 , 02-99)`, not detailed sectors. Coverage uneven by year (second category absent 2022–2023). |
| **Q28** | Percentage engaged across Enterprise Types | Enterprise, primary % | 8 enterprise categories, all present, balanced | ✅ **Fully feasible** |
| **Q29** | Women's industry participation by Rural/Urban | Gender=Female, Area, primary % | Rural, Urban, Rural+Urban all present | ✅ **Feasible** — note 24 missing Rural combinations (3 State × Year × Gender) |
| **Q30** | Women's industry participation across Enterprise Types | Gender=Female, Enterprise, primary % | 8 enterprise types present | ✅ **Fully feasible** |
| **Q31** | Industry and enterprise pattern by Gender | Gender, Industry, Enterprise, primary % | All dimensions present; 2 industry groupings | ✅ **Feasible at available granularity** — gender × enterprise analysis possible; industry detail limited to 2 broad bands |
| **Q32** | Industry and enterprise pattern change 2017–2023 | Year, Industry, Enterprise, primary % | All years present; industry coverage uneven by year | ⚠️ **Partially feasible** — enterprise temporal trends fully available; industry temporal trend limited because `(014, 016, 017 , 02-99)` absent 2022–2023 |

---

## 19. Proposed Dataset 2 Data Contract

| Item | Value |
|------|-------|
| **Source file** | `data/raw/dataset_2/Persons Engaged in Industry by Enterprise Type – PLFS Year.csv` |
| **Source row count** | 31,080 |
| **Source columns** | 10 |
| **Core dimensions** | State, Year, Gender, Type Of Areas, Industry Division Type, Enterprise Type |
| **Primary analytical measure** | `Persons Engaged In The Industry Groups By Enterprise Type (%)` |
| **Secondary source measures** | Estimated Persons (33.3% missing), Sample Number Of Workers (16.7% missing) — source fields only, not to be used to derive primary % |
| **Year range** | 2017–2023 (PLFS Jul–Jun format) |
| **Geographic coverage** | 36 States/UTs — 100% State × Year coverage |
| **Gender coverage** | Female, Male, Persons — balanced (10,360 each) |
| **Area coverage** | Rural, Urban, Rural + Urban — 3 missing combinations (24 rows) |
| **Industry coverage** | 2 broad groupings: `(05-99)` (all years), `(014, 016, 017 , 02-99)` (2017–2021 only) |
| **Enterprise coverage** | 8 categories — balanced (3,885 each), all years, all genders, all areas |
| **Observed source grain** | State × Year × Gender × Type Of Areas × Industry Division Type × Enterprise Type |
| **Missing-value considerations** | Primary measure: 0% missing. Secondary measures: partially missing (structurally, not randomly). 651 missing Industry × Area combinations due to year-coverage boundary for second industry type. |
| **Known methodological constraints** | (1) Industry Division Type has 2 broad groupings only — no detailed sector analysis. (2) `(014, 016, 017 , 02-99)` absent from 2022–2023 — unbalanced temporal industry coverage. (3) Primary % measure must be used as sourced — do not reconstruct from Estimated Persons or Sample Workers. (4) Irregular whitespace in `(014, 016, 017 , 02-99)` label — clean before use. |

---

## 20. Files Created

| File | Type | Description |
|------|------|-------------|
| `scripts/dataset_2_diagnostic.py` | Script | Full 20-step read-only diagnostic |
| `outputs/dataset_2_diagnostic/dataset_2_schema.csv` | Diagnostic CSV | Column names, dtypes, null counts |
| `outputs/dataset_2_diagnostic/dataset_2_dimension_inventory.csv` | Diagnostic CSV | Unique counts, missing, top values per column |
| `outputs/dataset_2_diagnostic/dataset_2_missingness.csv` | Diagnostic CSV | Missing count and % per column |
| `outputs/dataset_2_diagnostic/dataset_2_grain_diagnostic.csv` | Diagnostic CSV | Duplicate counts at each grain level |
| `outputs/dataset_2_diagnostic/dataset_2_coverage_diagnostic.csv` | Diagnostic CSV | Cross-dimension coverage vs theoretical max |
| `outputs/dataset_2_diagnostic/dataset_2_question_feasibility.csv` | Diagnostic CSV | Q27–Q32 feasibility assessment |
| `outputs/dataset_2_diagnostic/dataset_2_diagnostic_report.md` | Report | This document |

## Files Modified
**None.** All existing files are unchanged.

## Protection Confirmations
- ✅ Dataset 1 (`dataset_1_reusable_analytical.csv`) — not modified
- ✅ `scripts/dataset_1_analytics.py` — not modified
- ✅ `scripts/dataset_1_insights.py` — not modified
- ✅ `scripts/dataset_1_narratives.py` — not modified
- ✅ Q1–Q26 outputs — not modified
- ✅ Q27–Q32 analytical CSVs — **not created**
- ✅ Source Dataset 2 — MD5 hash unchanged (read-only)
- ✅ No packages installed

---

## 21. Known Limitations

1. **Industry granularity:** Only two broad PLFS industry bands available — detailed sector-level analysis not possible.
2. **Temporal industry imbalance:** `(014, 016, 017 , 02-99)` missing from 2022–2023, creating an unbalanced panel for industry comparisons.
3. **Secondary measures:** Estimated Persons (33.3% missing) and Sample Workers (16.7% missing) cannot be used to reconstruct the primary percentage measure.
4. **Label cleaning required:** Irregular whitespace in `(014, 016, 017 , 02-99)` must be standardised before analysis.
5. **Reusable analytical layer:** Not yet created — pending data contract approval and cleaning step.

---

*Diagnostic performed 2026-10-02. Source file not modified. All findings are observed facts from the actual Dataset 2 source.*
