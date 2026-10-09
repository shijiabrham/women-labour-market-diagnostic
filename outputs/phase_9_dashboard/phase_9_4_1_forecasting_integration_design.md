# Phase 9.4.1 — Visualisation, Data Storytelling and Forecasting Integration Design Specification

**Project:** Women’s Labour Market Diagnostic in India  
**Task:** Task 9.4.1 — Forecasting Outlook Integration Design Specification  
**Status:** SPECIFICATION COMPLETE (DESIGN ONLY)  
**Implementation Target (Task 9.4.2):** Python / Gradio Application (`app.py`, `ui/tab5_evidence.py` or `ui/tab6_forecasting.py`)  
**Core Analytical Purpose:** Seamlessly incorporate the approved Phase 7 one-year time-series forecasting capability into the existing Gradio application without compromising empirical discipline or altering previous phases.

---

## 1. Existing Application & Forecasting-File Inspection Summary

A rigorous audit of the existing analytical artifacts and application code was conducted prior to drafting this integration specification:

### A. Dashboard Architecture & Implementation (`app.py` & `ui/`)
- The existing application is modularly structured across five top-level tabs:
  - **Tab 1 (`ui/tab1_overview.py`):** National Diagnostic Overview (Macro KPI cards, 2017–2023 trajectory, 5 core Phase 8 diagnostic theme accordions).
  - **Tab 2 (`ui/tab2_state_explorer.py`):** State Diagnostic Explorer & Context Profiles (State dossiers, 4 descriptive archetypes, dumbbell comparison plot, multi-year state trajectory, deterministic narratives).
  - **Tab 3 (`ui/tab3_structural_faults.py`):** Structural Fault Lines (Education U-Curve, Educated Unemployment friction plot, Rural-Urban gap divergence plot).
  - **Tab 4 (`ui/tab4_enterprise_structure.py`):** Employment & Enterprise Structure (Dataset 2 enterprise distribution, public sector vs. proprietary informal analysis, structural absence notices).
  - **Tab 5 (`ui/tab5_evidence.py`):** Statistical Evidence, Predictive Limits & Methodology (Phase 6 inferential hypothesis matrix, Phase 7 LOSO ML explanatory ceiling, methodological boundary declarations).
- All analytical queries in Tabs 1–4 route strictly through authoritative analytical engines (`dataset_1_analytics.py`, `dataset_1_narratives.py`, `dataset_2_analytics.py`).
- Tab 5 directly consumes `statistical_results.csv` and `model_results.csv` without duplicating analytical computations.

### B. Approved One-Year Forecasting Results (`forecast_results.csv` & Reports)
- **File:** `outputs/phase_7_ml/forecasting/forecast_results.csv` ($N = 954$ rows).
- **Exact Schema:**
  `Level`, `State`, `Gender`, `Area_Type`, `Education`, `Indicator`, `Historical_End_Year`, `Forecast_Year`, `Forecast_Value`, `Lower_Interval_80`, `Upper_Interval_80`, `Selected_Model`, `Model_MAE`, `Naive_Baseline_MAE`, `MAE_Improvement_vs_Baseline`, `Forecast_Horizon`, `Eligibility_Status`, `Eligibility_Reason`.
- **Eligibility Universe Breakdown:**
  - `FORECAST_ELIGIBLE` ($N = 235$ rows / $24.6\%$): Series meeting strict rolling accuracy ($\text{MAE} \le 4.0$ pp) and outperforming Naive baseline by $\ge 0.10$ pp.
  - `FORECAST_ELIGIBLE_WITH_LIMITATIONS` ($N = 284$ rows / $29.8\%$): Series meeting acceptable accuracy ($\text{MAE} \le 3.5$ pp; $\le 2.5$ pp for UR) performing on par with Naive baseline; valid under 1-year horizon with cautionary notes.
  - `Total Eligible Scenarios:` **$519$ scenarios** ($54.4\%$).
  - `FORECAST_NOT_SUPPORTED` ($N = 435$ rows / $45.6\%$): Detailed education tiers ($N = 280$), cyclical unemployment series ($N = 37$), incomplete series ($N = 17$, e.g., Chandigarh Rural 2023), and high-volatility series ($N = 101$).
