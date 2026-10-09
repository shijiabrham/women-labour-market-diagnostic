# Phase 7.2 — Machine Learning Implementation & Evaluation Report

**Project:** Women’s Labour Market Diagnostic in India  
**Phase:** 7.2 — Machine Learning Implementation  
**Status:** COMPLETE  
**Primary Question:** Controlling for year and area type simultaneously, which education levels are most strongly associated with a narrower or wider gender LFPR gap, and does this predictive relationship change over time?

---

## 1. Executive Summary & Objective

Phase 7.2 operationalises the approved analytical design from Phase 7.1. The objective is to evaluate whether macro-structural predictors (**Education**, **Area_Type**, and **Year**) can predict variation in the **Female–Male LFPR Gap** in unseen Indian States under strict **Leave-One-State-Out (LOSO) Cross-Validation**.

The analysis is strictly predictive/associational. It does not estimate causal effects or policy impacts.

### Key Empirical Findings from Phase 7.2:
1. **Predictive Performance on Unseen States:** Under 36-fold LOSO validation, Ridge Regression achieves an out-of-fold $R^2 = 0.139$ (MAE = 15.98 pp, RMSE = 22.48 pp). Gradient Boosting achieves an out-of-fold $R^2 = 0.155$ (MAE = 15.70 pp, RMSE = 22.27 pp), relative to the baseline training-mean model ($R^2 = -0.008$, MAE = 18.05 pp, RMSE = 24.33 pp).
2. **Modest Non-linear Gain:** Gradient Boosting yields an incremental $R^2$ improvement of only $+0.016$ (+1.6 percentage points of variance explained) over linear Ridge regression, demonstrating that the structural relationship between education, area type, temporal trend, and the gender gap is predominantly linear and additive.
3. **Primary Predictive Predictors:** Across both models, the primary predictors explaining variation in the gender gap are:
   - **Temporal Trend (Year):** Associated with a narrowing of the gap over time ($\beta \approx +3.72$ pp per standard deviation increase in Year, or ~1.85 pp per year).
   - **Education Categories:** Education levels at *Middle* ($\beta = -24.93$ pp relative to Diploma) and *Literate & Upto Primary* ($\beta = -23.97$ pp) are associated with the widest gender penalty, whereas *Post Graduate & Above* ($\beta = -3.94$ pp) and *Diploma* are associated with the narrowest gap.
   - **Area Type:** Urban residence is associated with a wider gender gap ($\beta = -6.57$ pp relative to Rural).
4. **Interpretation of Explained and Unexplained Variance:** The model explains 15.5% of out-of-fold variation in the gender LFPR gap for unseen States ($R^2 = 0.155$). The remaining variation is not explained by Education, Area_Type, and Year in the current model, indicating that additional contextual, institutional, or state-specific factors not captured by these demographic predictors may account for the substantial majority of state-level variation.

---

## 2. Target Definition & Data Preparation

### 2.1 Target Construction
The modelling target is defined as:
$$\text{Target} = \text{LFPR}_{\text{Female}} - \text{LFPR}_{\text{Male}}$$

- Constructed at the identical unit: $\text{State} \times \text{Year} \times \text{Area\_Type} \times \text{Education}$.
- Source: `outputs/phase_4_eda/dataset_1_reusable_analytical.csv`.
- Only matched **Female** and **Male** pairs within the same stratum were retained.
- **Persons** observations were strictly excluded.
- Neither Female LFPR, Male LFPR, WPR, nor Unemployment Rate were used as predictors, completely avoiding target and collinearity leakage.

### 2.2 Subpopulation, Area Type Specification & Sample Count Verification
- **Area Types Included:** Exactly 2 categories: `Rural` and `Urban`.
  - **Methodological Note on Exclusion of `Rural + Urban`:** In Dataset 1, `Rural + Urban` is a composite source aggregation of `Rural` and `Urban`. Including all three would double-count observations within the same state, year, and education tier, distorting cross-validation weights. Hence, the model intentionally includes only the mutually exclusive sectors (`Rural` and `Urban`) as designed in Phase 7.1.
- **Education Levels (8 Detailed Categories):**
  1. *Not Literate*
  2. *Literate & Upto Primary*
  3. *Middle*
  4. *Secondary*
  5. *Higher Secondary*
  6. *Diploma/ Certificate Course* (reference category in encoding)
  7. *Graduate*
  8. *Post Graduate & Above*
- **Sample Arithmetic & Verification:**
  - State–Year Contexts: $36 \text{ States} \times 7 \text{ Years (2017–2023)} = 252 \text{ contexts}$.
  - Observations per Context: $2 \text{ Area Types (Rural, Urban)} \times 8 \text{ Detailed Education Levels} = 16 \text{ observations/context}$.
  - Theoretical Matched Observations: $252 \times 16 = 4,032 \text{ rows}$.
  - Source Missingness: Exactly 8 rows in Chandigarh (Rural sector across 8 education levels in 2023) exhibited structural missingness in LFPR.
  - Final Complete Modelling Sample: $4,032 - 8 = \mathbf{4,024 \text{ observations}}$ across 36 States and Union Territories.
  - Target Distribution: Mean = $-39.95$ pp, Median = $-43.10$ pp, Standard Deviation = $24.23$ pp (Range: $-100.00$ to $+100.00$ pp).

