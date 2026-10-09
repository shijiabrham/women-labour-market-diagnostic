# Phase 7.1 — Machine Learning / Predictive Analysis Feasibility and Design Review

**Project:** Women's Labour Market Diagnostic in India  
**Phase:** 7.1 — Feasibility and Design Review Only  
**Date:** 2026-10-07  
**Status:** AWAITING USER APPROVAL BEFORE PHASE 7.2

---

## 1. Executive Conclusion

The available data support **one clearly defensible ML problem** with genuine incremental value over Phases 4–6. Three additional formulations are plausible but less compelling. Dataset 2 is not suitable as the primary modelling target.

The recommended formulation is:

> **Regression: predict the female–male LFPR gap at the State × Year × Area_Type × Education level, using Education, Area_Type, and Year as primary structural predictors.**

This adds analytical value that Phases 4–6 do not supply: it quantifies the **relative predictive contribution** of each structural dimension simultaneously and reveals **interaction effects** (e.g., whether the education gradient of the gender gap differs by area type or changes across years) that the Friedman and Wilcoxon tests cannot capture.

**Final recommendation: B — PROCEED WITH CONDITIONS.**

---

## 2. Dataset Suitability Assessment

### Dataset 1

| Property | Value |
|----------|-------|
| Total rows | 22,650 |
| Modelling grain | State × Year × Gender × Area_Type × Education |
| Unique State–Year contexts | 252 (36 states × 7 years) |
| Outcome variables available | LFPR, WPR, Unemployment_Rate |
| Structural completeness | Complete — all 36 states observed in all 7 years |
| Repeated-measures structure | Strong — same state appears in 7 years |
| Between-state ICC for female LFPR | ≈ 0.66 (high) |
| Between-state ICC for female–male LFPR gap | ≈ 0.24 (moderate) |
| Year–LFPR correlation | 0.43 (non-trivial temporal trend) |
| LFPR extreme values (0 or 100) | Present — 156 zeros, 131 at 100 in female block |

**Suitability: HIGH.** Dataset 1 is well-structured for supervised regression, subject to panel-aware validation.

### Dataset 2

| Property | Value |
|----------|-------|
| Total rows | 31,080 |
| Modelling grain | State × Year × Gender × Area_Type × Industry × Enterprise_Type |
| Primary outcome | Percentage_Engaged per enterprise type |
| Compositional constraint | Shares within each State–Year–Gender–Industry group sum to ~100 % |
| Structural gap | Industry `(014, 016, 017, 02-99)` absent in 2022–2023 |
| No education dimension | Cannot link to education predictor without collapsing D1 |
| Cross-dataset join value | Corr(Female LFPR, Govt_Pct) = 0.078 — negligible |

**Suitability: LOW for primary ML target.** Compositional constraints, structural gaps, and absence of education make Dataset 2 a poor primary modelling target.

---

## 3. Candidate ML Problem Formulations

### Formulation 1 — Regression: Predict Female LFPR

| Criterion | Assessment |
|-----------|------------|
| **Target** | Female LFPR (continuous, 0–100) |
| **Predictors** | Education (8 levels), Area_Type, Year, State |
| **Modelling unit** | State × Year × Area_Type × Education (female only) |
| **Sample size** | 4,032 rows; 252 independent State–Year contexts |
| **Repeated-measures risk** | HIGH — ICC ≈ 0.66; state identity dominates the target |
| **Temporal leakage risk** | HIGH — Year is strongly correlated with LFPR (r = 0.43) |
| **State memorisation risk** | HIGH — model trained on 35 states may learn state-level means rather than structural patterns |
| **Leakage** | WPR and Unemployment_Rate must be excluded (collinear with LFPR) |
| **Incremental value over Phase 6** | LOW-MODERATE — Phase 6 already establishes education, area, and year effects individually |
| **Verdict** | Plausible but the strong state-level ICC means the model primarily learns *which state* rather than *what structural factors*. |

