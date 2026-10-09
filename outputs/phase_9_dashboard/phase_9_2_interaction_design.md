# Phase 9.2 — Dashboard Information Architecture and Interaction Design Specification

**Project:** Women’s Labour Market Diagnostic in India  
**Phase:** 9.2 — Information Architecture and Interaction Design (SPECIFICATION ONLY)  
**Status:** SPECIFICATION COMPLETE  
**Implementation Blueprint For:** Phase 9.3 (Gradio Application on Hugging Face Spaces)  
**Core Analytical Question:** *"What different labour-market contexts exist across India, and what characteristics distinguish them?"*

---

## 1. Executive Summary & Purpose

Phase 9.2 translates the approved Phase 9.1 architecture into a concrete, unambiguous interaction design and information architecture specification. This document serves as the direct implementation blueprint for Phase 9.3.

### Core Architectural Mandates:
1. **Zero Redundant Analysis:** The UI layer is purely an interactive interface over the validated Phase 1–8 artifacts and analytical engines (`dataset_1_analytics.py`, `dataset_1_insights.py`, `dataset_1_narratives.py`, `dataset_2_analytics.py`).
2. **Deterministic & Non-Causal:** All dynamically generated natural-language text must flow directly through `dataset_1_narratives.py` or pre-validated Phase 6/8 evidence text.
3. **No Phantom Datasets or In-Callback Math:** The application will not calculate ad-hoc statistical formulas or create temporary analytical datasets inside UI event callbacks.

---

## 2. Global vs. Local Filter Architecture

To prevent confusing multi-dimensional filter matrices and ensure analytical clarity, the application establishes a **hybrid scoped filter model**:

### Global Filters (Application Header)
There are **no application-wide global multi-select filters** that force simultaneous updates across all tabs.
- *Rationale:* Dataset 1 (Demographic Labour Force) and Dataset 2 (Non-Agricultural Enterprise Composition) operate at fundamentally different grains, cover different time structures, and address different questions. Imposing a global filter across both would lead to invalid joins, empty states, or misleading comparisons.
- *Shared App Header Controls:*
  - **Theme Toggle / Baseline Indicator:** Quick indicator badge showing the current National Context (Female LFPR 45.0%, Gender Gap $-33.1$ pp in 2023).
  - **Quick Reset Action:** `[Reset All Tabs to Default Baseline]` button.

### Section-Specific (Local) Filters
Each analytical section maintains self-contained, context-aware controls:
- **Section 1 (National Overview):** Temporal toggle (`2017–2023`), Gender toggle (`Female`, `Male`, `Both`), Indicator toggle (`LFPR`, `WPR`, `Unemployment_Rate`).
- **Section 2 (State Diagnostic Explorer):** Primary State (`State A`, single-select dropdown), Optional Comparator State (`State B`, single-select dropdown), Year slider (`2017–2023`, default `2023`), Indicator radio (`LFPR`, `WPR`, `Unemployment_Rate`).
- **Section 3 (Structural Fault Lines):** Sub-tab switch (`Education Gradient`, `Educated Unemployment`, `Rural-Urban Divide`), Year selector (`2017–2023`), Area Type radio (`Rural`, `Urban`, `Rural + Urban`).
- **Section 4 (Employment & Enterprise Structure):** Industry Division Type radio, Year dropdown, Gender radio, Area Type radio.
- **Section 5 (Statistical & ML Evidence):** Filter by Finding (`F1`–`F11`), Model view toggle (`Performance Metrics`, `Feature Attributions`, `Methodological Boundaries`).

---

## 3. Default Application State

When the application loads for the first time, it displays a fully populated, analytically informative view without requiring initial user interaction:

| Property | Default Value | Analytical Justification |
| :--- | :--- | :--- |
| **Active Tab** | **Section 1: National Diagnostic Overview** | Sets the macro stage before user dives into regional heterogeneity. |
| **Default Year** | `2023` | Most recent authoritative survey wave in the dataset. |
| **Default Indicator** | `LFPR` (Labour Force Participation Rate) | Primary diagnostic measure of economic engagement. |
| **Default Gender** | `Female` (with Male comparison enabled on charts) | Direct gender comparison is the central project dimension. |
| **Default Area Type** | `Rural + Urban` (National Total) | Comprehensive population view before examining spatial divides. |
| **Default Education** | `All` | Macro baseline before inspecting educational gradients. |
| **Default State (Tab 2)** | `Bihar` (State A) vs. `Kerala` (State B) | Pre-configures a stark, highly informative diagnostic contrast: rapid rural catchup from low baseline (Bihar) vs. educated high-unemployment regime (Kerala). |
| **Default Dataset 2 (Tab 4)** | Industry Division `(05-99)`, `2023`, `Rural + Urban` | Most robust, complete non-agricultural enterprise cross-section. |