---

## 3. Validation Design: Leave-One-State-Out (LOSO)

### 3.1 Methodological Rationale
A naive random row-level split (e.g. `train_test_split`) violates the independent sampling assumption because rows within the same State share unobserved state-level governance, industrial composition, and cultural norms. Such a split would result in pseudo-replication and severe data leakage.

To test true **out-of-sample geographic generalisability**, we implement **Leave-One-State-Out (LOSO) Cross-Validation**:
- **Total Folds:** 36.
- **Procedure per Fold:**
  1. Hold out all rows belonging to 1 State (112 observations for 35 states; 104 observations for Chandigarh).
  2. Train models exclusively on the remaining 35 States (~3,912 to 3,920 rows).
  3. All data preprocessing (StandardScaler for Year, OneHotEncoder for Education and Area_Type) is fit strictly on the training fold.
  4. Generate predictions for the held-out State.
- Aggregate all out-of-fold predictions ($N = 4,024$) to evaluate global performance metrics.

---

## 4. Models Implemented

### 4.1 Model 1: Baseline (Training-Fold Mean)
- Predicts the average gender gap of the 35 training states for every observation in the held-out state.
- Represents the performance of a naive spatial extrapolator lacking educational, spatial, or temporal information.

### 4.2 Model 2: Ridge Regression (L2 Regularised Linear Model)
- Predictors:
  - `Education`: One-Hot Encoded (8 categories; drop='first', reference = *Diploma/ Certificate Course*).
  - `Area_Type`: One-Hot Encoded (reference = *Rural*, indicator = *Urban*).
  - `Year`: Standardised numeric variable ($\mu=0, \sigma=1$ fitted per training fold).
- Regularisation parameter: $\alpha = 1.0$.

### 4.3 Model 3: Gradient Boosting Regressor (Nonlinear Tree-Based Model)
- Architecture: 100 boosting stages, learning rate = 0.1, maximum depth = 3.
- Evaluates whether interaction terms (e.g., Education $\times$ Area_Type, Education $\times$ Year) or non-linear functions provide predictive leverage over the linear baseline.

---

## 5. Model Performance & Evaluation

### 5.1 Out-Of-Fold Performance Table (36 Folds, $N = 4,024$)

| Model | Validation Method | Total Folds | Observations | MAE (pp) | RMSE (pp) | Out-of-Fold $R^2$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Training Mean)** | Leave-One-State-Out | 36 | 4,024 | 18.05 | 24.33 | **-0.008** |
| **Ridge Regression** | Leave-One-State-Out | 36 | 4,024 | 15.98 | 22.48 | **0.139** |
| **Gradient Boosting Regressor** | Leave-One-State-Out | 36 | 4,024 | 15.70 | 22.27 | **0.155** |

*Note: All metrics computed strictly on out-of-fold predictions. A negative $R^2$ for the baseline indicates that predicting the grand training mean across states performs slightly worse on held-out states than the held-out state's own mean.*

### 5.2 State-Level Variation in Predictive Accuracy
Examining individual fold $R^2$ scores reveals substantial heterogeneity in how well national structural patterns generalise across states:
- **Strong Generalisation ($R^2 > 0.35$):** States like *Odisha* ($R^2 = 0.558$), *Jammu and Kashmir* ($R^2 = 0.406$), *Assam* ($R^2 = 0.366$), and *Rajasthan* ($R^2 = 0.335$) exhibit gap structures that align closely with the national education and rural-urban profile.
- **Weak or Negative Generalisation ($R^2 < 0.0$):** States like *Haryana* ($R^2 = -1.461$), *Jharkhand* ($R^2 = -0.451$), *Tamil Nadu* ($R^2 = -0.399$), and *Uttar Pradesh* ($R^2 = -0.398$) have state-specific gender gaps that deviate sharply from the national baseline, reflecting unique local labour market institutions.

---

## 6. Model Interpretation & Predictive Importance

### 6.1 Feature Importance & Ridge Coefficients

