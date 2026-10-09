# -*- coding: utf-8 -*-
"""
ui/tab6_forecasting.py
======================
Tab 6: Forecasting Outlook (1-Year Horizon)
Renders time-series forecasting projections using the audited Phase 7 forecasting results.

Strict Architectural & Methodological Principles:
1. Single Source of Truth:
   - Reads directly from outputs/phase_7_ml/forecasting/forecast_results.csv.
   - Zero model fitting, recalculations, or heuristic adjustments in UI callbacks.
2. Dynamic Year & Scenario Handling:
   - Reads Historical_End_Year and Forecast_Year dynamically from selected scenario row.
   - Dynamically derives available State, Indicator, Gender, and Area choices from data.
   - No hardcoded 2023 or 2024 assumptions.
3. Three-State Eligibility Handling:
   - FORECAST_ELIGIBLE: Plots historical + projected point + empirical uncertainty interval.
   - FORECAST_ELIGIBLE_WITH_LIMITATIONS: Plots historical + projection with prominent caution banner.
   - FORECAST_NOT_SUPPORTED: Plots historical ONLY. Suppresses forecast point & uncertainty interval.
     Displays documented rejection reason. Never converts missing to zero.
4. Mandatory Audited Terminology:
   - "Empirical Uncertainty Interval (80% Nominal)"
   - "All-India Analytical Mean (Unweighted across 36 States/UTs)"
5. Mandatory Methodological Disclosure:
   - Explicitly explains why the outlook is strictly restricted to one year.
"""

from __future__ import annotations
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import gradio as gr

import scripts.dataset_1_analytics as d1_analytics
from ui.common import render_kpi_card

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORECAST_CSV_PATH = os.path.join(ROOT_DIR, "outputs", "phase_7_ml", "forecasting", "forecast_results.csv")

# UI Label constant for All-India level
ALL_INDIA_DISPLAY_LABEL = "All-India Analytical Mean (Unweighted across 36 States/UTs)"
ALL_INDIA_INTERNAL_KEY = "National (All States)"

# Internal cache
_forecast_df_cache: Optional[pd.DataFrame] = None

REQUIRED_FORECAST_COLUMNS = [
    "Level", "State", "Gender", "Area_Type", "Education", "Indicator",
    "Historical_End_Year", "Forecast_Year", "Forecast_Value",
    "Lower_Interval_80", "Upper_Interval_80", "Selected_Model",
    "Model_MAE", "Naive_Baseline_MAE", "MAE_Improvement_vs_Baseline",
    "Forecast_Horizon", "Eligibility_Status", "Eligibility_Reason"
]

def load_forecast_results(force_reload: bool = False, custom_path: Optional[str] = None) -> pd.DataFrame:
    """Load, validate, and cache approved forecast results.
    
    Supports controlled cache reload via force_reload=True or passing a custom_path.
    Validates required columns and uniqueness of keys prior to updating cache.
    """
    global _forecast_df_cache
    if _forecast_df_cache is None or force_reload or custom_path is not None:
        target_path = custom_path if custom_path is not None else FORECAST_CSV_PATH
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Forecast results file not found at: {target_path}")
            
        candidate_df = pd.read_csv(target_path)
        
        # Schema validation
        missing_cols = [c for c in REQUIRED_FORECAST_COLUMNS if c not in candidate_df.columns]
        if missing_cols:
            raise ValueError(f"Forecast results schema validation failed! Missing columns: {missing_cols}")
            
        # Key uniqueness validation for Education == 'All'
        all_edu = candidate_df[candidate_df["Education"] == "All"]
        dup_mask = all_edu.duplicated(subset=["State", "Indicator", "Gender", "Area_Type", "Education"], keep=False)
        if dup_mask.any():
            dup_keys = all_edu[dup_mask][["State", "Indicator", "Gender", "Area_Type"]].to_dict(orient="records")
            raise ValueError(f"Forecast results validation failed! Duplicate scenario keys detected: {dup_keys}")
            
        # Update cache once validated
        _forecast_df_cache = candidate_df
        
    return _forecast_df_cache

