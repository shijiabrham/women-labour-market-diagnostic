# Phase 7 Forecasting Audit

**Project:** Women’s Labour Market Diagnostic in India  
**Sub-task:** Targeted Methodological Audit of Phase 7 Time-Series Forecasting  
**Audited Artifacts:**
1. `outputs/phase_7_ml/forecasting/phase_7_forecasting_feasibility.md`
2. `outputs/phase_7_ml/forecasting/forecast_results.csv`
3. `scripts/phase_7_forecasting.py`  
**Audit Status:** AUDIT COMPLETE  
**Audit Verdict:** **APPROVED AFTER SPECIFIED CORRECTIONS**

---

## 1. Audit Conclusion

**Verdict: APPROVED AFTER SPECIFIED CORRECTIONS (READY WITH MINOR DOCUMENTATION CORRECTIONS)**

The existing time-series forecasting study and pipeline are methodologically disciplined, mathematically sound, and reproduce cleanly without runtime errors or data leakage. The study correctly enforces that **a scenario must be allowed to fail** (45.6% of candidate scenarios were rejected).

However, before the forecasting outputs can be integrated into the Phase 9 public-facing dashboard, three specific documentation and metadata clarifications are required:
1. **Reconciliation of Scenario vs. Row Counts:** Explicitly document that the 954 rows in `forecast_results.csv` represent the exact total candidate universe ($N = 954$), composed of $235$ `FORECAST_ELIGIBLE`, $284$ `FORECAST_ELIGIBLE_WITH_LIMITATIONS` (totaling $519$ eligible scenarios), and $435$ `FORECAST_NOT_SUPPORTED` scenarios.
2. **Uncertainty Interval Terminology:** Replace the term "80% Prediction Interval" with **"Empirical Uncertainty Interval (80% Nominal)"** to reflect that residual dispersion is estimated across only three rolling validation origins ($n=3$).
3. **National-Level Framing:** Clarify that "National" scenarios represent the **"State-level unweighted analytical mean across 36 States/UTs"**, not an official population-weighted all-India PLFS census estimate.

---

## 2. Eligibility Rule Audit

### A. Internal Consistency & Precedence
The eligibility rules in `scripts/phase_7_forecasting.py` (lines 173–208) are implemented sequentially and deterministically:
1. **Pre-check (Continuity & Completeness):** Any series with missing historical points or $< 5$ annual observations is immediately routed to `FORECAST_NOT_SUPPORTED` (e.g., Rural Chandigarh in 2023).
2. **Pre-check (Detailed Education):** All detailed education categories (`Level == "Education_Detailed"`) are unconditionally routed to `FORECAST_NOT_SUPPORTED` due to small-cell sampling noise.
3. **Indicator-Specific Rules:**
   - **Unemployment Rate:** Evaluated under stricter bounds ($\text{MAE} \le 2.5$ pp). If it meets this threshold, it is routed strictly to `FORECAST_ELIGIBLE_WITH_LIMITATIONS`. It is **never** permitted into unconditional `FORECAST_ELIGIBLE`, accurately reflecting its high cyclicality.
   - **LFPR & WPR:**
     - *Branch 1 (`FORECAST_ELIGIBLE`):* If candidate model achieves strictly positive improvement over Naive baseline ($\text{MAE Improvement} \ge 0.10$ pp) AND out-of-sample $\text{MAE} \le 4.0$ pp.
     - *Branch 2 (`FORECAST_ELIGIBLE_WITH_LIMITATIONS`):* If candidate model does not improve over Naive by $\ge 0.10$ pp, but achieves acceptable low error ($\text{MAE} \le 3.5$ pp).
     - *Branch 3 (`FORECAST_NOT_SUPPORTED`):* If out-of-sample $\text{MAE} > 3.5$ pp.

### B. Findings on Rule Execution
- **Mutually Exclusive:** There is zero contradictory overlap; the `if / elif / else` ladder guarantees that each scenario receives exactly one classification.
- **No Worse-Than-Naive Selections:** In all $284$ scenarios classified as `FORECAST_ELIGIBLE_WITH_LIMITATIONS`, the candidate model MAE is strictly $\le$ Naive MAE (min improvement $= 0.00$ pp, max improvement $= 2.14$ pp). No scenario with a model performing worse than the Naive baseline was classified as eligible.
- **Documentation Refinement:** The written report in Section 10 should clarify this exact precedence ladder so that readers do not perceive ambiguity between the $3.5$ pp and $4.0$ pp thresholds.