---

### Formulation 2 — Regression: Predict the Female–Male LFPR Gap *(Recommended)*

| Criterion | Assessment |
|-----------|------------|
| **Target** | LFPR_female − LFPR_male at State × Year × Area_Type × Education grain |
| **Predictors** | Education (8 levels), Area_Type (Rural/Urban), Year; State as grouping variable only |
| **Modelling unit** | State × Year × Area_Type × Education (gender-matched pairs) |
| **Sample size** | 4,016 rows; 252 unique State–Year contexts; 16 rows per context |
| **Target distribution** | Mean = −38.22, SD = 20.57; range −100 to +100 pp |
| **Between-state ICC for gap** | ≈ 0.24 (substantially lower than for raw LFPR) |
| **State memorisation risk** | MODERATE-LOW — within-state gender differencing partially removes state fixed effects |
| **Temporal leakage risk** | PRESENT — mitigated by using Year as explicit predictor and time-based CV |
| **Leakage** | LFPR_female and LFPR_male cannot both be predictors; WPR and UR excluded |
| **Incremental value over Phase 6** | **HIGH** — see Section 13 |
| **Verdict** | **Recommended.** Lower ICC makes generalisation more feasible. Target is analytically richer. Result extends Phase 6 findings in a meaningful and new direction. |

---

### Formulation 3 — Binary Classification: High vs Low Female LFPR

| Criterion | Assessment |
|-----------|------------|
| **Target** | Binary: female LFPR above/below national median (35.7 %) |
| **Class balance** | Near-balanced: 1,001 / 2,008 above median |
| **Repeated-measures risk** | HIGH — same state will be in the same class across most years |
| **Temporal leakage** | HIGH — the national median shifts over time, making the label temporally unstable |
| **Incremental value over Phase 6** | LOW — reproduces what Phase 3/4 descriptive maps already show |
| **Verdict** | Not recommended. The threshold is arbitrary, the label is unstable, and the result reproduces existing knowledge. |

---

### Formulation 4 — Regression Using D2 Enterprise Features as Predictors of Female LFPR

| Criterion | Assessment |
|-----------|------------|
| **Idea** | Aggregate D2 enterprise-type shares at State × Year; join to D1 as predictors |
| **Predictive value** | Corr(female LFPR, Govt_Pct) = 0.078 — near zero |
| **Compositional constraint** | Enterprise shares sum to ~100 %; cannot be treated as independent predictors |
| **Structural gap** | `(014, 016, 017, 02-99)` absent in 2022–2023 limits temporal coverage |
| **Verdict** | Not recommended as primary formulation. D2 features may appear as supplementary predictors in Formulation 2 only, with the compositional limitation stated. |

---

### Formulation 5 — Predict Unemployment Rate Gender Gap

| Criterion | Assessment |
|-----------|------------|
| **Target** | Female UR − Male UR at Education grain |
| **Repeated-measures risk** | HIGH |
| **Target distribution** | Right-skewed; clusters near zero at low education |
| **Incremental value over Phase 6** | LOW-MODERATE — Phase 6 F6 already establishes the Gender × Education interaction on unemployment with Friedman test |
| **Verdict** | Possible secondary analysis but not the primary ML formulation. |

---

## 4. Comparative Feasibility Table

| Criterion | F1: Female LFPR | **F2: Gender Gap** | F3: Binary LFPR | F4: D2+D1 Join | F5: UR Gap |
|-----------|:-:|:-:|:-:|:-:|:-:|
| Target is analytically meaningful | ✔ | **✔✔** | ✗ | ✔ | ✔ |
| Adds value beyond Phase 6 | Moderate | **High** | Low | Low | Low–Moderate |
| Between-state ICC manageable | ✗ (0.66) | **✔ (0.24)** | ✗ | n/a | ✗ |
| Temporal leakage controlled | Partial | **Partial** | ✗ | Partial | Partial |
| State memorisation risk | High | **Moderate** | High | High | High |
| Clean leakage boundary | ✔ | **✔** | ✗ (unstable label) | Partial | ✔ |
| Interpretability for capstone | High | **High** | Low | Low | Moderate |
| **Overall feasibility** | B | **A** | C | C | B |

