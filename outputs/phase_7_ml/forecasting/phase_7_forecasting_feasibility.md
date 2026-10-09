# Phase 7 Forecasting Feasibility & Validation

**Project:** Women’s Labour Market Diagnostic in India  
**Sub-task:** Phase 7.x — Time-Series Forecasting Feasibility Study & Model Validation  
**Status:** FEASIBILITY & VALIDATION COMPLETE  
**Primary Analytical Data Source:** `outputs/phase_4_eda/dataset_1_reusable_analytical.csv`  
**Execution Script:** `scripts/phase_7_forecasting.py`  
**Consolidated Results Dataset:** `outputs/phase_7_ml/forecasting/forecast_results.csv`  

---

## 1. Objective

The objective of this study is to assess whether future forecasting of key labour-market indicators—specifically Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), and Unemployment Rate (UR)—is methodologically defensible using the historical Periodic Labour Force Survey (PLFS) series available in Dataset 1.

Rather than maximizing the number of generated forecasts, this study is governed by an explicit analytical principle: **A scenario must be allowed to fail.** Forecasting models must demonstrate measurable out-of-sample improvement over naive baselines under rigorous time-based validation before being declared eligible for decision-making or policy communication.

---

## 2. Data Structure

The analysis relies strictly on the validated reusable Dataset 1 analytical layer:
- **Historical Temporal Span:** 2017 to 2023 (seven annual survey rounds).
- **Temporal Frequency:** Annual observations.
- **Dimensional Hierarchy:**
  - **State:** 36 States and Union Territories.
  - **Gender:** Female, Male, Persons.
  - **Area Type:** Rural, Urban, Rural + Urban.
  - **Education:** Source-provided aggregate `All`, plus 8 detailed educational attainment tiers.
  - **Indicators:** LFPR, WPR, Unemployment Rate.
- **Total Dataset Size:** 22,650 rows across all cross-sections.

---

## 3. Forecasting Constraints

Forecasting annual PLFS indicators under this structure faces several severe methodological constraints:
1. **Short Time Horizon:** The historical record contains only **seven annual data points** ($t = 1, \dots, 7$). This precludes high-parameter econometric models (e.g., ARIMA with seasonal orders, VAR, LSTM) which overfit severely on small samples.
2. **Structural Missings:** While 3,210 of the 3,240 State $\times$ Gender $\times$ Area $\times$ Education time series possess complete 7-year records, certain cells—most notably rural Chandigarh in 2023—are structurally absent in the source data.
3. **Non-Stationarity & Macro Regime Shifts:** The 2017–2023 period includes the economic shock of the COVID-19 pandemic (2020–2021) and a sharp subsequent expansion in rural female participation, introducing structural curvature into trend trajectories.
4. **No Cross-Sectional Pooling for Temporal Expansion:** Cross-sectional observations across States cannot be treated as additional time points. Time-series dynamics must be validated strictly on temporal ordering.

---

## 4. Feasibility Assessment

Prior to model fitting, an empirical audit was conducted across indicators, geographical levels, and education groups:

| Dimension / Indicator | Feasibility Finding | Analytical Rationale |
| :--- | :--- | :--- |
| **LFPR (Labour Force Participation Rate)** | **FEASIBLE** | Exhibits persistent secular trajectories and moderate year-on-year autocorrelation across national and most state series. |
| **WPR (Worker Population Ratio)** | **FEASIBLE** | Moves in parallel with LFPR; low open unemployment in rural areas results in consistent trend momentum. |
| **Unemployment Rate (UR)** | **FEASIBLE WITH LIMITATIONS** | Highly volatile, cyclical, and bounded close to zero in rural tiers; standard trend extrapolation fails; requires cautious error bounds. |
| **National Level** | **FEASIBLE** | Aggregating across 36 States eliminates localized idiosyncratic noise, producing smooth, continuous 7-year trajectories. |
| **State Level (Education = All)** | **FEASIBLE FOR MOST STATES** | Provides sufficient trend consistency in 33 of 36 States/UTs. Fails in small island/urban enclaves with sharp trend breaks. |
| **Detailed Education Tiers** | **NOT SUPPORTED** | Small cell sample sizes in specific state-education strata create high annual variance that lacks predictive signal. |

