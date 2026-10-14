# Project Story: Women’s Labour Market Diagnostic in India

## From Labour-Market Data to Evidence for Decision-Making

### 1. The question that started the project

Women’s participation in India’s labour market has changed over time, but national trends alone do not explain how these changes vary across states, education levels, and rural and urban settings. I wanted to investigate these differences and understand what the available data could tell us about women’s labour-market outcomes.

My central research question was:

**How do women’s labour-market outcomes vary across Indian states, education levels, and rural–urban contexts, and what does the employment structure look like within these different contexts?**

I was also interested in how such evidence could help NGOs and Corporate Social Responsibility (CSR) organisations make informed decisions when designing programmes and preparing funding proposals.

### 2. Building the analytical foundation

I used two datasets accessed through NITI Aayog’s National Data and Analytics Platform (NDAP). The first covered labour-market indicators by gender, education, geography, and year from 2017 to 2023. The second examined persons engaged in industry by enterprise type, providing a different perspective on employment structure.

I began by examining the datasets, their coverage, missing values, and analytical dimensions. I then developed reusable analytical datasets to support consistent comparisons across the different stages of the project.

The analysis combined exploratory data analysis, state-level comparisons, statistical hypothesis testing, effect sizes, machine-learning validation, and short-horizon forecasting. I used leave-one-state-out cross-validation to examine whether machine-learning models could generalise to a state or Union Territory not used for training. I also assessed the limitations of forecasting with only seven annual observations.

### 3. What the data revealed

One of the clearest findings was the increase in female labour-force participation across the state-level analytical series. The unweighted mean rose from 25.8% in 2017 to 45.0% in 2023. However, male participation remained substantially higher, with a female–male gap of approximately 33.1 percentage points in 2023.

These figures are unweighted means across states and Union Territories. They help compare regional patterns but should not be interpreted as official population-weighted national estimates.

The analysis also revealed different rural and urban trajectories. Mean rural female participation increased by approximately 24.5 percentage points between 2017 and 2023, compared with 9.4 percentage points in urban areas. This widening difference highlighted the importance of examining rural and urban contexts separately rather than relying only on an overall trend.

Education did not show a simple, steadily increasing relationship with participation. The analysis identified a non-linear pattern, with lower participation among some middle and secondary schooling groups and higher participation among certain tertiary-educated groups.

Graduate unemployment was another important finding. In 2023, the unemployment rate among women graduates was 23.3%, compared with 10.7% among men graduates. This points to the need to examine the different challenges associated with education and access to employment.

The enterprise analysis added another dimension by examining the distribution of employment across enterprise types. However, limitations in the underlying survey coverage meant that these results required careful interpretation and could not automatically be generalised to the entire economy.

### 4. Testing the limits of prediction

I evaluated machine-learning models using 36-fold leave-one-state-out cross-validation, holding out an entire state or Union Territory in each fold. This tested how well the models could predict the gender participation gap in a jurisdiction not used for training.

The Gradient Boosting model achieved an out-of-fold R² of 0.155, with a mean absolute error (MAE) of 15.70 percentage points and a root mean squared error (RMSE) of 22.27 percentage points.

These results indicated that the selected macro-demographic predictors had limited predictive power for an unseen state. They reinforced the importance of recognising regional differences and avoiding claims that a model can fully explain or predict local labour-market outcomes.

I also developed a one-year forecasting approach using expanding-window backtesting and explicit eligibility checks. Forecasts were retained where the available evidence met the project's eligibility criteria. Scenarios with insufficient reliability were marked as unsupported rather than presented as dependable projections.

This approach helped ensure that uncertainty and model limitations remained visible instead of allowing every possible scenario to produce a forecast.

### 5. Connecting evidence to programme design

An important application of this project is its potential use by NGOs and CSR organisations working on women's livelihoods, skills, and employment.

Understanding differences in labour-market outcomes across states, education levels, and rural–urban settings can help organisations identify geographies that warrant further investigation and explain why a particular issue deserves attention.

For example, an organisation preparing a proposal on women's employability could use the findings to strengthen its problem statement, describe the broader labour-market context, and identify which groups or geographic areas need closer assessment. The evidence could also help organisations frame programme objectives, identify relevant outcome indicators, and explain the rationale for seeking funding.

The findings may inform consideration of interventions such as employability training, career guidance, or employment support, depending on the needs identified locally. They can also help CSR teams and donors ask more focused questions when assessing programme priorities and proposals.

However, state-level analysis alone cannot determine which geography should receive funding or which intervention will be effective. Local data, community consultations, employer perspectives, and assessments of existing services remain necessary.

The purpose of this analysis is to provide a broader evidence base that helps organisations make more informed choices, strengthen the rationale for their programmes, and identify questions that require further investigation.

### 6. Turning analysis into an interactive tool

I translated the findings into a six-tab interactive dashboard covering the national overview, state comparisons, structural differences, enterprise structure, statistical evidence, and forecasting outlook.

The dashboard was designed to make the findings easier to explore while keeping methodological qualifications visible. I also worked on a static version alongside the original Gradio application.

This involved reviewing the visual presentation, checking chart behaviour, correcting issues in statistical notation and chart labels, and auditing the exported data.

The final verification process reported 69,214 data-integrity checks passed with zero failures. A separate numerical consistency audit reported matching analytical findings across the GitHub repository and both deployed dashboard versions.

### 7. Using AI tools responsibly

I used Antigravity IDE and AI-assisted tools to support parts of the development process, including code generation, debugging, test scaffolding, and consistency checks.

The project required reviewing outputs against the underlying analytical results and checking that the final presentation remained consistent with the data. This reinforced the importance of treating AI as an aid to development rather than a substitute for analytical judgement.

AI-assisted outputs still needed to be checked, and methodological decisions, interpretations, and limitations needed to be made explicit.

### 8. What I learned

This project reinforced the importance of connecting analytical results with their underlying data, validating model performance, and communicating uncertainty. A numerical result can be useful without providing a complete explanation of the social or economic processes behind it.

The analysis is descriptive and diagnostic. It does not establish that any particular factor caused the observed changes, nor does it measure the impact of a specific programme. The forecasts are exploratory and limited to a one-year horizon.

The principal outcome is a reproducible analytical project and an interactive tool that helps users examine women's labour-market patterns across different contexts. It provides a basis for further research and for framing more specific questions for programme design, policy analysis, and evaluation.

**This project demonstrates how data preparation, statistical reasoning, model validation, and clear visual communication can be brought together to make complex labour-market evidence more accessible and useful for decision-making.**

### Project Links
- **GitHub repository:** https://github.com/shijiabrham/women-labour-market-diagnostic
- **Static dashboard:** https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic-static
- **Gradio dashboard:** https://huggingface.co/spaces/shijiabraham/women-labour-market-diagnostic