def get_scenario_metadata():
    """Dynamically extract available choices and default metadata from forecast results."""
    df = load_forecast_results()
    
    # Filter to Education == 'All' for the interactive outlook
    df_all_edu = df[df["Education"] == "All"]
    
    # States list: All-India label first, followed by sorted states
    states = sorted([s for s in df_all_edu["State"].unique() if s != ALL_INDIA_INTERNAL_KEY])
    state_choices = [ALL_INDIA_DISPLAY_LABEL] + states
    
    indicators = sorted(df_all_edu["Indicator"].unique().tolist())
    genders = sorted(df_all_edu["Gender"].unique().tolist())
    area_types = sorted(df_all_edu["Area_Type"].unique().tolist())
    
    # Latest observed base year and forecast year across results
    base_year = int(df_all_edu["Historical_End_Year"].max())
    forecast_year = int(df_all_edu["Forecast_Year"].max())
    
    return state_choices, indicators, genders, area_types, base_year, forecast_year

def resolve_scenario(state_display: str, indicator: str, gender: str, area_type: str) -> Optional[pd.Series]:
    """Retrieve exactly one unambiguous row from forecast_results.csv."""
    df = load_forecast_results()
    
    internal_state = ALL_INDIA_INTERNAL_KEY if state_display == ALL_INDIA_DISPLAY_LABEL else state_display
    
    matches = df[
        (df["State"] == internal_state) &
        (df["Indicator"] == indicator) &
        (df["Gender"] == gender) &
        (df["Area_Type"] == area_type) &
        (df["Education"] == "All")
    ]
    
    if len(matches) == 0:
        return None
    elif len(matches) > 1:
        raise ValueError(f"Ambiguous scenario keys! Found {len(matches)} matching rows for {internal_state}, {indicator}, {gender}, {area_type}.")
    return matches.iloc[0]