---

## 5. Candidate Forecasting Scenarios

### Reconciliation of Scenarios and Result Records:
The consolidated results dataset () contains exactly **954 rows**, reflecting one record per candidate scenario evaluated:
- **FORECAST_ELIGIBLE ( = 235$ rows / .6\%$):** High-performing series meeting strict accuracy and improvement criteria.
- **FORECAST_ELIGIBLE_WITH_LIMITATIONS ( = 284$ rows / .8\%$):** Moderate-performing series valid under 1-year horizon with cautionary bounds.
- **Total Eligible Scenarios:**  + 284 = \mathbf{519}$ scenarios (.4\%$).
- **FORECAST_NOT_SUPPORTED ( = 435$ rows / .6\%$):** Detailed education tiers ($), cyclical unemployment series ($), incomplete series ($), and high-volatility series ($). These are preserved in the dataset with documented rejection reasons and null forecasts for complete auditability.


To ensure an evidence-led scope, **954 candidate forecasting scenarios** were systematically evaluated:
1. **National Scenarios ($N = 18$):** 3 Indicators $\times$ 2 Genders $\times$ 3 Area Types at `Education = All`.
2. **State-Level Scenarios ($N = 648$):** 36 States $\times$ 3 Indicators $\times$ 2 Genders $\times$ 3 Area Types at `Education = All`.
3. **Detailed Education Scenarios ($N = 288$):** 36 States $\times$ Female $\times$ Rural + Urban $\times$ 8 Detailed Education Tiers for LFPR.

---

## 6. Candidate Models

In accordance with best practices for short annual time series, four low-parameter, parsimonious models were tested:
1. **Naive Baseline (Last Known Value):**  
   $$\hat{y}_{T+h} = y_T$$  
   Essential benchmark. Any forecasting model must outperform this baseline to justify selection.
2. **Drift Model (Linear Trend Baseline):**  
   $$\hat{y}_{T+h} = y_T + h \left( \frac{y_T - y_1}{T - 1} \right)$$  
   Projects the average historical slope across the available span.
3. **Simple Exponential Smoothing (SES):**  
   $$\hat{y}_{T+h} = \ell_T, \quad \ell_t = \alpha y_t + (1 - \alpha) \ell_{t-1}$$  
   Captures locally weighted levels with $\alpha = 0.3$.
4. **Holt’s Linear Trend Method:**  
   $$\hat{y}_{T+h} = \ell_T + h b_T, \quad \ell_t = \alpha y_t + (1 - \alpha)(\ell_{t-1} + b_{t-1}), \quad b_t = \beta(\ell_t - \ell_{t-1}) + (1 - \beta) b_{t-1}$$  
   Separates smoothed local level ($\alpha = 0.4$) and trend slope ($\beta = 0.2$).

---

## 7. Time-Based Validation Design

Validation strictly adhered to **expanding-window backtesting** respecting historical time ordering:
- **No random train/test splitting.**
- **No future information leakage.**
- **Validation Protocol:**
  - *Origin 1:* Train on 2017–2020 ($n=4$), forecast 1-step ahead for 2021 ($t=5$).
  - *Origin 2:* Train on 2017–2021 ($n=5$), forecast 1-step ahead for 2022 ($t=6$).
  - *Origin 3:* Train on 2017–2022 ($n=6$), forecast 1-step ahead for 2023 ($t=7$).
- **Primary Validation Metric:** Out-of-sample Mean Absolute Error (MAE) averaged across the three rolling origins:
  $$\text{MAE} = \frac{1}{3} \sum_{t=2021}^{2023} |y_t - \hat{y}_t|$$

---

## 8. Forecast Performance

Across all evaluated scenarios, model performance varied systematically by indicator and level:

