# Phase 7 — Extended Forecasting Feasibility Assessment: Five-Year Horizon and Historical Backtesting

**Project:** Women’s Labour Market Diagnostic in India  
**Task:** Task 7.x — Five-Year Time-Series Forecasting Feasibility and Historical Backtesting Assessment  
**Status:** FEASIBILITY ASSESSMENT COMPLETE  
**Primary Data Source:** `outputs/phase_4_eda/dataset_1_reusable_analytical.csv` (PLFS 2017–2023)  
**Historical Base Period:** 2017–2023 (Seven annual survey rounds)  
**Target Horizon Assessed:** 5 Years Ahead ($h = 1, \dots, 5$, targeting 2024–2028 from 2023 base)  

---

## 1. Executive Conclusion

### Assessment Outcome:
**INSUFFICIENT EVIDENCE TO RECOMMEND INCLUSION**

### Core Empirical Rationale:
1. **Severe Temporal Backtesting Deficit:** With only seven annual historical observations (2017–2023), exactly **one** single genuine 5-year-ahead out-of-sample backtesting origin is mathematically possible across time: training on 2017–2018 ($n=2$) to forecast 2023 ($h=5$). Evaluating multiple States or indicators over this single 2018 $\rightarrow$ 2023 transition does **not** generate independent temporal validation points. A sample size of $N=1$ temporal origin cannot establish out-of-sample forecast reliability.
2. **Boundary Violations and Exploding Linear Extrapolations:** Unconstrained trend extrapolation over a 5-year horizon produces severe economic implausibilities. For example, projecting the 2017–2023 rural expansion momentum forward results in projected female LFPR exceeding **100%** by 2028 in States like Arunachal Pradesh (109.7%) and Nagaland (104.0%). For the Unemployment Rate, Holt's linear trend method projects **negative unemployment rates** by 2027 ($-0.67\%$) and 2028 ($-1.87\%$).
3. **Compound Uncertainty Cannot Be Defensibly Calibrated:** While 1-year-ahead prediction errors can be bounded empirically by recent validation residuals ($n=3$ origins), compounding uncertainty over a 5-year horizon cannot be credibly estimated from a 7-point series without fabricating error-growth assumptions.
4. **Distinction from Approved 1-Year Pipeline:** The existing Phase 7 one-year forecasting pipeline (`forecast_results.csv`) was rigorously evaluated across three expanding-window origins ($t=2021, 2022, 2023$) and is approved for dashboard integration. In contrast, extending the forecast horizon to five years lacks empirical validation, introduces high risk of misleading decision-makers, and cannot be defended methodologically.

---

## 2. Available Historical Data and Forecasting Scope

The empirical foundation available for time-series modeling in Dataset 1 is strictly defined by:
- **Available Annual Waves:** Exactly seven survey rounds: 2017, 2018, 2019, 2020, 2021, 2022, 2023.
- **Temporal Frequency:** Annual (1 observation per year per cell).
- **Temporal Dimension ($T$):** $T = 7$.
- **Indicators Assessed:**
  - Labour Force Participation Rate (LFPR)
  - Worker Population Ratio (WPR)
  - Unemployment Rate (UR)
- **Geographic Granularity:** 36 States/UTs and the All-India unweighted analytical mean across States.
- **Demographic Granularity:** Rural, Urban, Rural + Urban; Female, Male; Education = All.

### Structural Horizon Definition:
- **Historical Base Period:** Ends in **2023**.
- **Proposed Projection Horizon:** 5 Years Ahead ($h = 1, \dots, 5$), mapping to **2024, 2025, 2026, 2027, and 2028**.
- **Framing Constraint:** Projections from this dataset represent retrospective conditional extrapolations from the 2023 data endpoint; they cannot be framed as "current 2026 forecasts".

---

## 3. Five-Year-Ahead Backtesting Feasibility

To determine if 5-year-ahead forecast accuracy can be empirically evaluated, we audit how many genuine, non-overlapping or expanding out-of-sample backtest origins can be constructed without future data leakage:

### Mathematical Audit of Expanding / Rolling Origins ($T = 7$, Target Horizon $h = 5$):
- **Origin 1:**
  - Training Period: 2017–2018 (Length $n = 2$ annual points).
  - Forecast Target Year ($t + 5$): **2023**.
  - Actual Observed Value Available: **Yes** (PLFS 2023).
  - Validation Status: **Feasible, but severely constrained by training length ($n=2$).**
- **Origin 2:**
  - Training Period: 2017–2019 (Length $n = 3$ annual points).
  - Forecast Target Year ($t + 5$): **2024**.
  - Actual Observed Value Available: **No** (PLFS 2024 is not in the dataset).
  - Validation Status: **Impossible to evaluate.**