- **Approved Audited Terminology:**
  - Uncertainty intervals: **`Empirical Uncertainty Interval (80% Nominal)`**.
  - All-India series: **`All-India Analytical Mean (Unweighted across 36 States/UTs)`**.
  - Temporal framing: **`Base year: 2023 → Outlook year: 2024`** (1-year ahead horizon; strictly distinct from a current 2026 forecast).

### C. Five-Year Feasibility Assessment (`phase_7_five_year_forecasting_feasibility.md`)
- The mandatory feasibility assessment concluded: **INSUFFICIENT EVIDENCE TO RECOMMEND INCLUSION**.
- Key findings: Exactly one temporal backtesting origin ($N = 1$, $2018 \rightarrow 2023$) exists in a 7-year annual series; linear extrapolations over 5 years produce severe economic boundary violations (LFPR $> 100\%$ in Arunachal Pradesh and Nagaland; negative Unemployment Rates by 2027/2028).
- Directive: **Five-year projections must NOT be implemented or offered as an interactive feature.** The dashboard must include a prominent, mandatory methodological note explaining why the outlook is strictly restricted to one year.

---

## 2. Recommended Placement Within the Dashboard

Two potential integration architectures were evaluated:
1. *Option A (Subsection inside Tab 5):* Subsuming Forecasting Outlook inside Tab 5 alongside inferential tests and ML LOSO cross-validation.
2. *Option B (Dedicated Top-Level Tab 6):* Adding a dedicated top-level section: **`Tab 6: Forecasting Outlook (1-Year Horizon)`**.

### Recommended Decision: **Option B — Dedicated Top-Level Tab 6: "6. Forecasting Outlook"**

#### Rationale:
1. **Preservation of Distinct Analytical Paradigms:**
   - Tab 5 is an **Evidence, Audit & Methodology Reference** documenting retrospective inferential validation (Phase 6 hypothesis tests) and held-out cross-sectional generalization (Phase 7 LOSO ML $R^2 = 0.155$).
   - Forecasting Outlook is an **interactive time-series projection tool** designed to allow users to explore future trajectories, examine historical vs. projected time paths, and inspect scenario eligibility. Conflating them in Tab 5 would create severe visual and cognitive overload.
2. **Clear Separation of Predictive Methods:**
   - Leave-One-State-Out (LOSO) ML predicts held-out States across space.
   - Time-series forecasting predicts future points across time.
   - Placing Forecasting in its own tab reinforces the fundamental distinction between spatial prediction and temporal extrapolation.
3. **Preservation of Existing Tabs 1–5:**
   - Creating `ui/tab6_forecasting.py` leaves `ui/tab1_overview.py` through `ui/tab5_evidence.py` completely intact and unmodified, honoring the project protection rules.

---

## 3. Forecasting Outlook Information Architecture

The proposed **Tab 6: Forecasting Outlook** is structured into a clean, top-down analytical layout:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TAB 6: FORECASTING OUTLOOK                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. SECTION HEADER & TEMPORAL FRAMING                                        │
│    - Title: Model-Based 1-Year Forecasting Outlook (Base: 2023 → Target: 2024)│
│    - Subtitle: Conditional time-series projections based on PLFS 2017–2023. │
│    - Dynamic Status Banner: Latest Observed Year: 2023 | Horizon: 1 Year     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. INTERACTIVE CONTROL PANEL (Left Column - 30% width)                      │
│    - Geographic Level / State Dropdown (All-India Analytical Mean vs. States)│
│    - Indicator Radio (LFPR [default], WPR, Unemployment Rate)               │
│    - Gender Radio (Female [default], Male)                                   │
│    - Area Type Radio (Rural + Urban [default], Rural, Urban)                │
│    - Eligibility Status Badge (Eligible / Eligible with Limitations /       │
│      Unsupported)                                                           │
│    - Selected Model & Validation MAE Card                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. VISUALISATION & METRIC AREA (Right Column - 70% width)                   │
│    - Trajectory Plot: Historical Path (2017–2023) + Projected Point (2024)   │
│      with Empirical Uncertainty Interval Shading (80% Nominal)              │
│    - Metric Callout Ribbon: 2023 Observed vs. 2024 Projected (+/- Delta)    │
│    - Analytical Caveat / Uncertainty Callout                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. MANDATORY METHODOLOGICAL DISCLOSURES (Full Width)                        │
│    - Explaining the 1-Year Restriction (The Mandatory Five-Year Note)       │
│    - Model Selection & Validation Reference (Naive, Drift, SES, Holt)       │
│    - Non-Causal Planning Guidelines for NGOs & Policy Analysts              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Interactive Controls and Default Selections