### Summary of Out-of-Sample Performance:
- **National LFPR (Female, Rural + Urban):**
  - Naive Baseline MAE: $3.37$ pp
  - Drift MAE: $2.64$ pp
  - SES MAE: $3.08$ pp
  - **Holt Method MAE: $2.21$ pp** (Best model; $34.4\%$ error reduction over Naive baseline).
- **National LFPR (Male, Rural + Urban):**
  - Naive Baseline MAE: $0.77$ pp
  - **Drift MAE: $0.51$ pp** (Best model; male series is remarkably stable with small linear drift).
- **State-Level Dispersion:**
  - In high-growth agrarian states (e.g., Bihar, Odisha, Madhya Pradesh), Holt and Drift outperformed Naive by $1.2$ to $2.5$ pp MAE.
  - In volatile enclaves (e.g., Lakshadweep, Goa), Naive outperformed trend extrapolation because linear models over-projected past cyclical reversals.

---

## 9. Model Selection

Model selection was conducted independently for each scenario based strictly on out-of-sample MAE:
- Among the 519 scenarios meeting eligibility standards:
  - **Naive Selected:** $149$ scenarios ($28.7\%$) — primarily where indicators fluctuated without steady trend.
  - **Drift Selected:** $148$ scenarios ($28.5\%$) — optimal for steady, linear male trajectories and moderate urban series.
  - **SES Selected:** $132$ scenarios ($25.4\%$) — selected for series with shifting levels and weak persistent drift.
  - **Holt Selected:** $90$ scenarios ($17.3\%$) — best for strong secular female rural expansions.

---

## 10. Forecast Eligibility Framework

Each candidate scenario was classified according to strict, transparent criteria:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     FORECAST ELIGIBILITY MATRIX                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. FORECAST ELIGIBLE (235 Scenarios / 24.6%)                           │
│    - Complete 7-year historical series ending in 2023.                 │
│    - Out-of-sample MAE <= 4.0 pp across rolling origins.               │
│    - Candidate model improves over Naive baseline by >= 0.1 pp.        │
├────────────────────────────────────────────────────────────────────────┤
│ 2. FORECAST ELIGIBLE WITH LIMITATIONS (284 Scenarios / 29.8%)          │
│    - Complete 7-year historical series.                                │
│    - Out-of-sample MAE <= 3.5 pp (or <= 2.5 pp for Unemployment Rate). │
│    - Model performs on par with Naive baseline.                        │
│    - Valid only under 1-Year Horizon with cautionary notes.            │
├────────────────────────────────────────────────────────────────────────┤
│ 3. FORECAST NOT SUPPORTED (435 Scenarios / 45.6%)                      │
│    - All 288 Detailed Education Scenarios (high noise / cell variance).│
│    - Series with missing years (e.g., Chandigarh Rural).               │
│    - Series where out-of-sample MAE > 3.5 pp.                          │
│    - Unemployment series with severe cyclical reversals.               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Forecast Horizon Assessment

Given only seven historical annual observations, forecast uncertainty compounds exponentially with horizon:
- **1-Year Ahead ($t+1$, e.g., 2024):** **METHODOLOGICALLY DEFENSIBLE.** Point forecasts and prediction intervals are anchored by recent local levels and validated slope momentum.
- **3-Year Ahead ($t+3$, e.g., 2026):** **NOT SUPPORTED.** Compounding extrapolation errors over 3 years exceed the magnitude of historical policy shifts.
- **5-Year Ahead ($t+5$, e.g., 2028):** **UNACCEPTABLE.** Projecting 5 years into the future from a 7-year historical baseline violates empirical forecasting discipline.

**Decision:** Only **1-Year Ahead** forecasts are authorized and generated.

---

## 12. Uncertainty Assessment

For all eligible scenarios, empirical **Uncertainty Intervals (80% Nominal)** were constructed based on out-of-sample validation residuals:
$$\hat{y}_{T+1} \pm 1.282 \times \sigma_{\text{residuals}}$$
- For scenarios where residual variance was very small, an empirical minimum half-width of $\pm 1.0$ pp was enforced.
- Upper and lower bounds were strictly bounded between $0.0\%$ and $100.0\%$.

