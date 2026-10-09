# Phase 9.4.2 — Forecasting Outlook Implementation & Validation Report

**Project:** Women’s Labour Market Diagnostic in India  
**Task:** Task 9.4.2 — Implement Forecasting Outlook Tab (Gradio Dashboard Integration)  
**Status:** IMPLEMENTATION COMPLETE & FULLY VALIDATED  
**Application Entry Point:** `app.py`  
**New Module:** `ui/tab6_forecasting.py`  
**Design Specification Followed:** `outputs/phase_9_dashboard/phase_9_4_1_forecasting_integration_design.md`  
**Data Sources Consumed:**
- `outputs/phase_7_ml/forecasting/forecast_results.csv` (Approved Phase 7 forecasting results, $N = 954$ rows)
- `outputs/phase_4_eda/dataset_1_reusable_analytical.csv` (Historical PLFS series 2017–2023)

---

## 1. Overview & Architectural Compliance

Task 9.4.2 integrated the approved Phase 7 one-year time-series forecasting capability into the existing Gradio application as a new sixth top-level tab: **`6. Forecasting Outlook`**.

### Core Standards Upheld:
1. **Preservation of Existing Architecture:** All five existing tabs (`1. National Overview`, `2. State Diagnostic Explorer`, `3. Structural Fault Lines`, `4. Employment & Enterprise Structure`, `5. Statistical Evidence, Predictive Limits & Methodology`) remain completely functional and untouched in `ui/`.
2. **Single Source of Truth:** `ui/tab6_forecasting.py` consumes precomputed model selections, out-of-sample MAE metrics, empirical uncertainty intervals, and eligibility classifications directly from `outputs/phase_7_ml/forecasting/forecast_results.csv`. Zero model fitting or ad-hoc mathematical calculations take place in UI event callbacks.
3. **Data Protection:** No files across Phases 1–6, Phase 7 ML predictive modeling, Phase 8 synthesis, or existing analytical engines (`scripts/dataset_1_analytics.py`, `scripts/phase_7_forecasting.py`) were modified.
4. **Distinction of Predictive Modules:** The tab explicitly distinguishes temporal time-series forecasting ($t+1$ projections forward in time) from the spatial cross-sectional Leave-One-State-Out (LOSO) ML predictive modeling presented in Tab 5.

---

## 2. Implementation Details of Tab 6 (`ui/tab6_forecasting.py`)

### A. Dynamic Year & Scenario Handling
- **Dynamic Endpoints:** The base year (`2023`) and forecast year (`2024`) are read dynamically from `Historical_End_Year` and `Forecast_Year` in the dataset rows, avoiding hardcoded temporal assumptions.
- **Dynamic Control Populate:** Derives the list of 37 geographic levels (`All-India Analytical Mean` + 36 States/UTs), 3 indicators (`LFPR`, `WPR`, `Unemployment_Rate`), 2 genders (`Female`, `Male`), and 3 area types (`Rural + Urban`, `Rural`, `Urban`) directly from the data.
- **Education Dimension:** Fixed at `Education = All` with an explicit notice explaining that detailed education tiers were excluded due to small-cell sampling noise.

### B. Three-State Eligibility Protocol
The UI enforces strict three-state rendering behavior:
1. **`FORECAST_ELIGIBLE`:** Renders a green status badge (`FORECAST ELIGIBLE — VALIDATED`), the point forecast estimate, the 80% nominal uncertainty interval, the selected model name (`Holt`, `Drift`, `SES`, `Naive`), and validation MAE metrics.
2. **`FORECAST_ELIGIBLE_WITH_LIMITATIONS`:** Renders an amber status badge (`ELIGIBLE WITH LIMITATIONS — CAUTION`), the point estimate, the uncertainty interval, and a prominent callout highlighting baseline/cyclical volatility.
3. **`FORECAST_NOT_SUPPORTED`:** Renders a red status badge (`FORECAST NOT SUPPORTED`). Crucially, **no forecast point or uncertainty band is plotted**; only the historical trajectory (2017–2023) is shown, accompanied by a documented rejection banner explaining why the series was suppressed. Never converts missing forecasts to zero.