### A. Available Controls (Supported by `forecast_results.csv`)
1. **Geographic Level / State Dropdown:**
   - Choices: `All-India Analytical Mean (Unweighted across 36 States/UTs)` followed by the 36 States/UTs in alphabetical order (`Andhra Pradesh`, `Arunachal Pradesh`, ..., `West Bengal`).
   - Mapped internally to: `National (All States)` or the exact State name.
2. **Indicator Radio:**
   - Choices: `LFPR` (default), `WPR`, `Unemployment_Rate`.
3. **Gender Radio:**
   - Choices: `Female` (default), `Male`.
4. **Area Type Radio:**
   - Choices: `Rural + Urban` (default), `Rural`, `Urban`.
5. **Education Dimension:**
   - **Fixed / Hidden at `Education = All`**. Detailed education categories are **not** exposed as filter choices because the feasibility study demonstrated that small-cell sample variance renders detailed education forecasting unsupported. A permanent caption will state: `Education: All (Detailed education categories excluded due to small-cell sampling noise)`.

### B. Default Selections
- **State / Level:** `All-India Analytical Mean (Unweighted across 36 States/UTs)` (Level: `National`)
- **Indicator:** `LFPR`
- **Gender:** `Female`
- **Area Type:** `Rural + Urban`
- *Default Row Properties in `forecast_results.csv`:*
  - Historical End Year: `2023`
  - Forecast Year: `2024`
  - 2023 Observed Value: `45.01%`
  - 2024 Forecast Value: `46.36%`
  - Empirical Uncertainty Interval (80% Nominal): `[43.73%, 48.99%]`
  - Selected Model: `Holt`
  - Model Out-of-Sample MAE: `2.21 pp` (vs. Naive Baseline `3.37 pp`)
  - Eligibility Status: `FORECAST_ELIGIBLE`

---

## 5. Forecast Visualisation Specification

The primary visualization is an interactive Plotly trajectory chart designed to maintain complete visual honesty regarding the transition from historical data to model projection:

### A. Chart Elements & Visual Encoding
1. **Historical Trajectory (2017–2023):**
   - Solid blue line (`#2563eb`, width 3px) with circular markers (`size=8`).
   - Sourced directly from `dataset_1_reusable_analytical.csv` for the exact filtered series.
   - Text annotations showing observed values (e.g. `45.0%` in 2023).
2. **Forecast Point Estimate (2024):**
   - Distinct colored marker (diamond, `#d97706` or `#059669`, `size=11`).
   - Dashed connector line (`dash='dash'`, width 2.5px) linking the 2023 observed point to the 2024 forecast point.
   - Point label showing projected value (e.g. `46.4% [Proj]`).
3. **Empirical Uncertainty Interval (80% Nominal):**
   - Visualized as a shaded vertical band or error bar at 2024 spanning `Lower_Interval_80` to `Upper_Interval_80`.
   - Semi-transparent fill (`rgba(217, 119, 6, 0.2)`).
   - Clearly labeled in the legend: `Empirical Uncertainty Interval (80% Nominal)`.
4. **Historical vs. Projection Demarcation:**
   - Vertical dotted separator line at $X = 2023.5$.
   - Shaded background for $X > 2023.5$ labeled: `Model-Based 1-Year Outlook`.
5. **Axes & Formatting:**
   - X-axis: Categorical/Integer years `[2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]`.
   - Y-axis: Indicator percentage bounded within reasonable range $[0, 100\%]$ (or local view with appropriate padding).
   - Title: `Historical Trajectory (2017–2023) and 1-Year Outlook (2024): [Indicator] - [State/Level]`.

---

## 6. Eligibility and Unsupported-Scenario Behaviour