---

## 5. Recommended ML Formulation

> **Regression: Predict the female–male LFPR gap (in percentage points) using Education, Area_Type, and Year as structural predictors, with State as a panel grouping variable used only in validation.**

### What this formulation tests

Phase 6 established — separately — that the gender gap exists universally (F2), that education affects female LFPR non-monotonically (F5), and that the rural–urban gap widened (F4). These findings were each established one dimension at a time.

The ML formulation asks: **When education level, area type, and year all vary simultaneously, which dimension contributes most to predicting the size of the gender LFPR gap? And how do they interact?**

This is a genuine open question not answered by any Phase 4–6 analysis.

---

## 6. Target Definition

| Item | Specification |
|------|--------------|
| **Target variable** | `gap = LFPR_female − LFPR_male` |
| **Grain** | State × Year × Area_Type × Education (gender-matched pairs) |
| **Type** | Continuous (approximately −100 to +100 pp) |
| **Filter** | Area_Type ∈ {Rural, Urban} (exclude Rural + Urban combined to avoid double-counting); Education ∈ 8 detailed categories |
| **Boundary observations** | LFPR = 0 or 100 rows should be flagged and sensitivity analysis run with/without them |
| **Missing values** | 8 missing LFPR values in female block — these rows will be excluded |

---

## 7. Predictor Definition

| Predictor | Type | Encoding | Notes |
|-----------|------|----------|-------|
| `Education` | Categorical (8 levels) | Ordinal integer (0–7) or one-hot | Ordinal preserves the education-level ordering |
| `Area_Type` | Binary (Rural / Urban) | 0 / 1 | Rural = 0, Urban = 1 |
| `Year` | Ordinal integer 2017–2023 | As-is or z-scored | Captures national temporal trend |
| `State` | Categorical (36 levels) | **Grouping variable only** in primary analysis | See leakage warning below |

> [!WARNING]
> **State as predictor.** If State is included as a predictor with training-set mean encoding, the model learns state-level mean gaps and the result is in-sample only. State must be **excluded** from the primary predictor set to permit LOSO generalisation testing. A secondary in-sample analysis with State included is permitted but must be clearly labelled.

**Variables explicitly excluded:**

- `LFPR_Female` and `LFPR_Male` (jointly — only their difference is the target)
- `WPR` (all genders — derived from LFPR in the same source)
- `Unemployment_Rate` (same source wave; partially collinear)
- Any aggregate already computed from the gap itself

---

## 8. Unit of Modelling

| Item | Value |
|------|-------|
| **Row** | State × Year × Area_Type × Education gender-matched pair |
| **Effective independent units** | 252 unique State–Year contexts |
| **Rows per independent context** | 16 (8 education levels × 2 area types) |
| **Total modelling rows** | ~4,016 complete cases |

> [!NOTE]
> The 4,016 rows share only 252 independent contexts. All 16 rows within a State–Year context are structurally correlated. The validation design must respect this structure.

---

## 9. Leakage Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Target self-inclusion (LFPR_F, LFPR_M) | Critical | Exclude both from predictor set |
| Row-level naive split | High | Use LOSO or time-based CV; never random row split |
| WPR and UR collinearity | High | Exclude from predictor set |
| State mean-encoding leakage | Medium | Use leave-one-out encoding strictly within each training fold |
| Temporal leakage | Medium | Time-based split as secondary validation |
| D2 join leakage | Low (if used) | Join only at State × Year level with same-year matching |

---

## 10. Validation Strategy

### Core problem

With between-state ICC ≈ 0.24, a random row-level split assigns rows from the same state to both train and test. The model has already seen the state's structural context, producing **optimistically biased generalisation estimates**.

