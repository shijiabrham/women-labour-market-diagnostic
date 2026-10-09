# Q18-Q26 Methodological Specification

## Source
**Reusable analytical layer:** `outputs/phase_4_eda/dataset_1_reusable_analytical.csv`
**Grain:** State × Year × Gender × Area_Type × Education (22 650 rows, 8 columns)

## Aggregation Principles
- When a dimension is **collapsed**, the arithmetic mean of available non-missing indicator values is used.
- Missing (NaN) values are excluded from the mean. If all values in a group are NaN, the result is NaN.
- Zero is a valid observation; it is included in the mean.
- No population weights exist in Dataset 1. All means are **unweighted analytical means**.
- Existing source aggregate categories are **always preferred** over constructing a new aggregate:

  | Source aggregate | Meaning | Usage |
  |-----------------|---------|-------|
  | `Persons` (Gender) | All persons, as reported | Used when no gender filter needed |
  | `Rural + Urban` (Area_Type) | Combined area, as reported | Used as 'overall' area filter for Q18-Q24 |
  | `All` (Education) | All education levels, as reported | Used as 'overall' education filter for Q21-Q26 |

## Methodological Decision Table

| Q | Question | Indicator | Gender filter | Area_Type treatment | Education treatment | Year treatment | State treatment | Output grain |
|---|---------|-----------|---------------|---------------------|---------------------|----------------|-----------------|-------------|
| Q18 | Female vs Male LFPR by Education | LFPR | Female, Male | Filter: Rural + Urban (source aggregate — avoids artificial cross-area mean) | Filter: 8 detailed categories; exclude All, Secondary & Above | Retain (2017-2023) | Collapse: unweighted mean across 36 states | Year × Education (wide: Female | Male | FM_Gap) |
| Q19 | Female vs Male WPR by Education | WPR | Female, Male | Filter: Rural + Urban | Filter: 8 detailed categories | Retain | Collapse: unweighted mean | Year × Education (wide) |
| Q20 | Female vs Male Unemployment by Education | Unemployment_Rate | Female, Male | Filter: Rural + Urban | Filter: 8 detailed categories | Retain | Collapse: unweighted mean | Year × Education (wide) |
| Q21 | Gender differences by Rural vs Urban | LFPR, WPR, UR | Female, Male | Filter: Rural, Urban (exclude Rural+Urban — this IS the comparison) | Filter: All (source aggregate — avoids 10-edu collapse) | Retain (2017-2023) | Collapse: unweighted mean | Year × Area_Type (wide: Female | Male | FM_Gap per indicator) |
| Q22 | Women's LFPR trend 2017-2023 | LFPR | Female | Filter: Rural + Urban (source aggregate) | Filter: All (source aggregate) | Retain (primary dimension) | Collapse: unweighted mean | Year (+ cumulative change vs 2017) |
| Q23 | Women's WPR trend 2017-2023 | WPR | Female | Filter: Rural + Urban | Filter: All | Retain | Collapse: unweighted mean | Year (+ cumulative change vs 2017) |
| Q24 | Women's Unemployment trend 2017-2023 | Unemployment_Rate | Female | Filter: Rural + Urban | Filter: All | Retain | Collapse: unweighted mean | Year (+ cumulative change vs 2017) |
| Q25 | Education groups: 2017-2023 changes | LFPR, WPR, UR | Female | Filter: Rural + Urban | Filter: 8 detailed categories (exclude All, Secondary & Above) | Filter: 2017 and 2023 only (endpoint comparison) | Collapse: unweighted mean | Education × Indicator (Value_2017 | Value_2023 | Abs_Change | Pct_Change) |
| Q26 | Rural vs Urban temporal patterns (women) | LFPR, WPR, UR | Female | Filter: Rural, Urban (exclude Rural+Urban — this IS the comparison) | Filter: All (source aggregate) | Retain (primary dimension) | Collapse: unweighted mean | Year (wide: Rural | Urban | RU_Gap per indicator + change vs 2017) |

## Rationale for Dimension Treatment

### Why Rural + Urban is used as the 'overall' filter in Q18-Q24
- `Rural + Urban` is an existing source-provided aggregate category.
- Using it avoids constructing an artificial cross-area mean from Rural and Urban rows.
- This ensures the values reflect the same definitional scope as the source data.

### Why `All` is used as the 'overall' education filter in Q21-Q26
- `All` is an existing source-provided aggregate education category.
- Using it avoids collapsing 10 education rows with an unweighted mean across heterogeneous education groups.

### Why State is collapsed in all Q18-Q26 questions
- Q18-Q26 are framed as **national-level** comparisons (by Gender, Education, Area, or Year).
- State-level disaggregation is available in the reusable layer and can be accessed for future state-specific questions.

### Why Year is retained in Q18-Q21 and Q22-Q26
- Retaining Year preserves the full 2017-2023 temporal dimension.
- This avoids suppressing inter-year variation and makes the outputs usable for trend analysis.

### Dynamic computations (not stored in reusable layer)
| Derived measure | Formula | Questions used |
|----------------|---------|----------------|
| Female-Male Gap | Female − Male | Q18, Q19, Q20, Q21 |
| Rural-Urban Gap | Rural − Urban | Q26 |
| Absolute Change vs 2017 | Value_Year − Value_2017 | Q22, Q23, Q24, Q26 |
| Percentage Change vs 2017 | (AbsChange / Value_2017) × 100; NaN if Value_2017=0 or missing | Q22, Q23, Q24, Q25, Q26 |
| Absolute Change 2017-2023 | Value_2023 − Value_2017 | Q25 |

## Protection
- Q1-Q17 scripts, CSVs, validation reports, and narratives were not modified.
- Source Dataset 1 was not modified.
- Reusable analytical layer was not modified.
- No packages were installed.
- Dataset 2 was not accessed.

---
*Specification generated automatically.*