| Feature Name | Ridge Coefficient ($\beta$) | GBR Feature Importance | Associational Direction with Female-Male LFPR Gap |
| :--- | :---: | :---: | :--- |
| **Year (Standardised)** | $+3.719$ | 0.1870 | **Narrowing Gap:** Gap narrows by ~1.85 pp per calendar year |
| **Education: Literate & Upto Primary** | $-23.973$ | 0.1859 | **Widening Gap:** Substantially wider gap than Diploma holder |
| **Area Type: Urban** | $-6.567$ | 0.1756 | **Widening Gap:** Urban gap is ~6.57 pp wider than Rural |
| **Education: Middle** | $-24.926$ | 0.1695 | **Widening Gap:** Widest gender gap among all education levels |
| **Education: Post Graduate & Above** | $-3.944$ | 0.0955 | **Narrowing Gap:** Gap is close to Diploma level |
| **Education: Secondary** | $-17.245$ | 0.0651 | **Widening Gap:** Moderate gap penalty |
| **Education: Not Literate** | $-12.794$ | 0.0432 | **Moderate Gap:** Narrower gap penalty than Middle/Primary |
| **Education: Graduate** | $-15.625$ | 0.0420 | **Widening Gap:** Noticeable gap penalty despite higher education |
| **Education: Higher Secondary** | $-15.135$ | 0.0362 | **Widening Gap:** Moderate gap penalty |

*(Note: Reference category for Education is 'Diploma/ Certificate Course'; Reference category for Area Type is 'Rural'.)*

### 6.2 Substantive Insights from Model Parameters:
1. **The U-Shaped Education Profile in the Gender Gap:**
   - The widest gender gap occurs at low-to-intermediate schooling levels: *Middle* ($-50.72$ pp actual mean gap) and *Literate & Upto Primary* ($-49.77$ pp actual mean gap).
   - In contrast, technical and advanced education categories exhibit significantly narrower gender gaps: *Diploma* ($-25.52$ pp actual mean gap) and *Post Graduate & Above* ($-29.70$ pp actual mean gap).
   - *Not Literate* women have a narrower gender gap ($-38.57$ pp) than women with primary or middle schooling, reflecting subsistence agricultural labour participation among less-educated rural women.
2. **The Urban Gender Penalty:**
   - Urban environments are associated with an additional $-6.57$ pp penalty in the gender gap compared to rural areas. This reflects higher male participation and lower female informal participation in urban centres.
3. **The Temporal Trend:**
   - Year is the single most influential predictive feature in Gradient Boosting (importance = 0.1870). Over the 2017–2023 observation window, the gender gap has systematically narrowed across all education levels by approximately $3.72$ pp per standard deviation increase in time.

---

## 7. Comparative Assessment: What Does ML Add Beyond Phase 6?

Phase 6 established bivariate and omnibus differences using non-parametric tests:
- **F2:** Confirmed that Female LFPR is significantly lower than Male LFPR within every state and year ($p < 0.001$).
- **F4:** Confirmed that the Rural-Urban gap widened over time ($p < 0.001$).
- **F5 & F8:** Confirmed significant differences in LFPR across education levels ($p < 0.001$) and differential change over time.

### Incremental Contributions of Phase 7:
1. **Multivariate Decomposition:** Phase 6 examined education and urbanization separately. Phase 7 demonstrates that **even after controlling simultaneously for urbanization and temporal trajectory, education differences contribute independently to explaining the gender gap**.
2. **Quantification of Relative Importance:** Phase 7 ranks structural features by predictive leverage: **Year (0.187)** and **Primary/Middle Education (~0.186)** contribute almost equally to predictive variance, followed closely by **Urbanization (0.176)**.
3. **Bounds on Generalisability (The Macro Ceiling):** By demonstrating that models achieve an out-of-fold $R^2$ of only ~0.155 across unseen states, Phase 7 establishes that **national educational, urbanization, and temporal trends explain approximately 15.5% of geographic variation in the gender gap**. The remaining variation is not explained by Education, Area_Type, and Year in the current model, indicating that additional contextual, structural, or state-specific factors are relevant.
4. **Validation of Model Linearity:** The near-equivalence between Ridge ($R^2 = 0.139$) and Gradient Boosting ($R^2 = 0.155$) shows that complex higher-order interactions add marginal predictive utility; the structural determinants of the gender gap operate largely additively.

---

## 8. Limitations and Methodological Safeguards

1. **Non-Causal Framework:** All coefficients and feature importances reflect conditional statistical associations. They cannot be interpreted as the causal effect of educational attainment or urban migration on gender gaps.
2. **Absence of Sub-State Covariates:** Predictors are limited to macro demographic aggregates (Education, Area Type, Year). Household income, child care availability, marital status, and caste are absent from the state-level analytical layer.
3. **State-Level Fixed Effects Omission:** State identity was deliberately excluded as a predictor to assess geographic generalisation. Consequently, the model cannot capture state-specific baseline levels, leading to negative fold $R^2$ in states with extreme socio-cultural divergences.
4. **Unweighted Aggregation:** Model observations are unweighted by state population. Large states (e.g. Uttar Pradesh) contribute the same number of observations as small Union Territories (e.g. Lakshadweep).

---

## 9. Conclusion of Phase 7.2

Phase 7.2 successfully implemented, validated, and interpreted the approved machine learning architecture under Leave-One-State-Out cross-validation. The results provide an empirical bridge between the statistical tests of Phase 6 and the broader narrative of the diagnostic: structural features (education, urbanization, time) matter systematically, but state-level institutional context remains the dominant determinant of women's labour market outcomes in India.

Phase 7 is complete and ready for review.
