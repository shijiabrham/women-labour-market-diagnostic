# Women’s Labour Market Diagnostic in India

## From Labour-Market Data to Evidence for Decision-Making

**Project type:** Applied Data Analytics  
**Data source:** Periodic Labour Force Survey (PLFS), accessed through NITI Aayog’s National Data and Analytics Platform (NDAP)

### Problem and Research Question

Women’s labour-market outcomes vary across Indian states, education levels, rural–urban settings, and employment structures. A single national participation rate cannot show these differences. This project asks: **How do women’s labour-market outcomes vary across these contexts, and what does the employment structure look like within them?**

### Data and Analytical Approach

The project analyses two PLFS datasets: labour-market outcomes by education and employment structure by enterprise type and industry. The analysis covers 2017–2023 and combines data-quality checks, reusable analytical datasets, exploratory analysis, state and gender comparisons, statistical tests and effect sizes, 36-fold leave-one-state-out machine-learning validation, and guarded one-year forecasting. Findings are presented in a six-tab interactive dashboard.

### Key Findings

- **Gender gap persists:** The unweighted mean female Labour Force Participation Rate (LFPR) across 36 States/UTs rose from 25.78% in 2017 to 45.01% in 2023. Female LFPR remained below male LFPR in all 251 matched State–Year observations. The 2023 gap was approximately 33.1 percentage points.
- **Rural–urban divergence widened:** Mean rural female LFPR increased by approximately 24.5 percentage points between 2017 and 2023, compared with 9.4 percentage points in urban areas.
- **Education and unemployment:** Participation varied non-linearly by education. In 2023, female graduate unemployment was 23.31%, compared with 10.74% among male graduates.
- **Predictive limits:** Under 36-fold leave-one-state-out cross-validation, Gradient Boosting achieved R² = 0.155, MAE = 15.70 percentage points, and RMSE = 22.27 percentage points, indicating limited generalisation to an unseen state.
- **Exploratory forecast:** The eligible Holt forecast estimated female LFPR at 46.36% for 2024, with a nominal 80% interval of 43.73%–48.99%. Historical MAE was 2.21 percentage points, compared with 3.37 for the naïve baseline.

### Relevance to NGOs and CSR Organisations

The diagnostic can help organisations strengthen proposal problem statements, explore which geographies or groups warrant closer assessment, frame programme-design questions, and select relevant outcome indicators. It can inform consideration of interventions such as employability training, career guidance, or employment support, subject to local needs assessment.

State-level patterns alone cannot determine funding priorities or prove which intervention will work. Local data, community consultations, employer perspectives, and assessments of existing services remain essential.

### Limitations and Responsible Interpretation

LFPR figures are unweighted means across States/UTs, not official population-weighted national estimates. The analysis is descriptive and observational; it does not establish causation or programme impact. The enterprise analysis has coverage limitations, and the forecasts are exploratory, based on only seven annual observations, and subject to substantial uncertainty.

### Project Links

- **Static dashboard:** https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic-static
- **Gradio dashboard:** https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic
- **GitHub repository:** https://github.com/shijiabrham/women-labour-market-diagnostic