### C. Visualisation Specification (Plotly Trajectory Chart)
- **Historical Path (2017–2023):** Solid blue line (`#2563eb`, width 3px) with circular markers and data value labels.
- **Historical vs. Forecast Demarcation:** Vertical dotted line at the base year boundary ($X = \text{Base Year} + 0.5$).
- **Projection Path (2024):** Distinct diamond marker (`#d97706`, size 12px) linked to the 2023 endpoint via a dashed amber line.
- **Empirical Uncertainty Interval:** Vertical whisker bar and shaded background highlighting the 80% nominal uncertainty range.

### D. Mandatory Five-Year Limitation Disclosure
The exact mandatory text required by the specification is prominently rendered in a full-width accordion container directly below the visualization:
> **Why is the outlook limited to one year?**  
> The available PLFS dataset contains seven annual observations, from 2017 to 2023. The forecasting models were evaluated using historical one-year-ahead validation. The available data do not provide sufficient independent historical periods to assess five-year-ahead forecast accuracy.  
> A separate feasibility assessment also found that some five-year trend projections produced implausible values, including labour-force participation rates above 100% and negative unemployment rates.  
> **For these reasons, the dashboard provides only eligible one-year-ahead forecasts.** Longer-term projections are not displayed because their reliability cannot be established adequately with the available data.  
> The forecasting analysis can be reassessed when additional annual observations become available.

### E. Audited Terminology Enforced
- **`Empirical Uncertainty Interval (80% Nominal)`** (calibrated from out-of-sample expanding-window validation residuals, not asymptotic confidence bounds).
- **`All-India Analytical Mean (Unweighted across 36 States/UTs)`** (unweighted analytical arithmetic mean, not an official population-weighted PLFS census estimate).

---

## 3. Automated Test Suite & Validation Results

A rigorous automated test script was executed to verify Tab 6 functionality and confirm zero regression across Tabs 1–5:

| Test Item | Verification Check | Result |
| :--- | :--- | :---: |
| **Data Loading & Schema** | Verified `forecast_results.csv` exists and contains all 18 required columns across 954 rows | **PASS** |
| **Dynamic Metadata** | Dynamically extracted Base Year (`2023`) and Forecast Year (`2024`); verified 37 geographic choices | **PASS** |
| **Default Scenario Resolution** | Default resolved to All-India Female LFPR Rural+Urban (`FORECAST_ELIGIBLE`, Holt model, $46.36\%$ forecast, $[43.73\%, 48.99\%]$ interval) | **PASS** |
| **FORECAST_ELIGIBLE Rendering** | Verified all 4 chart traces (historical line, connector line, uncertainty bar, forecast marker) | **PASS** |
| **ELIGIBLE_WITH_LIMITATIONS** | Tested All-India Female Unemployment Rate Rural+Urban; verified amber caution badge | **PASS** |
| **FORECAST_NOT_SUPPORTED** | Tested Bihar Female LFPR Rural+Urban; verified **1 trace only** (historical line), no forecast marker, no zero plotting | **PASS** |
| **Mandatory 5-Year Note** | Confirmed exact presence of required explanatory text in `ui/tab6_forecasting.py` | **PASS** |
| **Tabs 1–6 Integration in `app.py`** | Imported `app.demo`; verified all 6 tabs mount cleanly with 16 registered backend callback functions | **PASS** |
| **Regression Test (Tabs 1–5)** | Sequentially executed rendering functions for Tabs 1, 2, 3, 4, and 5 | **PASS** |

---

## 4. File Protection Verification

Confirmed that all protected files remain intact, unchanged, and locked:
- `outputs/phase_4_eda/dataset_1_reusable_analytical.csv` (Untouched)
- `outputs/phase_4_eda/dataset_2_reusable_analytical.csv` (Untouched)
- `outputs/phase_6_statistical_analysis/statistical_results.csv` (Untouched)
- `outputs/phase_7_ml/model_results.csv` (Untouched)
- `outputs/phase_7_ml/forecasting/forecast_results.csv` (Untouched)
- `scripts/phase_7_forecasting.py` (Untouched)
- `outputs/phase_8_diagnostic/phase_8_analytical_synthesis.md` (Untouched)
- `outputs/phase_9_dashboard/phase_9_1_dashboard_architecture.md` (Untouched)
- `outputs/phase_9_dashboard/phase_9_2_interaction_design.md` (Untouched)
- `outputs/phase_9_dashboard/phase_9_3_implementation_validation.md` (Untouched)
- `outputs/phase_9_dashboard/phase_9_4_1_forecasting_integration_design.md` (Untouched)