### Primary: Leave-One-State-Out Cross-Validation (LOSO)

| Item | Specification |
|------|--------------|
| **Method** | 36-fold leave-one-state-out CV |
| **Training set (per fold)** | 35 states × 7 years × 16 rows ≈ 3,920 rows |
| **Test set (per fold)** | 1 state × 7 years × 16 rows = 112 rows |
| **State in predictor set** | **No** — State is unknown for held-out state |
| **What it answers** | Can the model generalise to a new geographic context it has never seen? |

This is the most defensible design given the capstone's diagnostic focus on state-level heterogeneity.

### Secondary: Temporal Split

| Item | Specification |
|------|--------------|
| **Train** | Years 2017–2021 (~2,880 rows) |
| **Test** | Years 2022–2023 (~1,152 rows) |
| **What it answers** | Do patterns from earlier years generalise to later years? |
| **Limitation** | 2022–2023 spans the post-COVID recovery; structural shifts may make this an unusually challenging test set |

### Strategy assessment

| Strategy | Leakage risk | Appropriate? |
|----------|-------------|:---:|
| A. Random row-level split | **HIGH** | ✗ |
| B. State-grouped LOSO | Low | **✔ Primary** |
| C. Time-based split | Low | **✔ Secondary** |
| D. State + time block | Low but very small test set | Exploratory only |
| E. Stratified K-fold by state | Medium | Avoid |

---

## 11. Recommended Model Family

Given: continuous target, ~4,016 rows, confirmed non-linear education gradient (F5), interaction effects as primary question, and interpretability required.

### Primary: Gradient Boosted Trees (XGBoost or LightGBM)

| Property | Assessment |
|----------|------------|
| Handles non-linearity | Yes — captures the non-monotone education gradient |
| Captures interactions | Yes — tree splits reveal conditional effects |
| Feature importance | SHAP values provide observation-level and global explanations |
| Interpretability | High via SHAP, partial dependence plots, ICE curves |
| Sample size requirement | Low — suitable for ~4,000 rows |
| Regularisation | Built-in via learning rate, max depth, subsampling |
| Packages required | `xgboost` or `lightgbm`, `shap` |

### Baseline: Ridge Regression

| Property | Assessment |
|----------|------------|
| Interpretability | Highest — coefficients directly quantify each predictor's contribution |
| Non-linearity | Requires explicit interaction/polynomial terms |
| Regularisation | L2 (Ridge) |
| Packages required | `scikit-learn` |

> [!TIP]
> The comparison between Ridge and gradient boosting is itself analytically valuable: if they perform similarly, linear structure adequately captures the gap pattern (confirming and simplifying Phase 6 findings). If boosting substantially outperforms Ridge, meaningful non-linear interactions are present beyond what Phase 6 tests captured.

---

## 12. Evaluation Metrics

| Metric | Rationale |
|--------|-----------|
| **RMSE** (pp) | Primary metric — interpretable in the same units as the gap |
| **MAE** (pp) | Less sensitive to extreme boundary values (LFPR = 0 or 100) |
| **R²** | Proportion of gap variance explained — comparable across models |
| **Out-of-state R²** | Primary validation metric — measures genuine generalisation |
| **SHAP feature importance** | Primary analytical output — reveals which dimension drives gap prediction |
| **Partial dependence plots** | Show how predicted gap changes across education levels controlling for other predictors |

> [!IMPORTANT]
> If out-of-state R² is near zero despite good in-sample R², this is itself an analytically meaningful finding: it confirms that state fixed effects dominate and structural predictors (education, area) do not generalise. This should be reported as a capstone finding, not treated as a model failure.

---

## 13. Expected Analytical Contribution Beyond Phases 4–6