---

## 13. Eligible Future Forecasts

Eligible 2024 forecasts have been generated and stored in `outputs/phase_7_ml/forecasting/forecast_results.csv`.

### Key All-India Analytical Mean Projections (2024, Unweighted across 36 States/UTs):
| Indicator | Gender | Area Type | Model | 2023 Observed | 2024 Forecast | Empirical Uncertainty Interval (80% Nominal) | Out-of-Sample MAE | Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **LFPR** | Female | Rural + Urban | Holt | 45.01% | **46.36%** | [43.73%, 48.99%] | 2.21 pp | FORECAST ELIGIBLE |
| **LFPR** | Female | Rural | Holt | 48.80% | **53.81%** | [50.50%, 57.12%] | 2.10 pp | FORECAST ELIGIBLE |
| **LFPR** | Female | Urban | Drift | 28.00% | **32.76%** | [31.24%, 34.28%] | 1.29 pp | FORECAST ELIGIBLE |
| **LFPR** | Male | Rural + Urban | Drift | 78.09% | **78.55%** | [77.55%, 79.55%] | 0.51 pp | FORECAST ELIGIBLE |
| **WPR** | Female | Rural + Urban | Holt | 43.50% | **44.50%** | [42.10%, 46.89%] | 1.88 pp | FORECAST ELIGIBLE |
| **WPR** | Male | Rural + Urban | Drift | 75.30% | **75.93%** | [74.93%, 76.93%] | 0.51 pp | FORECAST ELIGIBLE |

---

## 14. Unsupported Forecast Scenarios

The study explicitly documents **435 scenarios as FORECAST NOT SUPPORTED**:
1. **Detailed Education Categories ($N = 280$):** High annual sampling variance at the State $\times$ Education level produces erratically fluctuating series where trend models produce unrealistic compounding errors.
2. **Cyclical Unemployment Rate Series ($N = 37$):** Series where out-of-sample MAE exceeded $2.5$ pp or trend extrapolation produced negative or explosive values during sudden reversals.
3. **Structurally Incomplete Series ($N = 17$):** Rural Chandigarh (missing 2023) and related non-continuous series.
4. **High-Error State LFPR Series ($N = 97$):** States such as Nagaland, Arunachal Pradesh, or Lakshadweep where extreme annual swings (MAE $> 4.0$ pp) preclude reliable extrapolation.

---

## 15. Methodological Limitations

1. **Short Historical Memory:** A 7-point time series cannot detect multi-year economic cycles or mean-reverting structural ceilings.
2. **No Policy Shock Covariates:** These time-series models are purely autoregressive/extrapolative; they do not incorporate macroeconomic shocks, inflation, or government policy shifts.
3. **Non-Causal Nature:** Projected increases reflect statistical extrapolation of recent momentum and must not be interpreted as guaranteed or policy-driven outcomes.

---

## 16. Refreshability & Dynamic Pipeline

The implementation script `scripts/phase_7_forecasting.py` is fully dynamic:
- It dynamically queries `latest_observed_year = df["Year"].max()`.
- When new survey rounds (e.g., PLFS 2024) are appended to Dataset 1, re-running the script automatically incorporates the new year, updates expanding-window origins, reassesses model performance against Naive baselines, updates eligibility classifications, and generates updated $t+1$ projections.

---

## 17. Conclusion

Forecasting future labour-market outcomes from PLFS Dataset 1 is **methodologically defensible under strict boundaries**:
1. **Scope:** Restricted to **National and State levels at Education = All**.
2. **Indicators:** Defensible for **LFPR and WPR**; strictly constrained for **Unemployment Rate**.
3. **Horizon:** Defensible **strictly for 1-Year Ahead ($t+1$)**. Longer horizons (3-year, 5-year) are not supported.
4. **Detailed Education:** Firmly rejected as not supported due to small-cell sampling noise.

*Phase 7 forecasting feasibility study complete. Results consolidated in `forecast_results.csv`.*