### Empirical Backtest Audit Conclusion:
- There is **exactly ONE** historical 5-year-ahead validation point ($2018 \rightarrow 2023$).
- Training any time-series model on only **two data points** ($2017, 2018$) to project five years into the future is statistically degenerate:
  - Naive baseline simply carries forward the 2018 value (ignoring all subsequent structural shifts).
  - Drift and Holt methods compute a linear trajectory based solely on the slope between 2017 and 2018.
- **Empirical Backtest Results on Origin 1 (Train 2017–2018 $\rightarrow$ Forecast 2023):**
  - *National Female LFPR (Observed 2023 = 45.01%):*
    - Naive (pred = 27.97%): Absolute Error = **$17.04$ pp**
    - Drift (pred = 38.92%): Absolute Error = **$6.09$ pp**
    - SES (pred = 26.44%): Absolute Error = **$18.58$ pp**
    - Holt (pred = 38.92%): Absolute Error = **$6.09$ pp**
  - *National Female WPR (Observed 2023 = 42.47%):*
    - Naive (pred = 25.45%): Absolute Error = **$17.02$ pp**
    - Drift (pred = 37.57%): Absolute Error = **$4.90$ pp**
- **Methodological Assessment:** While Drift/Holt produced lower error than Naive over this single 5-year transition, **evaluating one single point provides zero statistical degrees of freedom**. It is mathematically impossible to estimate error variance, stability, or ranking confidence from an $N=1$ temporal test. Cross-sectional units (testing 36 states over the same 2018 $\rightarrow$ 2023 window) share identical macroeconomic, COVID-19, and policy shocks, and therefore do not provide independent temporal validation.

---

## 4. Candidate Model Assessment

Restricting model evaluation to the approved parsimonious set (Naive, Drift, Simple Exponential Smoothing, Holt):

### 1. Naive Baseline (Last Known Value)
- **Formulation:** $\hat{y}_{2023+h} = y_{2023}$ (flat projection of 45.01% for all 5 years).
- **Properties:** Mathematically stable, perfectly bounded, never violates range [0, 100%].
- **Limitation:** Fails completely to reflect trend momentum established between 2017 and 2023; projects zero future participation change despite a +19.2 pp historical gain.

### 2. Drift Model (Linear Trend Slope)
- **Formulation:** Computes historical slope over 2017–2023 ($\Delta = \frac{45.01 - 25.78}{6} \approx +3.205$ pp/year) and projects linearly:
  - 2024: 48.22%
  - 2025: 51.42%
  - 2026: 54.63%
  - 2027: 57.84%
  - 2028: **61.04%**
- **Properties:** Captures secular direction, but assumes uninterrupted linear acceleration indefinitely.

### 3. Simple Exponential Smoothing (SES)
- **Formulation:** Exponentially decays past observations; with $\alpha = 0.3$, level settles at 37.92% and remains completely flat for all $h = 1, \dots, 5$.
- **Properties:** Severely lags trending series; unsuited for 5-year trajectory analysis.

### 4. Holt’s Linear Trend Model
- **Formulation:** Tracks smoothed local level and local slope:
  - 2024: 46.36%
  - 2025: 49.18%
  - 2026: 52.01%
  - 2027: 54.84%
  - 2028: **57.66%**
- **Properties:** Produces slightly tempered slopes compared to full-span Drift, but still compounds linearly without dampening or asymptotic saturation.

---

## 5. Forecast Plausibility and Indicator Constraints

When candidate models are applied across the full 36-state cross-section to project 5 years forward (to 2028), critical structural and boundary violations emerge:

### A. Boundary Violations for LFPR and WPR:
- Linear extrapolation of the rapid 2017–2023 rural recovery pushes state-level participation rates past physiological and demographic maximums:
  - **Arunachal Pradesh:** 2023 Female LFPR = 66.5%; Drift 2028 projection = **$109.7\%$** (Violates upper bound of 100%).
  - **Nagaland:** 2023 Female LFPR = 64.3%; Drift 2028 projection = **$104.0\%$** (Violates upper bound of 100%).
  - **Himachal Pradesh:** Holt 2028 projection = **$101.4\%$**.
- *Methodological Consequence:* Linear models lack asymptotic saturation (e.g. logistic/S-curve bounds). Silently clipping forecasts at 100% or manufacturing arbitrary caps would violate empirical transparency.

### B. Severe Boundary Collapse for Unemployment Rate:
- The national female Unemployment Rate declined from 11.65% in 2017 to 4.87% in 2022 and 6.15% in 2023.
- Extrapolating the downward trend using Holt's linear trend method projects:
  - 2024: $2.91\%$
  - 2025: $1.71\%$
  - 2026: $0.52\%$
  - 2027: **$-0.67\%$** (Negative unemployment rate)
  - 2028: **$-1.87\%$** (Negative unemployment rate)
- *Methodological Consequence:* Cyclical and friction-bounded indicators like unemployment cannot tolerate multi-year linear extrapolation on short samples.