The UI must implement a strict three-state rendering protocol based on the `Eligibility_Status` field in `forecast_results.csv`:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SCENARIO ELIGIBILITY HANDLING                        │
├────────────────────────────────────────────────────────────────────────┤
│ STATE 1: FORECAST_ELIGIBLE                                             │
│ - Badge: Green ("FORECAST ELIGIBLE - VALIDATED")                       │
│ - Chart: Renders historical line + projected point + uncertainty band. │
│ - Metrics: Displays 2024 forecast, model name, validation MAE, delta.  │
├────────────────────────────────────────────────────────────────────────┤
│ STATE 2: FORECAST_ELIGIBLE_WITH_LIMITATIONS                            │
│ - Badge: Amber ("ELIGIBLE WITH LIMITATIONS - CAUTION ADVISED")         │
│ - Chart: Renders historical line + projected point + uncertainty band. │
│ - Notice: Prominent amber callout detailing the limitation reason      │
│   (e.g., volatile series; model performs on par with Naive baseline). │
├────────────────────────────────────────────────────────────────────────┤
│ STATE 3: FORECAST_NOT_SUPPORTED                                        │
│ - Badge: Red ("FORECAST NOT SUPPORTED")                                │
│ - Chart: Historical line (2017-2023) ONLY. NO forecast point or band.  │
│ - Notice: Clear explanatory box stating exact reason from metadata     │
│   (e.g. "Out-of-sample forecast error exceeds 3.5 pp threshold" or     │
│   "Structurally incomplete series in source survey").                  │
│ - No zeros or fabricated values are plotted.                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Data-Availability and Uncertainty Messaging

### Mandatory Messaging Requirements:
1. **Dynamic Temporal Header:**
   The section header will prominently display:
   > **Base Year: 2023 (Latest Observed PLFS Wave) → Outlook Year: 2024 (1-Year Horizon)**  
   > *Note: This represents a model-based conditional projection from the latest available annual survey data in the current dataset (PLFS 2023). It is NOT an observed 2026 figure.*
2. **Audited Uncertainty Interval Label:**
   All uncertainty bands, tables, and tooltips must use the exact audited label:
   **`Empirical Uncertainty Interval (80% Nominal)`**  
   Accompanied by the explanatory note:  
   *"Uncertainty intervals are empirical bounds calibrated from out-of-sample expanding-window validation residuals (2021–2023); they reflect recent model volatility rather than formal asymptotic confidence intervals."*
3. **All-India Series Framing:**
   All-India totals must be labeled:  
   **`All-India Analytical Mean (Unweighted across 36 States/UTs)`**  
   With the caveat:  
   *"Values represent unweighted analytical arithmetic means across reporting States/UTs, not official population-weighted census estimates."*

---

## 8. Mandatory Methodological Note Explaining the Five-Year Restriction

In strict compliance with Section 6 of the user specification, the dashboard must feature this explicit, unshortened note placed directly in Tab 6 immediately below the visualization:

```markdown
### ⚠️ Methodological Disclosure: Why is the outlook limited to one year?

The available PLFS dataset contains seven annual observations, from 2017 to 2023. The forecasting models were evaluated using historical one-year-ahead validation. The available data do not provide sufficient independent historical periods to assess five-year-ahead forecast accuracy.

A separate feasibility assessment also found that some five-year trend projections produced implausible values, including labour-force participation rates above 100% and negative unemployment rates.

**For these reasons, the dashboard provides only eligible one-year-ahead forecasts.** Longer-term projections are not displayed because their reliability cannot be established adequately with the available data.

The forecasting analysis can be reassessed when additional annual observations become available.
```

*Design Rule:* This note must appear in a dedicated, clearly visible container. No disabled 5-year buttons or horizon sliders will be shown.

---

## 9. Data-Loading and Refreshability Architecture

### A. Integration with Precomputed Results
The application must consume `outputs/phase_7_ml/forecasting/forecast_results.csv` directly:
- **No in-callback model fitting:** The UI will never fit Naive, Drift, SES, or Holt models on the fly.
- **Lookup Protocol:**  
  When a user selects `(State, Indicator, Gender, Area_Type)`:
  1. Filter `forecast_results.csv` for matching attributes where `Education == "All"`.
  2. Extract `Eligibility_Status`, `Selected_Model`, `Forecast_Year`, `Forecast_Value`, `Lower_Interval_80`, `Upper_Interval_80`, `Model_MAE`, `Naive_Baseline_MAE`, and `Eligibility_Reason`.
  3. Load the historical series (2017–2023) from `dataset_1_reusable_analytical.csv` using the existing cached `d1_analytics.load()` engine.
  4. Render the combined plot and metric ribbon.