def render_forecasting_kpis(scenario_row: Optional[pd.Series], state_display: str, indicator: str) -> str:
    """Render dynamic status ribbon based on scenario row."""
    if scenario_row is None:
        return render_kpi_card("Scenario Status", "Data Unavailable", "No matching scenario found in results", "Error")
        
    status = scenario_row["Eligibility_Status"]
    base_yr = int(scenario_row["Historical_End_Year"]) if not pd.isna(scenario_row["Historical_End_Year"]) else "N/A"
    fc_yr = int(scenario_row["Forecast_Year"]) if not pd.isna(scenario_row["Forecast_Year"]) else "N/A"
    fc_val = scenario_row["Forecast_Value"]
    model_name = scenario_row["Selected_Model"]
    model_mae = scenario_row["Model_MAE"]
    naive_mae = scenario_row["Naive_Baseline_MAE"]
    lower_int = scenario_row["Lower_Interval_80"]
    upper_int = scenario_row["Upper_Interval_80"]
    
    # Validate interval bounds safely for display
    valid_int = (
        lower_int is not None and upper_int is not None and
        isinstance(lower_int, (int, float, np.number)) and
        isinstance(upper_int, (int, float, np.number)) and
        np.isfinite(lower_int) and np.isfinite(upper_int) and
        lower_int <= upper_int
    )
    
    if status == "FORECAST_ELIGIBLE":
        badge_style = "background:#dcfce7; color:#15803d;"
        badge_text = "FORECAST ELIGIBLE — VALIDATED"
        val_str = f"{fc_val:.2f}%" if pd.notna(fc_val) else "N/A"
        sub_str = f"Model: {model_name} (MAE: {model_mae:.2f} pp vs. Naive: {naive_mae:.2f} pp)"
        int_str = f"[{lower_int:.2f}%, {upper_int:.2f}%]" if valid_int else "Unavailable / Invalid"
    elif status == "FORECAST_ELIGIBLE_WITH_LIMITATIONS":
        badge_style = "background:#fef3c7; color:#b45309;"
        badge_text = "ELIGIBLE WITH LIMITATIONS — CAUTION"
        val_str = f"{fc_val:.2f}%" if pd.notna(fc_val) else "N/A"
        sub_str = f"Model: {model_name} (MAE: {model_mae:.2f} pp vs. Naive: {naive_mae:.2f} pp)"
        int_str = f"[{lower_int:.2f}%, {upper_int:.2f}%]" if valid_int else "Unavailable / Invalid"
    else:
        badge_style = "background:#fee2e2; color:#b91c1c;"
        badge_text = "FORECAST NOT SUPPORTED"
        val_str = "No Projection"
        sub_str = "Trend extrapolation unvalidated or series incomplete"
        int_str = "N/A (Projection Suppressed)"
        
    c1 = f"""
    <div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px 20px; box-shadow:0 1px 3px rgba(0,0,0,0.05); margin-bottom:12px;'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>
            <span style='color:#64748b; font-size:12px; font-weight:600; text-transform:uppercase;'>Eligibility Status</span>
            <span style='{badge_style} padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600;'>{badge_text}</span>
        </div>
        <div style='color:#0f172a; font-size:24px; font-weight:700;'>{status.replace('_', ' ')}</div>
        <div style='color:#64748b; font-size:12px; margin-top:4px;'>Base Year: {base_yr} → Outlook Year: {fc_yr}</div>
    </div>
    """
    
    c2 = render_kpi_card(
        f"{fc_yr} Point Forecast",
        val_str,
        sub_str,
        f"Horizon: 1-Year"
    )
    
    c3 = render_kpi_card(
        "Empirical Uncertainty Interval",
        int_str,
        "80% Nominal Bound (from validation residuals)",
        "Uncertainty"
    )
    
    return f"<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:12px;'>{c1}{c2}{c3}</div>"