| Phase 6 finding | What ML adds |
|-----------------|-------------|
| F2: Gap is universal and large (mean −41 pp) | Reveals which combinations of education, area, and year predict *narrower* vs *wider* gaps — Phase 6 could not do this simultaneously |
| F4: Rural–Urban gap widened | Quantifies whether Area_Type contributes *independently* of Education and Year in a multivariate model |
| F5: Education gradient is non-monotone in female LFPR | Tests whether the same non-monotonicity appears in the gender *gap* and whether it is more pronounced in Rural or Urban areas |
| F6: Gender × Education pattern in unemployment | Complements by showing if the education pattern holds for *participation*, not just unemployment |
| F8: Larger LFPR gains among lower-educated women | Year × Education interaction in the model can confirm or contradict whether this differential is narrowing the gap |

**Specific new question Phase 7 can answer:**

> *"Controlling for year and area type simultaneously, which education levels most strongly predict a narrower or wider gender LFPR gap, and has this predictive relationship changed between 2017 and 2023?"*

This question is not answered by any Phase 4–6 analysis.

---

## 14. Risks and Limitations

| Risk | Severity | Mitigation |
|------|----------|------------|
| State memorisation | High | LOSO validation; State excluded from primary predictor set |
| Small number of independent units (252) | Medium | Use interpretable, regularised models; report confidence intervals |
| Boundary LFPR values (0 and 100) | Medium | Sensitivity analysis with and without boundary rows |
| No causal interpretation | High (misinterpretation risk) | All findings must be described as predictive associations |
| Year as trend proxy | Medium | Explicit Year predictor; temporal CV to test generalisation |
| Compositional D2 data (if used) | High | Not used as primary predictor; if supplementary, limitation stated explicitly |
| Package installation required | Low | Confirm `scikit-learn`, `xgboost`/`lightgbm`, `shap` availability before Phase 7.2 |

---

## 15. Final Phase 7 Recommendation

### Verdict: **B — PROCEED WITH CONDITIONS**

A defensible ML problem exists. The gender-gap regression formulation is analytically motivated, adds genuine incremental value over Phase 6, and can be implemented with the existing data structure.

### Conditions for proceeding to Phase 7.2

1. **Validation must be LOSO** as primary; time-based split (2017–2021 / 2022–2023) as secondary. A random row-level split must not be used.
2. **State must be excluded from the predictor set** in the primary LOSO analysis. A secondary in-sample analysis with State may be included but must be clearly labelled.
3. **LFPR_female, LFPR_male, WPR, and Unemployment_Rate must be excluded** from the predictor set.
4. **Ridge regression must be implemented as a baseline** before gradient boosting.
5. **SHAP feature importance is required** — the primary deliverable of Phase 7 is interpretive, not predictive.
6. **No causal language** may be used in any Phase 7 output.
7. **Dataset 2 should not be the primary modelling input.** It may provide one supplementary State × Year level predictor if desired, with the compositional limitation explicitly noted.

### Exact specification for Phase 7.2 if approved

| Item | Specification |
|------|--------------|
| **Problem type** | Regression |
| **Target** | `LFPR_Female − LFPR_Male` at State × Year × Area_Type × Education grain |
| **Primary predictors** | Education (8 categories, ordinal encoded), Area_Type (Rural/Urban, binary), Year (numeric) |
| **Secondary predictors (in-sample only)** | State (36 categories, leave-one-out mean encoded within fold) |
| **Modelling rows** | ~4,016 complete-case rows |
| **Models** | 1. Ridge regression (baseline); 2. Gradient boosted trees (main) |
| **Primary validation** | Leave-one-state-out CV (36 folds) |
| **Secondary validation** | Temporal split: train 2017–2021, test 2022–2023 |
| **Primary evaluation metrics** | RMSE (pp), MAE (pp), out-of-state R² |
| **Primary analytical output** | SHAP feature importance + partial dependence plots |
| **Output directory** | `outputs/phase_7_ml/` |

---

*Phase 7.1 feasibility and design review complete. No models were trained. No data were modified. No Phase 1–6 outputs were altered.*