---

## 6. Uncertainty Assessment

### Why 5-Year Uncertainty Intervals Cannot Be Defensibly Calibrated:
1. **Error Compounding Over Horizons:** In time-series econometrics, forecast variance grows with horizon $h$ (typically proportional to $\sigma \sqrt{h}$ for random walks or compounding polynomial expansions for trend models).
2. **Insufficient Empirical Residuals:**
   - For 1-year forecasts, Phase 7 calibrated uncertainty intervals using the standard deviation of residuals across 3 rolling one-step-ahead origins ($n=3$).
   - For 5-year forecasts, there is **only one residual observation** ($N=1$, from the 2018 $\rightarrow$ 2023 backtest).
   - Sample standard deviation cannot be calculated from $N=1$.
3. **Manufactured Intervals vs. False Precision:**
   - Attempting to scale the 1-step residual standard deviation by arbitrary heuristic multipliers (e.g. $\sqrt{5} \approx 2.23$) would manufacture uncertainty intervals without empirical validation.
   - Reporting a 5-year projection without intervals presents false precision; reporting manufactured intervals presents false methodology.

---

## 7. Potential Usefulness for NGO and CSR Planning

We evaluate whether an exploratory 5-year outlook provides genuine strategic utility versus decision risk for civil society, CSR, and policy planners:

| Planning Use Case | Potential Utility | Substantive Analytical Risk |
| :--- | :--- | :--- |
| **Directional Benchmarking** | Shows what happens if 2017–2023 momentum continues uninterrupted. | High risk of confusing mechanical extrapolation with policy targets or economic forecasts. |
| **Comparative Trajectories** | Contrasts flat (Naive) vs. trend (Drift/Holt) paths. | Assumes past rural distress entry continues linearly without structural saturation. |
| **Multi-Year Budgeting / Target Setting** | NGOs often plan on 3-to-5 year funding cycles. | **Extremely Dangerous:** Setting targets based on $61\%$ projected national female LFPR or negative unemployment rates could lead to severe programmatic misallocation. |

### Conclusion on Usefulness:
While decision-makers frequently desire 5-year horizons, **the diagnostic integrity of the project would be compromised by providing projections that cannot be validated**. The appearance of quantitative precision over a 5-year window would encourage unjustified reliance on an extrapolation that has no statistical support.

---

## 8. Refreshability and Data Availability

- **Dynamic Data Dependence:** The forecasting script architecture developed in Task 7.x (`scripts/phase_7_forecasting.py`) dynamically detects `latest_observed_year`.
- **Temporal Horizon Scaling:**
  - When PLFS 2024 is added ($T = 8$), two 5-year backtesting origins become available ($2018 \rightarrow 2023$ and $2019 \rightarrow 2024$).
  - When PLFS 2025 is added ($T = 9$), three origins become available.
- **Reassessment Trigger:** Five-year forecasting should not be reconsidered until at least **$T \ge 10$ annual waves** (e.g. PLFS 2026) are available, providing at least 5 rolling 5-year validation origins to evaluate out-of-sample error growth and model dampening.

---

## 9. Recommendation for Dashboard Inclusion

### Explicit Recommendation:
**OPTION A: EXCLUDED FROM THE APPLICATION (DEFERRED)**

### Detailed Actionable Directives:
1. **Maintain Phase 9 Scope:** Do **not** add a 5-year forecasting tab, slider, or projection component to the Gradio application (`app.py`).
2. **Preserve Approved 1-Year Pipeline:** Retain the validated, audited **1-Year Ahead Outlook ($t+1$, targeting 2024 from 2023 base)** with its documented empirical uncertainty intervals as the sole forecasting component.
3. **Transparent Methodology Note in Dashboard:** If longer horizons are mentioned in Tab 5 (Methodology), state explicitly:  
   *"Multi-year horizons (3-year and 5-year projections) were systematically audited and excluded due to mathematical boundary violations (e.g. extrapolations exceeding 100% or falling below 0%) and the impossibility of conducting multi-origin time-based backtesting on a 7-year annual series."*

---

## 10. Limitations and Conditions for Future Reassessment

Future reassessment of multi-year forecasting may only be reopened if the following empirical conditions are met:
1. **Minimum Historical Length:** The dataset expands to at least $T \ge 10$ annual observations.
2. **Non-Linear / Bounded Model Formulations:** Replacement of unconstrained linear trend models with bounded growth models (e.g., Logistic / Bass diffusion models) to prevent participation rates exceeding 100% or unemployment dropping below zero.
3. **Multi-Origin Empirical Backtesting:** Availability of at least 4 independent rolling origins demonstrating that a multi-year model systematically beats a dampened benchmark.

---

*Assessment completed in accordance with Phase 7 audit standards. No existing outputs modified.*