---

## 4. Detailed Information Architecture & UI Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               HEADER: Women’s Labour Market Diagnostic in India             │
│ [National 2023 Headline: Female LFPR 45.0% | Gender Gap -33.1 pp | Reset]   │
├─────────────────────────────────────────────────────────────────────────────┤
│ TAB 1: National Overview | TAB 2: State Explorer | TAB 3: Structural Faults │
│ TAB 4: Enterprise Structure | TAB 5: Statistical & Predictive Evidence     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 1: National Diagnostic Overview

#### A. Layout & Component Hierarchy
1. **Header & Context:**
   - Title: `National Labour Market Trajectory (2017–2023)`
   - Subtitle: `Examining the secular expansion in women's labour participation alongside persistent gender divides.`
2. **Headline KPI Ribbon (3 Metric Cards):**
   - *Card 1: 2023 Female LFPR:* `45.0%` (Sub-text: `+19.2 pp since 2017`)
   - *Card 2: 2023 Male LFPR:* `78.1%` (Sub-text: `+2.8 pp since 2017 | Stable trend`)
   - *Card 3: 2023 Gender Gap:* `-33.1 pp` (Sub-text: `Female participation remains systematically lower`)
3. **Primary Interactive Visual Area:**
   - *Controls:* Indicator Radio (`LFPR` [default], `WPR`, `Unemployment_Rate`); Gender Toggle (`Both` [default], `Female Only`, `Male Only`).
   - *Chart:* Dual-line temporal trajectory (Plotly line chart, 2017–2023). Shows stable male trajectory (~75–78%) contrasted with the rising female trajectory (25.8% $\rightarrow$ 45.0%).
   - *Narrative Callout Box (Generated via `dataset_1_narratives.py`):* Deterministic text describing national growth rate, endpoint comparison, and stability caveats.
4. **The Five Core Diagnostic Themes (Interactive Accordion):**
   - Collapsible cards detailing the five validated Phase 8 themes:
     1. *Universal Gender Participation Gap with Temporal Narrowing*
     2. *Rural-Urban Divergence in Female Labour-Force Participation*
     3. *Non-Monotonic Education-Participation Pattern*
     4. *Higher Educated Women's Unemployment Gap*
     5. *Gendered Enterprise Structure of Employment*
   - Each accordion card contains: (a) Core finding, (b) Key numbers, (c) Statistically supported basis, and (d) `[Jump to Deep Dive]` button routing to Tab 2, 3, or 4.

---

### Section 2: State Diagnostic Explorer & Context Profiles

#### A. User Journey & Interaction Flow
```
User selects State A (e.g. Maharashtra)
  │
  ├──> System retrieves State Dossier via dataset_1_analytics.py
  ├──> Assigns Descriptive Archetype Badge (Phase 8 Synthesis)
  ├──> Generates Dynamic Narrative via dataset_1_narratives.py
  ├──> Updates State KPI Ribbon & Trajectory Plot
  │
  └──> (Optional) User selects State B (e.g. Uttar Pradesh)
         │
         └──> System renders Dumbbell & Gap Comparison Plots
```

#### B. Component Layout
1. **Control Panel:**
   - Primary State Dropdown (`State A`, 36 items, searchable).
   - Optional Comparator Dropdown (`State B`, 36 items + `None [default]`).
   - Year Slider (`2017–2023`, default `2023`).
   - Indicator Selector (`LFPR`, `WPR`, `Unemployment_Rate`).
2. **Archetype Badge & Context Card:**
   - Prominently displays the descriptive archetype assigned in Phase 8:
     - 🏔️ *High-Participation Agrarian & Hill Context*
     - 🌾 *Rapid-Catchup Northern & Eastern Agrarian Context*
     - 🏭 *Moderate-Participation Peninsular & Diversified Context*
     - 🏙️ *Low-Participation Urban & Northern Enclave Context*
   - Clear disclaimer note: `Descriptive labour-market archetype based on observed multi-dimensional profiles, not a statistical cluster.`
3. **State KPI Ribbon (4 Cards):**
   - *Female Participation Rate* (e.g., 40.1%)
   - *Gender Participation Gap* (e.g., $-37.1$ pp)
   - *Rural-Urban Female Gap* (e.g., $+18.6$ pp Rural advantage)
   - *2017–2023 Net Change* (e.g., $+9.3$ pp gain)