---

## 3. Forecast Results Reconciliation

### Resolving the Apparent "519 vs. 954" Discrepancy
The audit traced the exact row structure of `forecast_results.csv`:
- **Total Candidate Scenarios Evaluated:** **954 rows** (one unique row per scenario).
- **Breakdown by Level:**
  - `Education_Detailed` ($N = 288$ rows): 36 States $\times$ 8 Education categories $\times$ Female $\times$ Rural+Urban $\times$ LFPR.
  - `National` ($N = 18$ rows): 3 Indicators $\times$ 2 Genders $\times$ 3 Area Types.
  - `State` ($N = 648$ rows): 36 States $\times$ 3 Indicators $\times$ 2 Genders $\times$ 3 Area Types at `Education = All`.
  - **Total:** $288 + 18 + 648 = 954$ rows.
- **Reconciliation with Reported 519 Scenarios:**
  - $235$ `FORECAST_ELIGIBLE` rows
  - $+ 284$ `FORECAST_ELIGIBLE_WITH_LIMITATIONS` rows
  - **$= 519$ Total Eligible Scenarios** ($54.4\%$ of the 954 candidate scenarios).
  - The remaining $435$ rows ($45.6\%$) are explicitly recorded in the dataset as `FORECAST_NOT_SUPPORTED`, complete with the documented `Eligibility_Reason` and null forecast values.
- **Conclusion:** The 954-row CSV is **completely correct and internally coherent**. The apparent discrepancy was merely a documentation ambiguity (the report text cited the sum of eligible scenarios without explicitly stating that the CSV stores both eligible and unsupported scenarios for complete auditability).

---

## 4. Prediction Interval Audit

### A. Residual Basis & Small-Sample Limitation
- In `scripts/phase_7_forecasting.py`, prediction intervals are constructed as:
  $$\hat{y}_{T+1} \pm 1.282 \times \sigma_{\text{residuals}}$$
- The residual standard deviation $\sigma_{\text{residuals}}$ is computed directly from the **three rolling out-of-sample validation residuals** ($t = 2021, 2022, 2023$).
- Where residual dispersion is $< 1.0$, a minimum half-width clamp of $1.0$ pp is enforced; values are strictly bounded between $0.0\%$ and $100.0\%$.

### B. Methodological Assessment & Recommended Terminology
- Calling this a formal **"80% Prediction Interval"** is statistically over-optimistic because:
  1. A sample of $n = 3$ residuals possesses only 2 degrees of freedom, making precise Gaussian tail estimation theoretically fraught.
  2. The $1.282$ multiplier assumes known residual variance, which underestimates parameter uncertainty under very small samples.
- **Recommended Presentation Action:**
  - Retain the calculation (it provides a valuable, data-driven measure of recent model volatility).
  - Re-label the metric in the UI and documentation as **"Empirical Uncertainty Interval (80% Nominal)"**.
  - Add an inline footnote: *"Uncertainty intervals are empirical bounds based on out-of-sample validation residuals (2021–2023); they reflect recent model volatility rather than formal asymptotic confidence limits."*

---

## 5. National-Level Interpretation Audit

### A. Mathematical Nature of "National" Values
- In `scripts/phase_7_forecasting.py` (lines 142–144):
  `sub = df[(df.Gender == gen) & (df.Area_Type == area) & (df.Education == edu)]`  
  `series_df = sub.groupby("Year")[ind].mean().reset_index()`
- This calculates an **unweighted analytical arithmetic mean** across reporting States/UTs.
- It does **not** use survey population weights (which are not present in Dataset 1).

### B. Required Presentation Terminology
- Terms such as "National Female LFPR Forecast" could be misinterpreted as official census or population-weighted all-India projections.
- **Required Framing for UI / Reporting:**
  - Use: **"All-India Analytical Mean (Unweighted across 36 States/UTs)"** or **"National Benchmark (State-Level Unweighted Mean)"**.
  - Maintain the existing Phase 8 and Phase 9 aggregation warning disclaiming population weighting.

---

## 6. Data Availability Limitation

