# -*- coding: utf-8 -*-
"""
ui/tab5_evidence.py
Tab 5: Statistical Evidence, Predictive Limits & Methodology
Renders Phase 6 hypothesis table, Phase 7 ML limits (LOSO CV), and methodological boundaries.
Consumes outputs/phase_6_statistical_analysis/statistical_results.csv and phase_7_ml directly.
"""

import gradio as gr
import pandas as pd
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAT_CSV = os.path.join(ROOT, "outputs", "phase_6_statistical_analysis", "statistical_results.csv")
ML_CSV = os.path.join(ROOT, "outputs", "phase_7_ml", "model_results.csv")
ML_IMP_CSV = os.path.join(ROOT, "outputs", "phase_7_ml", "model_feature_importance.csv")

def load_phase6_table():
    if not os.path.exists(STAT_CSV):
        return pd.DataFrame()
    df = pd.read_csv(STAT_CSV)
    # Filter to main omnibus rows and key comparisons
    main_rows = df[df.Result_Type.isin(["omnibus", "gap", "change"])].copy()
    
    # Clean display columns
    display_df = pd.DataFrame({
        "Finding": main_rows["Finding"],
        "Analysis / Comparison": main_rows["Comparison"],
        "Test Applied": main_rows["Test"],
        "Test Statistic": main_rows["Statistic"].round(2),
        "p-value": main_rows["p"].apply(lambda p: "< 0.001" if p < 0.001 else f"{p:.4f}"),
        "Effect Size (r / ε²)": main_rows["EffectSize_r"].fillna(main_rows["Epsilon2"]).round(3)
    })
    return display_df

def load_ml_results():
    if not os.path.exists(ML_CSV):
        return pd.DataFrame()
    df = pd.read_csv(ML_CSV)
    return df[["Model", "Validation_Method", "Total_Folds", "MAE", "RMSE", "R2"]].round(3)

def load_ml_importance():
    if not os.path.exists(ML_IMP_CSV):
        return pd.DataFrame()
    df = pd.read_csv(ML_IMP_CSV)
    return df.round(4)

def build_tab5():
    with gr.Tab("5. Statistical Evidence, Predictive Limits & Methodology"):
        gr.Markdown("## Statistical Evidence, Predictive Limits & Methodology")
        gr.Markdown(
            "Complete scientific traceability for all empirical claims in the diagnostic. "
            "Exposes inferential hypothesis test results from Phase 6, predictive machine-learning "
            "bounds from Phase 7, and essential methodological boundaries."
        )
        
        with gr.Accordion("5.1 Phase 6 Inferential Hypothesis Testing Matrix (Findings F1–F11)", open=True):
            gr.Markdown(
                "Non-parametric statistical tests conducted on authoritative reusable analytical layers. "
                "Paired tests use matched within-state designs; omnibus multi-group tests use Friedman χ² with Bonferroni correction."
            )
            gr.Dataframe(value=load_phase6_table(), interactive=False)
            gr.Markdown(
                "- **Sample Size Note for Finding F2:** The inferential paired test was conducted on $n = 251$ matched State × Year observations "
                "(across 252 potential State-Year contexts, with 1 missing matched pair due to source missingness in Chandigarh Rural 2023).\n"
                "- **Permutation Test Note for Finding F3:** State variation permutation test ($p < 0.001$, variance $= 137.36$) establishes non-random spatial dispersion."
            )
            
        with gr.Accordion("5.2 Phase 7 Machine Learning: Predictive Boundaries & Out-of-Fold Limits", open=True):
            gr.Markdown(
                "Supervised regression predicting the **Female–Male LFPR Gap** (`LFPR_Female − LFPR_Male`) using "
                "`Education`, `Area_Type`, and `Year` under strict **36-Fold Leave-One-State-Out (LOSO) Cross-Validation**."
            )
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("### Out-of-Fold Model Performance (36 Folds, N = 4,024)")
                    gr.Dataframe(value=load_ml_results(), interactive=False)
                with gr.Column(scale=2):
                    gr.Markdown("### Feature Importance & Ridge Coefficients")
                    gr.Dataframe(value=load_ml_importance(), interactive=False)
                    
            gr.Markdown(
                """
                > ⚠️ **Critical Predictive & Non-Causal Boundary:**
                > - **The Explanatory Ceiling:** The best demographic model (Gradient Boosting) achieved an out-of-fold $R^2 = 0.155$, 
                > explaining approximately **15.5%** of variation in the gender gap for an unseen State.
                > - **Unexplained Variation (~84.5%):** Because State identity was deliberately excluded from predictors under LOSO validation, 
                > approximately 84.5% of variance remained unexplained by Education, Area Type, and Year alone.
                > - **Interpretation:** This demonstrates that demographic and temporal variables alone do not capture most of the variation 
                > across unseen States. Additional contextual, institutional, and regional factors are relevant, but this does NOT establish 
                > that State identity causally drives the unexplained gap.
                """
            )
            
        with gr.Accordion("5.3 Methodological Boundaries & Evidence Rules", open=False):
            gr.Markdown(
                """
                1. **Non-Causal Framework:** All empirical patterns, coefficients, and feature importances represent conditional statistical associations. No causal claims (e.g. 'education causes participation to fall') are made or supported.
                2. **Unweighted Analytical Means:** Unless specified otherwise, national and subgroup averages represent unweighted analytical means across reporting States/UTs, not population-weighted aggregates.
                3. **Zero Earnings / Wage Covariates:** PLFS activity status measures economic engagement, not compensation, job quality, or poverty status.
                4. **Dataset 2 Structural Truncation:** Industry Division `(014, 016, 017, 02-99)` is structurally missing in PLFS waves 2022–2023. It is suppressed from relevant charts and never plotted as zero.
                5. **Descriptive Archetypes:** The 4 State labour-market contexts described in Phase 8 and Tab 2 are descriptive qualitative archetypes based on observed multi-dimensional profiles, not formal statistical or machine-learning clusters.
                """
            )