4. **Visualisation Area (Dual Views):**
   - *View 1 (Single State Mode):* Multi-year temporal trajectory (2017–2023) showing Female Rural, Female Urban, and Male benchmark.
   - *View 2 (Comparator Mode):* Dumbbell plot comparing State A vs. State B across gender and rural/urban lines, with gap difference callouts.
5. **Dynamic Diagnostic Narrative Card:**
   - Sourced directly from `dataset_1_narratives.generate_narratives()`, providing structured paragraph summary of levels, gaps, and changes.

---

### Section 3: Structural Fault Lines

This section addresses the two critical structural paradoxes through three dedicated sub-tabs:

#### Sub-Tab 3.1: The Education U-Curve
- **Visual:** Grouped Bar / Line chart plotting Female LFPR across the 8 detailed education categories:
  `Not Literate` $\rightarrow$ `Literate & Primary` $\rightarrow$ `Middle` $\rightarrow$ `Secondary` $\rightarrow$ `Higher Secondary` $\rightarrow$ `Diploma` $\rightarrow$ `Graduate` $\rightarrow$ `Post Graduate`.
- **Interaction:** Area Type selector (`Rural + Urban`, `Rural`, `Urban`), Year selector.
- **Key Display:** Highlights the acute trough at Secondary/Higher Secondary (23.7%–24.0%) compared to non-literate (36.5%) and diploma/postgraduate (56.6%–59.1%).
- **Inline Evidence Badge:** `Statistically Validated: Friedman test χ² = 958.79, p < 0.001, ε² = 0.542 (Finding F5)`.

#### Sub-Tab 3.2: Educated Unemployment Friction
- **Visual:** Dumbbell / Grouped Column chart plotting Female vs. Male Unemployment Rate across education tiers.
- **Key Display:** Highlights the dramatic widening of open unemployment at Graduate (Female 23.3% vs. Male 10.7%) and Postgraduate levels (Female 22.2% vs. Male 8.6%), contrasted with near-zero friction for non-literate workers ($< 0.5\%$).
- **Inline Evidence Badge:** `Statistically Validated: Friedman test χ² = 467.27, p < 0.001, ε² = 0.262 (Finding F6)`.

#### Sub-Tab 3.3: Rural-Urban Divergence
- **Visual:** Area/Slope chart showing the divergence of Rural vs. Urban Female LFPR from 2017 to 2023.
- **Key Display:** Visualises the expansion of the rural-urban gap from $4.7$ pp (2017) to $19.8$ pp (2023).
- **Inline Evidence Badge:** `Statistically Validated: Gap Widening Wilcoxon W = 625.0, p < 0.001, r = 0.858 (Finding F4)`.

---

### Section 4: Employment & Enterprise Structure (Dataset 2)

#### A. Core Visualisation & Content
1. **Context & Metrics Notice:**
   - Prominent notice: `Metric: Percentage Engaged (% share of non-agricultural enterprise employment). Does not represent absolute headcounts or population totals.`
2. **Enterprise Composition Chart:**
   - Horizontal Stacked Bar / Diverging Bar showing % share across the 8 enterprise categories:
     `Proprietary and Partnership`, `Govt./ Local Body/ Public Sector`, `Employer's Households`, `Public/ Private Limited Company`, `Trust/ Non-profit`, `Autonomous Bodies`, `Cooperative Societies`, `Others`.
   - Compares Female distribution vs. Male distribution in Industry Division `(05-99)`.
3. **Key Structural Highlights:**
   - *Public Sector Anchor:* Highlight box showing Female reliance on government/local body enterprises (24.9% vs. 16.0% male).
   - *Domestic Service:* Highlight box showing female over-representation in Employer Households (6.3% vs. 0.8% male).
   - *Private Sector Cap:* Highlights that corporate companies absorb only 8.3% of working women.

#### B. Structural Absence & Warning Treatment
- **Division `(014, 016, 017, 02-99)` Handling:**
  - If user selects Industry Division `(014, 016, 017, 02-99)` and Year `2022` or `2023`:
    - The chart is **not rendered with zeros**.
    - An explicit amber warning banner appears:  
      `⚠️ Structural Survey Absence: Industry Division (014, 016, 017, 02-99) was not surveyed / reported in PLFS 2022–23 and 2023–24. Data available for 2017–2021 only.`