The audit verified that the pipeline and documentation strictly enforce data reality:
- **Historical Temporal Span:** Exactly 7 annual points: 2017, 2018, 2019, 2020, 2021, 2022, 2023.
- **Validation Origins:** Exactly 3 rolling one-step-ahead origins: 2021, 2022, 2023.
- **Latest Observed Year:** Dynamically identified as **2023**.
- **Forecast Target:** 1-Year Ahead ($t+1$), which corresponds to **2024**.
- **Defensible Framing for Dashboard Integration:**
  - The dashboard must **never** present the 2024 forecast as a "current 2026 estimate".
  - The display must be clearly titled: **"Model-Based 1-Year Outlook (Base Year: 2023 $\rightarrow$ Outlook Year: 2024)"**.
  - An explicit annotation must state: *"Based on the latest available annual survey data (PLFS 2023). Represents a model-based conditional projection, not an observed 2026 value."*

---

## 7. Refreshability Audit

The implementation in `scripts/phase_7_forecasting.py` was audited for reusability:
- **Dynamic Year Detection:** `latest_observed_year = int(df["Year"].max())` (Line 115) and `earliest_observed_year = int(df["Year"].min())` (Line 116).
- **Expanding Validation Loop:** Uses `split_idx in range(min_train_len, n_total)` (Line 80), dynamically scaling if an 8th or 9th year is added.
- **Forecast Year Assignment:** `forecast_year = latest_observed_year + 1` (Line 219).
- **Verdict:** The script is **fully refreshable**. When a future PLFS round (e.g., 2024) is appended to Dataset 1, running `python3 scripts/phase_7_forecasting.py` will automatically incorporate the new year, expand the validation origins to 4, re-evaluate all 954 scenarios, update eligibility, and generate 2025 forecasts. No structural redesign is required.

---

## 8. Model Selection Audit

- **Candidate Set:** Strictly confined to the four parsimonious models specified: Naive, Drift, SES ($\alpha=0.3$), and Holt ($\alpha=0.4, \beta=0.2$). No unapproved models (ARIMA, Prophet, neural networks) were introduced.
- **Selection Criterion:** For every scenario, the model with the minimum out-of-sample MAE across expanding origins was deterministically selected.
- **Distribution of Selected Models:**
  - Naive: 149 scenarios ($28.7\%$)
  - Drift: 148 scenarios ($28.5\%$)
  - SES: 132 scenarios ($25.4\%$)
  - Holt: 90 scenarios ($17.3\%$)
- **Verdict:** Model selection strictly adheres to the stated methodology.

---

## 9. Data Integrity and Granularity Audit

- **No Synthetic Data:** Verified that zero interpolation, spline smoothing, forward-filling, or synthetic observations were injected into historical series.
- **Missingness Preserved:** Non-continuous series (e.g., Chandigarh Rural, which lacks a 2023 observation) were rejected (`FORECAST_NOT_SUPPORTED`) rather than imputed. Missing values in forecast columns are preserved as clean `NaN`s, never converted to zero.
- **Granularity Boundaries:** Detailed education categories ($N = 288$) were systematically excluded from eligibility.

---

## 10. Interpretation Boundary Audit

- The report and metadata strictly avoid causal language.
- Forecasts are explicitly defined as *conditional empirical extrapolations of recent momentum*, not guaranteed policy outcomes or official Government of India targets.
- All non-causal guidelines from Phase 8 are maintained.

---

## 11. Required Corrections Before Dashboard Integration

The following targeted corrections are required in metadata and documentation prior to Phase 9 integration:

| Issue | Severity | Required Action |
| :--- | :---: | :--- |
| **Prediction Interval Labeling** | **Minor** | In UI and report, label intervals as *"Empirical Uncertainty Interval (80% Nominal)"* rather than formal asymptotic prediction intervals. |
| **National Series Labeling** | **Minor** | In UI and report, label national series as *"All-India Analytical Mean (Unweighted across 36 States/UTs)"*. |
| **Temporal Horizon Framing** | **Moderate** | Ensure UI labels forecast as *"1-Year Horizon Outlook (Base: 2023 $\rightarrow$ Target: 2024)"* with prominent notices that this is a model projection from 2023 data, not an observed 2026 figure. |
| **Report Reconciliation Table** | **Minor** | Add an explicit 1-paragraph reconciliation in `phase_7_forecasting_feasibility.md` explaining that the 954 rows represent the total scenario universe ($235$ eligible + $284$ limited + $435$ unsupported). |

---

## 12. Final Integration Decision

**Verdict: APPROVED AFTER SPECIFIED CORRECTIONS**

The forecasting architecture, script, and reusable dataset (`forecast_results.csv`) are **APPROVED** for dashboard integration in Phase 9, subject to the four minor presentation and labeling adjustments specified in Section 11.

No full re-run of the forecasting pipeline or model redesign is needed.
