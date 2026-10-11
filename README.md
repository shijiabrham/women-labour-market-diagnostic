---
title: Women Labour Market Diagnostic
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
short_description: Women labour market diagnostic across Indian states
---

# Women’s Labour Market Diagnostic in India

An interactive diagnostic exploring how women’s labour-market outcomes vary across Indian states, education levels and rural–urban contexts, with gender comparison as a core analytical dimension. The project uses annual Periodic Labour Force Survey (PLFS) data for 2017–2023 accessed through the National Data and Analytics Platform (NDAP).

**Core research question:** How do women's labour-market outcomes vary across Indian states, education levels and rural–urban contexts, and what does the employment structure look like within these different contexts?

## Explore the application

- **[Open the live static dashboard](https://shijiabraham-women-labour-market-diagnostic-static.static.hf.space)**
- [Open the static Hugging Face Space](https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic-static)
- [Open the Gradio application](https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic)

The dashboard has six analytical tabs:

1. **National Diagnostic Overview** — national-level trajectories, gender gaps and structural patterns across 36 States/UTs.
2. **State Diagnostic Explorer & Context Profiles** — state-level diagnostic profiles and pairwise comparisons.
3. **Structural Fault Lines** — rural–urban differences, education-related LFPR patterns and graduate unemployment.
4. **Employment & Enterprise Structure** — gender distribution across enterprise types in the non-agricultural employment-structure dataset.
5. **Statistical Evidence, Predictive Limits & Methodology** — statistical tests, model evaluation and methodological interpretation.
6. **Forecasting Outlook** — an exploratory one-year-ahead time-series forecast with a nominal 80% uncertainty interval.

## Why this diagnostic matters

NGOs, CSR foundations and other social-sector organisations working on women’s economic empowerment or employability can use the dashboard to explore differences in labour-market conditions, compare contexts and identify questions that need further investigation. It can inform programme-design discussions, local research priorities and the selection of employment outcome indicators.

The dashboard is a **diagnostic tool, not a programme evaluation**. It helps identify patterns and generate questions; it does not establish why a pattern exists or prove that a particular intervention will work. Decisions about programme design or resource allocation should be informed by local evidence, consultations with women and employers, and organisations’ own programme data.

## Data sources

The project uses two PLFS datasets accessed through NDAP:

- **Dataset 7129 — Labour-market indicators by education, gender and area (2017–2023):** includes State/UT, year, rural/urban area, gender, education level, Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR) and unemployment rate.
- **Dataset 7131 — Persons engaged in industry by enterprise type (2017–2023):** supports analysis of employment structure by geography, gender, industry and enterprise type.

The datasets address related but different analytical questions. Dataset 7131 has coverage limitations and its enterprise-type analysis should not be interpreted as representing the entire economy. Missing or structurally unavailable values are not treated as zero. Comparisons between datasets are made only where their dimensions and definitions support a meaningful comparison.

## Analytical approach

The project combines:

- Dataset profiling, data-quality checks, missingness assessment and analytical data preparation.
- Exploratory analysis of LFPR, WPR and unemployment by gender, education, geography and year.
- State and rural–urban comparisons, including descriptive labour-market context profiles.
- Statistical tests to assess selected differences and patterns.
- Leave-One-State-Out (LOSO) cross-validation to assess whether machine-learning models generalise to an unseen state.
- A one-year-ahead forecast using Holt’s method, evaluated against a naïve baseline.
- An interactive dashboard to present results and methodological caveats.

### Forecasting approach and limits

The forecasting component uses seven annual observations (2017–2023) to estimate female LFPR for 2024. The Holt model produces a forecast of **46.36%**, with a **nominal 80% interval of 43.73%–48.99%**. Its historical mean absolute error (MAE) was **2.21 percentage points**, compared with **3.37 percentage points** for the naïve baseline.

This is an exploratory, short-horizon forecast based on a very short annual series. The interval is heuristic rather than a guarantee, and the forecast should not be treated as a definitive prediction of future outcomes. The project does not produce a five-year forecast.

## Selected findings

The following national-level figures are **unweighted means across 36 States/UTs**, not official population-weighted national estimates:

- **Female LFPR increased:** from **25.78% in 2017** to **45.01% in 2023**.
- **The gender gap narrowed but persisted:** female LFPR remained below male LFPR in all **251 matched State–Year observations** in the analysis.
- **Rural–urban change differed:** mean rural female LFPR increased by approximately **24.5 percentage points** between 2017 and 2023, compared with approximately **9.4 percentage points** in urban areas.
- **Graduate unemployment remained a concern:** in 2023, female graduate unemployment was **23.31%**, compared with **10.74%** among male graduates.

These findings describe patterns in the analysed data. They do not, by themselves, explain the causes of the patterns or establish the effectiveness of any programme.

## Limitations and responsible interpretation

- The analysis is descriptive and observational; it does not establish causal relationships or measure the impact of a specific intervention.
- Unweighted State/UT means should not be confused with official population-weighted national estimates.
- State-level patterns cannot explain every individual woman’s circumstances.
- The enterprise-structure dataset has coverage constraints and does not represent all forms of employment across the economy.
- The machine-learning results have limited predictive performance; they should be interpreted as an assessment of generalisation, not as a causal explanation.
- The forecast is limited to one year ahead and is uncertain because only seven annual observations are available.
- The analysis does not include all individual, household, employer or local factors that can shape women’s employment outcomes.

## Run the application locally

### Gradio dashboard

The root `requirements.txt` contains the lightweight dashboard runtime dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python3 app.py
```

The local Gradio address will be shown in the terminal when the application starts.

### Static dashboard

To serve the static dashboard locally from the repository root:

```bash
python3 -m http.server 8080 --directory static
```

Then open `http://localhost:8080` in a browser.

### Validate exported dashboard data

```bash
python3 scripts/validate_exported_data.py
```

This validates the exported JSON data used by the static dashboard.

### Analytical pipeline dependencies

The root `requirements.txt` is intended for the dashboard runtime and does not include every package needed to rerun all offline analyses. Some statistical-analysis and machine-learning scripts also require `scipy` and `scikit-learn`. Install those separately when reproducing those analyses:

```bash
pip install scipy scikit-learn
```

Check each script and its accompanying phase documentation for its specific inputs and execution details before rerunning the full analytical pipeline.

## Repository documentation

Detailed methodology, validation and findings are documented in the `outputs/` directory, including:

- `outputs/phase_8_diagnostic/phase_8_analytical_synthesis.md` — synthesis of the diagnostic themes and findings.
- `outputs/phase_6_statistical_analysis/phase_6_statistical_analysis_results.md` — statistical-analysis results.
- `outputs/phase_7_ml/phase_7_2_ml_analysis.md` and `outputs/phase_7_ml/phase_7_2_final_audit.md` — machine-learning analysis and audit.
- `outputs/phase_7_ml/forecasting/` — forecasting feasibility and audit documentation.

## Project output

A publicly accessible interactive labour-market diagnostic intended to support evidence-informed exploration by analysts and social-sector practitioners. It is designed to help users identify patterns and frame better questions—not to replace local research, programme monitoring or impact evaluation.