def render_forecast_trajectory(
    state_display: str, indicator: str, gender: str, area_type: str, scenario_row: Optional[pd.Series]
) -> go.Figure:
    """Build dynamic Plotly trajectory chart combining historical data and forecast point."""
    fig = go.Figure()
    
    # 1. Historical Data Retrieval from Dataset 1 Reusable Analytical Layer
    df_d1 = d1_analytics.load()
    internal_state = ALL_INDIA_INTERNAL_KEY if state_display == ALL_INDIA_DISPLAY_LABEL else state_display
    
    if internal_state == ALL_INDIA_INTERNAL_KEY:
        # All-India unweighted analytical mean across 36 states/UTs
        hist_sub = df_d1[
            (df_d1["Education"] == "All") &
            (df_d1["Gender"] == gender) &
            (df_d1["Area_Type"] == area_type)
        ]
        hist_series = hist_sub.groupby("Year")[indicator].mean().reset_index()
    else:
        # State-specific series
        hist_sub = df_d1[
            (df_d1["State"] == internal_state) &
            (df_d1["Education"] == "All") &
            (df_d1["Gender"] == gender) &
            (df_d1["Area_Type"] == area_type)
        ]
        hist_series = hist_sub.sort_values("Year")[["Year", indicator]].dropna(subset=[indicator])
        
    hist_years = hist_series["Year"].tolist()
    hist_vals = hist_series[indicator].tolist()
    
    # Correction A: Handle empty historical series safely without hardcoded fallback
    if len(hist_years) == 0:
        fig.add_annotation(
            text="⚠️ No historical observations available for this series.",
            showarrow=False,
            font=dict(size=13, color="#b91c1c"),
            bgcolor="#fee2e2",
            bordercolor="#fca5a5",
            borderwidth=1,
            borderpad=8
        )
        fig.update_layout(
            title=f"Historical Trajectory: {indicator} ({state_display}) - No Data Available",
            template="plotly_white",
            height=420,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig
        
    base_year = int(max(hist_years))
    
    # Plot observed historical trajectory
    fig.add_trace(go.Scatter(
        x=hist_years,
        y=hist_vals,
        mode="lines+markers+text",
        name="Observed Historical Data",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=8, color="#2563eb"),
        text=[f"{v:.1f}%" for v in hist_vals],
        textposition="top center",
        textfont=dict(size=11, color="#1e3a8a")
    ))
        
    # Boundary line between historical and forecast
    boundary_x = base_year + 0.5
    fig.add_vline(
        x=boundary_x,
        line=dict(color="#94a3b8", width=1.5, dash="dot"),
        annotation_text="Forecast Horizon Start",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#64748b")
    )
    
    # Check scenario validity and uncertainty bounds
    is_eligible = scenario_row is not None and scenario_row.get("Eligibility_Status") in [
        "FORECAST_ELIGIBLE", "FORECAST_ELIGIBLE_WITH_LIMITATIONS"
    ]
    
    # Correction C: Check metadata consistency between historical endpoint and scenario metadata
    metadata_consistent = False
    inconsistency_msg = ""
    if is_eligible and scenario_row is not None:
        scen_hist_end = scenario_row.get("Historical_End_Year")
        scen_fc_yr = scenario_row.get("Forecast_Year")
        if pd.isna(scen_hist_end) or pd.isna(scen_fc_yr):
            inconsistency_msg = "Scenario metadata missing Historical_End_Year or Forecast_Year."
        elif int(scen_hist_end) != base_year:
            inconsistency_msg = f"Historical series endpoint ({base_year}) does not match scenario metadata ({int(scen_hist_end)})."
        elif int(scen_fc_yr) != base_year + 1:
            inconsistency_msg = f"Forecast year ({int(scen_fc_yr)}) is not strictly a 1-year horizon from base year ({base_year})."
        else:
            metadata_consistent = True

    # Correction E: Uncertainty interval validity check
    valid_interval = False
    lower_int = None
    upper_int = None
    if is_eligible and scenario_row is not None:
        raw_lower = scenario_row.get("Lower_Interval_80")
        raw_upper = scenario_row.get("Upper_Interval_80")
        if (raw_lower is not None and raw_upper is not None and
            isinstance(raw_lower, (int, float, np.number)) and
            isinstance(raw_upper, (int, float, np.number)) and
            np.isfinite(raw_lower) and np.isfinite(raw_upper) and
            raw_lower <= raw_upper):
            lower_int = float(raw_lower)
            upper_int = float(raw_upper)
            valid_interval = True

    # 2. Forecast Point & Interval Handling
    if is_eligible and metadata_consistent and scenario_row is not None:
        fc_yr = int(scenario_row["Forecast_Year"])
        fc_val = float(scenario_row["Forecast_Value"])
        last_hist_val = hist_vals[-1]
        
        # Dashed connector from last historical observation to forecast point
        fig.add_trace(go.Scatter(
            x=[base_year, fc_yr],
            y=[last_hist_val, fc_val],
            mode="lines",
            name="1-Year Projection Path",
            line=dict(color="#d97706", width=2.5, dash="dash"),
            showlegend=False
        ))
        
        # Uncertainty Interval Bar / Shaded Band at Forecast Year (if valid)
        if valid_interval and lower_int is not None and upper_int is not None:
            fig.add_trace(go.Scatter(
                x=[fc_yr, fc_yr],
                y=[lower_int, upper_int],
                mode="lines+markers",
                name="Empirical Uncertainty Interval (80% Nominal)",
                line=dict(color="#f59e0b", width=6),
                marker=dict(symbol="line-ew", size=14, color="#b45309"),
                hoverinfo="text",
                hovertext=f"80% Nominal Interval: [{lower_int:.2f}%, {upper_int:.2f}%]"
            ))
        
        # Forecast Point Marker
        fig.add_trace(go.Scatter(
            x=[fc_yr],
            y=[fc_val],
            mode="markers+text",
            name=f"Forecast Point ({scenario_row['Selected_Model']})",
            marker=dict(size=12, symbol="diamond", color="#d97706", line=dict(color="#78350f", width=1.5)),
            text=[f"{fc_val:.2f}% [Proj]"],
            textposition="top center",
            textfont=dict(size=11, color="#78350f", family="sans-serif")
        ))
        
        # Background shading for forecast outlook area
        fig.add_vrect(
            x0=boundary_x,
            x1=fc_yr + 0.5,
            fillcolor="rgba(245, 158, 11, 0.08)",
            layer="below",
            line_width=0,
            annotation_text=f"Model Outlook ({fc_yr})",
            annotation_position="bottom right",
            annotation_font=dict(size=11, color="#b45309")
        )
    elif is_eligible and not metadata_consistent:
        # Inconsistent metadata: suppress projection and show warning
        fig.add_annotation(
            x=base_year + 0.8,
            y=np.nanmean(hist_vals),
            text=f"⚠️ Projection Suppressed:<br>Metadata Inconsistency: {inconsistency_msg}",
            showarrow=False,
            font=dict(size=11, color="#b91c1c"),
            bgcolor="#fee2e2",
            bordercolor="#fca5a5",
            borderwidth=1,
            borderpad=6
        )
    elif scenario_row is not None:
        # Unsupported: annotate why forecast is not plotted
        fig.add_annotation(
            x=base_year + 0.8,
            y=np.nanmean(hist_vals),
            text=f"⚠️ Projection Suppressed:<br>{scenario_row['Eligibility_Reason']}",
            showarrow=False,
            font=dict(size=11, color="#b91c1c"),
            bgcolor="#fee2e2",
            bordercolor="#fca5a5",
            borderwidth=1,
            borderpad=6
        )

    # Layout styling & Y-axis scaling
    # Correction B: For FORECAST_NOT_SUPPORTED, scale strictly using historical data
    all_y = hist_vals.copy()
    if is_eligible and metadata_consistent and scenario_row is not None:
        if not pd.isna(scenario_row.get("Forecast_Value")):
            all_y.append(float(scenario_row["Forecast_Value"]))
        if valid_interval and lower_int is not None and upper_int is not None:
            all_y.extend([lower_int, upper_int])
            
    y_min = max(0.0, min(all_y) - 5.0)
    y_max = min(100.0, max(all_y) + 8.0)
    y_range = [y_min, y_max]

    fig.update_layout(
        title=f"Historical Trajectory and 1-Year Forecasting Outlook: {indicator} ({state_display})",
        xaxis=dict(
            title="Survey Wave / Projection Year",
            tickmode="linear",
            tick0=min(hist_years),
            dtick=1
        ),
        yaxis=dict(
            title=f"{indicator} (%)",
            range=y_range
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        margin=dict(l=50, r=40, t=60, b=40),
        height=420
    )
    return fig

def render_explanatory_markdown(scenario_row: Optional[pd.Series]) -> str:
    """Render analytical details, eligibility caution, and validation breakdown."""
    if scenario_row is None:
        return "⚠️ *Scenario not found in validated forecast results.*"
        
    status = scenario_row["Eligibility_Status"]
    reason = scenario_row["Eligibility_Reason"]
    model_name = scenario_row["Selected_Model"]
    model_mae = scenario_row["Model_MAE"]
    naive_mae = scenario_row["Naive_Baseline_MAE"]
    improvement = scenario_row["MAE_Improvement_vs_Baseline"]
    
    # Check interval validity
    valid_interval = False
    raw_lower = scenario_row.get("Lower_Interval_80")
    raw_upper = scenario_row.get("Upper_Interval_80")
    if (raw_lower is not None and raw_upper is not None and
        isinstance(raw_lower, (int, float, np.number)) and
        isinstance(raw_upper, (int, float, np.number)) and
        np.isfinite(raw_lower) and np.isfinite(raw_upper) and
        raw_lower <= raw_upper):
        valid_interval = True
        
    interval_note = ""
    if status in ["FORECAST_ELIGIBLE", "FORECAST_ELIGIBLE_WITH_LIMITATIONS"] and not valid_interval:
        interval_note = "\n\n> ⚠️ **Note:** Empirical uncertainty interval is unavailable or invalid for this scenario; point forecast is displayed without interval bounds."
    
    if status == "FORECAST_ELIGIBLE":
        status_box = (
            f"> 🟢 **Validated Forecast:** This scenario meets strict out-of-sample accuracy standards "
            f"($\\text{{MAE}} \\le 4.0$ pp) and demonstrates verifiable improvement over the Naive baseline. "
            f"The **{model_name}** model was deterministically selected across expanding historical validation origins."
        )
    elif status == "FORECAST_ELIGIBLE_WITH_LIMITATIONS":
        status_box = (
            f"> 🟡 **Caution — Eligible with Limitations:** {reason}\n"
            f"> Model: **{model_name}** achieved an out-of-sample MAE of {model_mae:.2f} pp. "
            f"Users should treat this outlook with caution, recognizing higher cyclical or baseline volatility."
        )
    else:
        status_box = (
            f"> 🔴 **Forecast Not Supported:** {reason}\n"
            f"> In accordance with empirical safeguards, projections for this scenario are **suppressed** "
            f"because error thresholds were exceeded or the historical series lacks continuous observations. "
            f"No arbitrary or zero values are plotted."
        )
        
    validation_detail = (
        f"**Model Selection & Backtesting Metrics:**\n"
        f"- Selected Model: `{model_name}`\n"
        f"- Out-of-Sample MAE across 3 Rolling Origins: `{model_mae:.2f} pp`\n"
        f"- Naive Baseline MAE: `{naive_mae:.2f} pp`\n"
        f"- Net Improvement over Baseline: `{improvement:+.2f} pp`"
    ) if status != "FORECAST_NOT_SUPPORTED" else (
        f"**Methodological Rejection Rationale:**\n"
        f"- Reason: {reason}\n"
        f"- Candidate Model MAE: `{model_mae} pp` vs. Naive Baseline: `{naive_mae} pp`"
    )
    
    return f"{status_box}{interval_note}\n\n{validation_detail}"

# Mandatory Methodological Note Text (Worded exactly as specified)
MANDATORY_FIVE_YEAR_NOTE_MD = """
### ⚠️ Methodological Disclosure: Why is the outlook limited to one year?

The available PLFS dataset contains seven annual observations, from 2017 to 2023. The forecasting models were evaluated using historical one-year-ahead validation. The available data do not provide sufficient independent historical periods to assess five-year-ahead forecast accuracy.

A separate feasibility assessment also found that some five-year trend projections produced implausible values, including labour-force participation rates above 100% and negative unemployment rates.

**For these reasons, the dashboard provides only eligible one-year-ahead forecasts.** Longer-term projections are not displayed because their reliability cannot be established adequately with the available data.

The forecasting analysis can be reassessed when additional annual observations become available.
"""

def build_tab6():
    """Construct Gradio UI components for Tab 6: Forecasting Outlook."""
    state_choices, indicators, genders, area_types, base_year, forecast_year = get_scenario_metadata()
    
    # Preferred defaults
    default_state = ALL_INDIA_DISPLAY_LABEL if ALL_INDIA_DISPLAY_LABEL in state_choices else state_choices[0]
    default_indicator = "LFPR" if "LFPR" in indicators else indicators[0]
    default_gender = "Female" if "Female" in genders else genders[0]
    default_area = "Rural + Urban" if "Rural + Urban" in area_types else area_types[0]
    
    initial_row = resolve_scenario(default_state, default_indicator, default_gender, default_area)
    
    with gr.Tab("6. Forecasting Outlook"):
        gr.Markdown(
            f"""
            ## Model-Based 1-Year Forecasting Outlook (Base: {base_year} → Outlook: {forecast_year})
            **Conditional time-series projections derived from annual Periodic Labour Force Survey (PLFS) data.**  
            *Note: Projections reflect statistical trend and level momentum from historical observations up to {base_year}. They represent model-based conditional projections for {forecast_year}, NOT observed post-{base_year} figures or official policy targets.*
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                state_dropdown = gr.Dropdown(
                    choices=state_choices,
                    value=default_state,
                    label="Geographic Level / State",
                    info="Select All-India benchmark or individual State/UT"
                )
                indicator_radio = gr.Radio(
                    choices=indicators,
                    value=default_indicator,
                    label="Labour Market Indicator",
                    info="Dataset 1 Core Measures"
                )
                gender_radio = gr.Radio(
                    choices=genders,
                    value=default_gender,
                    label="Gender Dimension",
                    info="Female vs. Male trajectory"
                )
                area_radio = gr.Radio(
                    choices=area_types,
                    value=default_area,
                    label="Area Type",
                    info="Spatial segmentation"
                )
                gr.Markdown(
                    "<div style='font-size:11px; color:#64748b; font-style:italic; margin-top:-8px;'>"
                    "Education is fixed at 'All'. Detailed education-level forecasting is excluded due to small-cell sampling noise."
                    "</div>"
                )
                
            with gr.Column(scale=3):
                kpi_output = gr.HTML(value=render_forecasting_kpis(initial_row, default_state, default_indicator))
                plot_output = gr.Plot(value=render_forecast_trajectory(default_state, default_indicator, default_gender, default_area, initial_row))
                explanatory_output = gr.Markdown(value=render_explanatory_markdown(initial_row))
                
        # Mandatory Five-Year Limitation Disclosure
        with gr.Accordion("Methodological Disclosure: Why is the outlook limited to one year?", open=True):
            gr.Markdown(MANDATORY_FIVE_YEAR_NOTE_MD)
            
        with gr.Accordion("Time-Series Forecasting vs. Machine Learning Cross-Validation", open=False):
            gr.Markdown(
                """
                - **Time-Series Forecasting (Tab 6):** Evaluates *temporal momentum* forward in time ($t+1$). Models (Naive, Drift, SES, Holt) are validated using rolling expanding windows across 2021–2023.
                - **Machine Learning Predictive Modeling (Tab 5):** Evaluates *cross-sectional generalization* across space using 36-Fold Leave-One-State-Out (LOSO) validation. It explains ~15.5% of variance in the gender gap across unseen States using demographic predictors.
                - **Non-Causal Status:** Neither module establishes causal determinants. Both provide bounded, empirical evidence to guide program planning.
                """
            )

        # Dynamic Callback
        def update_tab6(st_val, ind_val, gen_val, ar_val):
            row = resolve_scenario(st_val, ind_val, gen_val, ar_val)
            kpis_html = render_forecasting_kpis(row, st_val, ind_val)
            fig = render_forecast_trajectory(st_val, ind_val, gen_val, ar_val, row)
            md_text = render_explanatory_markdown(row)
            return kpis_html, fig, md_text

        inputs = [state_dropdown, indicator_radio, gender_radio, area_radio]
        outputs = [kpi_output, plot_output, explanatory_output]
        
        state_dropdown.change(fn=update_tab6, inputs=inputs, outputs=outputs)
        indicator_radio.change(fn=update_tab6, inputs=inputs, outputs=outputs)
        gender_radio.change(fn=update_tab6, inputs=inputs, outputs=outputs)
        area_radio.change(fn=update_tab6, inputs=inputs, outputs=outputs)