### B. Metadata Verification & Dynamic Detection
- The audit confirmed that `forecast_results.csv` contains complete, explicit temporal metadata:
  - `Historical_End_Year` (2023)
  - `Forecast_Year` (2024)
  - `Forecast_Horizon` ("1-Year")
- The UI helper will dynamically read `latest_observed_year = int(forecast_df["Historical_End_Year"].max())` and `forecast_year = int(forecast_df["Forecast_Year"].max())`. No year values are hardcoded in the UI rendering functions.

---

## 10. Distinguishing the Two Predictive Components

To ensure complete clarity for researchers, CSR donors, and policy analysts, the application must maintain a strict conceptual boundary between the two predictive modules:

| Dimension | Machine Learning Predictive Model (Phase 7 / Tab 5) | Time-Series Forecasting Outlook (Phase 7.x / Tab 6) |
| :--- | :--- | :--- |
| **Analytical Question** | *"Can demographic characteristics predict the gender gap in an unseen State?"* | *"What is the projected 1-year trajectory of an indicator conditional on past momentum?"* |
| **Prediction Dimension** | **Cross-Sectional / Spatial** (predicting across States). | **Temporal** (predicting future annual points). |
| **Validation Method** | **36-Fold Leave-One-State-Out (LOSO) Cross-Validation**. | **Expanding-Window Historical Backtesting (2021–2023)**. |
| **Core Finding / Metric** | $R^2 = 0.155$ (Demographics explain ~15.5% of spatial variance). | Out-of-sample MAE (Holt MAE = 2.21 pp vs. Naive MAE = 3.37 pp). |
| **Primary Limitation** | ~84.5% of variance remains unexplained by demographics. | Horizon strictly restricted to 1 year; 7 historical points. |
| **Causal Status** | Strictly non-causal statistical associations. | Strictly non-causal mechanical extrapolation. |

---

## 11. Implementation Checklist for Task 9.4.2

When implementing Task 9.4.2, the following steps must be executed:
1. [ ] Create `ui/tab6_forecasting.py` containing:
   - Data loading helper caching `forecast_results.csv`.
   - Trajectory plot generator combining historical data from `d1_analytics.load()` and forecast points.
   - Three-state eligibility card renderer (Eligible, Eligible with Limitations, Unsupported).
   - Mandatory Five-Year Restriction Note container.
2. [ ] Register Tab 6 in `app.py`:
   - Import `build_tab6` from `ui.tab6_forecasting`.
   - Mount `build_tab6()` inside the main `gr.Tabs()` block.
3. [ ] Verify that Tabs 1–5 and existing analytical scripts remain 100% untouched.
4. [ ] Run automated programmatic test verifying that all 36 States, all 3 indicators, and all eligibility states render cleanly without exceptions.

---

## 12. Acceptance Criteria for Implementation and Testing

1. **Exact Scenario Fidelity:** Selecting any of the 954 scenarios displays the exact values, models, and eligibility statuses recorded in `forecast_results.csv`.
2. **Visual Boundary Demarcation:** The transition from 2023 observed data to 2024 forecast is visually unmistakable.
3. **No Phantom Forecasts:** Selecting an unsupported scenario (e.g. Bihar LFPR Rural+Urban or any detailed education tier) suppresses the forecast point and displays the documented rejection reason.
4. **Mandatory 5-Year Note Present:** The exact text explaining the 5-year restriction appears prominently in Tab 6.
5. **Audited Terminology Enforced:** Uses *Empirical Uncertainty Interval (80% Nominal)* and *All-India Analytical Mean (Unweighted across 36 States/UTs)*.
6. **No Code Modification in Previous Phases:** No files outside `app.py` and `ui/tab6_forecasting.py` are modified during implementation.

---

*Phase 9.4.1 design specification complete. No code implemented. Ready for Task 9.4.2.*