- **Enterprise Collapsing Warning:**
  - Displays inline reminder: `Enterprise percentages are compositional and unweighted across firm sizes.`

---

### Section 5: Statistical Evidence, Predictive Limits & Methodology

#### A. Phase 6 Inferential Hypothesis Evidence Table
An interactive, filterable Gradio Dataframe displaying all 9 tested findings:

| Finding | Topic | Sample ($n$) | Statistical Test | Statistic | $p$-value | Effect Size | Practical Meaning |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| **F1** | Temporal LFPR Rise | 36 States | Wilcoxon Signed-Rank | 663.0 | $< 0.001$ | $r = 0.864$ | Systematic national increase (+19.2 pp). |
| **F2** | Gender Participation Gap | 251 pairs | Wilcoxon Signed-Rank | 0.0 | $< 0.001$ | $r = -0.867$ | Universal female deficit in all matched contexts. |
| **F3** | State Variation | 36 States | Permutation Test | 137.36 | $< 0.001$ | — | Non-random state-level heterogeneity. |
| **F4** | Rural-Urban Gap Widening | 35 States | Wilcoxon Signed-Rank | 625.0 | $< 0.001$ | $r = 0.858$ | Systematic spatial gap expansion (+14.65 pp). |
| **F5** | Education Gradient | 251 pairs | Friedman Omnibus | 958.79 | $< 0.001$ | $\epsilon^2 = 0.542$ | Non-monotone U-curve across education. |
| **F6** | Educated Unemployment Gap | 251 pairs | Friedman Omnibus | 467.27 | $< 0.001$ | $\epsilon^2 = 0.262$ | Gender unemployment gap widens with education. |
| **F8** | Differential Gains by Education | 36 States | Friedman Omnibus | 66.36 | $< 0.001$ | $\epsilon^2 = 0.236$ | Gains concentrated in lower-educated tiers. |
| **F10** | Enterprise Shift (2017–23) | 36 States | Wilcoxon Signed-Rank | 666.0 | $< 0.001$ | $r = 0.872$ | Systematic enterprise composition change. |
| **F11** | Gender Enterprise Gap | 252 pairs | Wilcoxon Signed-Rank | 31,878.0 | $< 0.001$ | $r = 0.867$ | Systematic female over-indexing in public sector. |

#### B. Phase 7 Machine Learning Explanatory Limits
- **Model Performance Summary Card:**
  - Baseline (Training Mean): $R^2 = -0.008$, MAE $= 18.05$ pp
  - Ridge Regression: $R^2 = 0.139$, MAE $= 15.98$ pp
  - Gradient Boosting: $R^2 = 0.155$, MAE $= 15.70$ pp
- **The Explanatory Ceiling Callout (Donut/Gauge Visualisation):**
  - **15.5% Explained by Demographics:** Education, Area Type, and Year explain ~15.5% of out-of-fold variation under 36-fold Leave-One-State-Out (LOSO) cross-validation.
  - **84.5% Unexplained Variation:** When State is omitted from predictors, ~84.5% of variance remains unexplained by these demographic variables alone.
  - *Analytical Warning:* `This demonstrates the limits of macro-demographic prediction. It does not prove that State causes the remaining variance, but highlights that unmodelled regional, institutional, and cultural factors play a substantial role.`

---

## 5. Missingness, Zeroes, and Edge-Case Handling Protocol

The UI must explicitly implement this **decision matrix for data display**:

| Situation | Example Case | UI Display Text | Plot Behavior |
| :--- | :--- | :--- | :--- |
| **A. Valid Zero** | Not Literate Female Unemployment Rate = 0.4% (or 0.0%) | `0.0%` | Plotted as bar at 0. |
| **B. Structurally Missing Row** | Rural Chandigarh 2023 LFPR (8 rows in D1) | `[Data Structurally Absent in Source]` | Suppressed from plot; no bar drawn; grey hatched placeholder. |
| **C. Dataset 2 Industry Truncation** | Division `(014, 016, 017, 02-99)` in 2022 or 2023 | `⚠️ Structurally absent in 2022–2023 PLFS waves` | Chart hidden; informative warning banner displayed. |
| **D. Missing Comparator Observation** | User compares Chandigarh Rural 2023 to Delhi Rural 2023 | `Comparison unavailable (missing observation for Chandigarh)` | Individual value shown for Delhi; gap badge displays `N/A`. |
| **E. Empty Filter Combination** | Non-existent category combination | `No observations match the selected criteria.` | Empty-state message with `[Reset Filters]` button. |
| **F. Unweighted Analytical Mean** | Aggregating across states without population weights | Subtitle tag: `(Unweighted analytical mean)` | Displayed with explanatory hover tooltip. |

---

## 6. Gradio Component Mapping Table

Every visual and interactive component planned for Phase 9.3 maps directly to native Gradio components:

| UI Element | Functional Purpose | Gradio Component | Input Dependencies | Output Target / Callback |
| :--- | :--- | :--- | :--- | :--- |
| **Main Section Navigation** | Switch between the 5 analytical sections | `gr.Tabs()`, `gr.Tab()` | User tab click | Renders active tab container |
| **Indicator Selector** | Toggle between LFPR, WPR, and UR | `gr.Radio()` | User click (`LFPR`, `WPR`, `UR`) | Re-runs `dataset_1_analytics.analyse()` |
| **Primary State Selector** | Select State A for deep-dive | `gr.Dropdown()` | 36 State names | Updates State dossier & plots |
| **Comparator State Selector**| Select optional State B for comparison | `gr.Dropdown()` | 36 State names + `None` | Toggles Dumbbell comparator plot |
| **Year Slider / Dropdown** | Select survey wave (2017–2023) | `gr.Slider()` / `gr.Dropdown()` | Integer range [2017, 2023] | Triggers temporal slice update |
| **Area Type Selector** | Switch Rural, Urban, Rural + Urban | `gr.Radio()` | Area categories | Updates area breakdown plots |
| **Headline KPI Cards** | Display macro indicators & deltas | `gr.HTML()` / `gr.Markdown()` | Structured engine outputs | Renders styled HTML card ribbon |
| **Archetype Badge** | Display Phase 8 State Archetype | `gr.HTML()` | State name | Renders contextual badge & text |
| **Dynamic Narrative Card** | Present auto-generated natural text | `gr.Markdown()` | Output of `generate_narratives()` | Displays narrative block |
| **Interactive Plots** | Render line, bar, dumbbell charts | `gr.Plot()` | Plotly Figure objects | Interactive chart rendering |
| **Statistical Findings Table**| Interactive hypothesis test matrix | `gr.Dataframe()` | `statistical_results.csv` | Interactive sortable table |
| **Warning / Caveat Banners**| Surface missingness & method caveats | `gr.Markdown()` / `gr.Alert()`| Filter state check | Shows/hides warning banner |

---

## 7. Responsive Layout & Usability Architecture

- **Primary Form Factor:** Desktop / Laptop (1280px–1920px width) optimized for complex dual-panel analytical reading.
- **Grid Structure:** Standard 2-column or 3-column asymmetric layout:
  - *Left Column (Width: 30%):* Sticky controls, filter selectors, archetype badge, and deterministic narrative card.
  - *Right Column (Width: 70%):* KPI ribbon, main interactive visualization, and expandable evidence drawer.
- **Stacking Behavior on Smaller Viewports (Tablets):** Left control panel gracefully stacks vertically above visualizations; charts resize to 100% container width.

---

## 8. Phase 9.3 Implementation Boundaries

When Phase 9.3 begins, the developer must operate within these **strict implementation boundaries**:

### What Phase 9.3 MAY Do:
1. Create `app.py` and supporting UI helper scripts under `src/` or `app/`.
2. Import and call functions from `scripts/dataset_1_analytics.py`, `scripts/dataset_1_insights.py`, `scripts/dataset_1_narratives.py`, and `scripts/dataset_2_analytics.py`.
3. Construct Plotly visualizations based on structured engine outputs.
4. Render the Gradio layout specified in Section 4.

### What Phase 9.3 MUST NOT Do:
1. **MUST NOT** recalculate or re-aggregate raw PLFS microdata.
2. **MUST NOT** modify any files in `outputs/phase_4_eda/`, `outputs/phase_6_statistical_analysis/`, `outputs/phase_7_ml/`, or `outputs/phase_8_diagnostic/`.
3. **MUST NOT** create new analytical CSV files.
4. **MUST NOT** fit new machine learning models or statistical tests.
5. **MUST NOT** invent new state archetypes or causal claims.
6. **MUST NOT** silently impute missing survey cells or convert structural absence into zero.

---

## 9. Summary & Acceptance Criteria

Phase 9.2 provides a complete, unambiguous architectural and interaction blueprint. A developer can implement the Gradio application in Phase 9.3 directly from this document without making arbitrary analytical or design choices.

*Phase 9.2 specification complete. Implementation awaits Phase 9.3 sign-off.*
