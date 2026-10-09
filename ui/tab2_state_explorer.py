# -*- coding: utf-8 -*-
"""
ui/tab2_state_explorer.py
Tab 2: State Diagnostic Explorer & Context Profiles
Implements single-state diagnostic dossier, dual-state comparison (dumbbell/gap),
Phase 8 descriptive archetypes, and deterministic narratives.
Uses scripts/dataset_1_analytics.py and dataset_1_narratives.py directly.
"""

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import scripts.dataset_1_analytics as d1_analytics
import scripts.dataset_1_insights as d1_insights
import scripts.dataset_1_narratives as d1_narratives
from ui.common import get_state_archetype, render_kpi_card

def get_state_list():
    df = d1_analytics.load()
    return sorted(df.State.unique().tolist())

def render_state_badge(state_name: str) -> str:
    arch = get_state_archetype(state_name)
    return f"""
    <div style='background:#f8fafc; border-left:4px solid #2563eb; padding:12px 16px; border-radius:4px; margin-bottom:12px;'>
        <div style='font-size:14px; font-weight:700; color:#1e293b;'>
            {arch['icon']} {arch['name']}
        </div>
        <div style='font-size:12px; color:#475569; margin-top:4px;'>
            {arch['desc']}
        </div>
        <div style='font-size:11px; color:#94a3b8; margin-top:4px; font-style:italic;'>
            Descriptive State-level labour-market archetype from Phase 8 synthesis (not a formal statistical cluster).
        </div>
    </div>
    """

def get_state_kpis(state_name: str, year: int, indicator: str = "LFPR"):
    df = d1_analytics.load()
    sub_curr = df[(df.State == state_name) & (df.Year == year) & (df.Education == "All")]
    sub_base = df[(df.State == state_name) & (df.Year == 2017) & (df.Education == "All")]
    
    # Total Rural+Urban
    f_tot = sub_curr[(sub_curr.Gender == "Female") & (sub_curr.Area_Type == "Rural + Urban")][indicator].values
    m_tot = sub_curr[(sub_curr.Gender == "Male") & (sub_curr.Area_Type == "Rural + Urban")][indicator].values
    
    f_val = f_tot[0] if len(f_tot) > 0 and not np.isnan(f_tot[0]) else None
    m_val = m_tot[0] if len(m_tot) > 0 and not np.isnan(m_tot[0]) else None
    gap_val = (f_val - m_val) if (f_val is not None and m_val is not None) else None
    
    # 2017 baseline for delta
    f_base = sub_base[(sub_base.Gender == "Female") & (sub_base.Area_Type == "Rural + Urban")][indicator].values
    f_base_val = f_base[0] if len(f_base) > 0 and not np.isnan(f_base[0]) else None
    delta_val = (f_val - f_base_val) if (f_val is not None and f_base_val is not None) else None
    
    # Rural vs Urban
    f_r = sub_curr[(sub_curr.Gender == "Female") & (sub_curr.Area_Type == "Rural")][indicator].values
    f_u = sub_curr[(sub_curr.Gender == "Female") & (sub_curr.Area_Type == "Urban")][indicator].values
    r_val = f_r[0] if len(f_r) > 0 and not np.isnan(f_r[0]) else None
    u_val = f_u[0] if len(f_u) > 0 and not np.isnan(f_u[0]) else None
    ru_gap = (r_val - u_val) if (r_val is not None and u_val is not None) else None
    
    c1 = render_kpi_card(
        f"{state_name} Female {indicator}",
        f"{f_val:.1f}%" if f_val is not None else "N/A (Missing Sector)",
        f"{delta_val:+.1f} pp vs 2017" if delta_val is not None else "Baseline comparison N/A",
        f"Year {year}"
    )
    c2 = render_kpi_card(
        "Gender Gap (F − M)",
        f"{gap_val:+.1f} pp" if gap_val is not None else "N/A",
        f"Male: {m_val:.1f}%" if m_val is not None else "Male: N/A",
        "Disparity"
    )
    c3 = render_kpi_card(
        "Rural − Urban Female Gap",
        f"{ru_gap:+.1f} pp" if ru_gap is not None else "N/A (Missing Sector)",
        f"Rural: {r_val:.1f}% | Urban: {u_val:.1f}%" if (r_val and u_val) else "Incomplete Sector Data",
        "Spatial Divide"
    )
    return f"<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;'>{c1}{c2}{c3}</div>"

def render_state_plot(state_a: str, state_b: str, year: int, indicator: str = "LFPR"):
    df = d1_analytics.load()
    
    if not state_b or state_b == "None" or state_b == state_a:
        # SINGLE STATE TEMPORAL VIEW
        sub = df[(df.State == state_a) & (df.Education == "All")]
        years = sorted(sub.Year.unique())
        
        f_tot = [sub[(sub.Year == y) & (sub.Gender == "Female") & (sub.Area_Type == "Rural + Urban")][indicator].mean() for y in years]
        f_r = [sub[(sub.Year == y) & (sub.Gender == "Female") & (sub.Area_Type == "Rural")][indicator].mean() for y in years]
        f_u = [sub[(sub.Year == y) & (sub.Gender == "Female") & (sub.Area_Type == "Urban")][indicator].mean() for y in years]
        m_tot = [sub[(sub.Year == y) & (sub.Gender == "Male") & (sub.Area_Type == "Rural + Urban")][indicator].mean() for y in years]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=f_tot, mode='lines+markers', name='Female Total', line=dict(color='#2563eb', width=3)))
        fig.add_trace(go.Scatter(x=years, y=f_r, mode='lines+markers', name='Female Rural', line=dict(color='#16a34a', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=years, y=f_u, mode='lines+markers', name='Female Urban', line=dict(color='#d97706', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=years, y=m_tot, mode='lines+markers', name='Male Total', line=dict(color='#64748b', width=2, dash='dash')))
        
        fig.update_layout(
            title=f"Multi-Year Trajectory for {state_a} ({indicator})",
            xaxis_title="Year",
            yaxis_title=f"{indicator} (%)",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=380
        )
        return fig
    else:
        # DUAL STATE COMPARISON VIEW (Dumbbell Chart)
        categories = ["Female Total", "Male Total", "Female Rural", "Female Urban"]
        
        def get_vals(st):
            sub = df[(df.State == st) & (df.Year == year) & (df.Education == "All")]
            v_ft = sub[(sub.Gender == "Female") & (sub.Area_Type == "Rural + Urban")][indicator].values
            v_mt = sub[(sub.Gender == "Male") & (sub.Area_Type == "Rural + Urban")][indicator].values
            v_fr = sub[(sub.Gender == "Female") & (sub.Area_Type == "Rural")][indicator].values
            v_fu = sub[(sub.Gender == "Female") & (sub.Area_Type == "Urban")][indicator].values
            return [
                v_ft[0] if len(v_ft) > 0 and not np.isnan(v_ft[0]) else None,
                v_mt[0] if len(v_mt) > 0 and not np.isnan(v_mt[0]) else None,
                v_fr[0] if len(v_fr) > 0 and not np.isnan(v_fr[0]) else None,
                v_fu[0] if len(v_fu) > 0 and not np.isnan(v_fu[0]) else None
            ]
            
        vals_a = get_vals(state_a)
        vals_b = get_vals(state_b)
        
        fig = go.Figure()
        for cat, va, vb in zip(categories, vals_a, vals_b):
            if va is not None and vb is not None:
                fig.add_trace(go.Scatter(
                    x=[va, vb], y=[cat, cat],
                    mode='lines',
                    line=dict(color='#94a3b8', width=3),
                    showlegend=False
                ))
                
        fig.add_trace(go.Scatter(
            x=vals_a, y=categories,
            mode='markers+text',
            name=f"State A: {state_a}",
            marker=dict(size=14, color='#2563eb'),
            text=[f"{v:.1f}%" if v is not None else "N/A" for v in vals_a],
            textposition="top center"
        ))
        fig.add_trace(go.Scatter(
            x=vals_b, y=categories,
            mode='markers+text',
            name=f"State B: {state_b}",
            marker=dict(size=14, color='#e11d48'),
            text=[f"{v:.1f}%" if v is not None else "N/A" for v in vals_b],
            textposition="top center"
        ))
        
        fig.update_layout(
            title=f"Dumbbell Comparison: {state_a} vs. {state_b} ({indicator}, Year {year})",
            xaxis_title=f"{indicator} (%)",
            yaxis_title="Segment",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=80, r=40, t=60, b=40),
            height=380
        )
        return fig

def render_state_narrative(state_a: str, year: int, indicator: str = "LFPR") -> str:
    try:
        raw_df = d1_analytics.load()
        filtered_df = d1_analytics.filter_data(raw_df, state=state_a, area_type="Rural + Urban", education="All", gender="Female")
        trend_df = d1_analytics.trend(filtered_df, indicator=indicator, dimensions=["Year"])
        
        ctx = d1_insights.AnalyticalContext(
            indicators=[indicator],
            dimensions=["Year"],
            filters={"state": state_a, "area_type": "Rural + Urban", "education": "All", "gender": "Female"},
            analysis_type="trend",
            endpoint_years=(2017, year)
        )
        insights = d1_insights.detect_applicable_insights(ctx, trend_df)
        narratives = d1_narratives.generate_narratives(ctx, insights)
        
        text = f"### 📌 Deterministic State Dossier: {state_a}\n\n"
        if narratives:
            for n in narratives[:2]:
                text += f"**{n.get('headline', '')}**\n\n{n.get('key_finding', '')}\n\n"
                if n.get('change_statement'):
                    text += f"- *Change Statement:* {n.get('change_statement')}\n\n"
        else:
            text += f"In {year}, {state_a} exhibits key diagnostic patterns captured in Dataset 1.\n"
        return text
    except Exception:
        return f"### 📌 Deterministic State Dossier: {state_a}\n\nDiagnostic trajectory and profiles for {state_a} in {year}."

def build_tab2():
    states = get_state_list()
    default_state_a = "Bihar" if "Bihar" in states else states[0]
    default_state_b = "Kerala" if "Kerala" in states else "None"
    
    with gr.Tab("2. State Diagnostic Explorer"):
        gr.Markdown("## State Diagnostic Explorer & Context Profiles")
        gr.Markdown(
            "Select any Indian State or Union Territory to inspect its comprehensive labour-market dossier, "
            "contextual archetype badge, and deterministic narrative. Optionally select a comparator State."
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                state_a_dropdown = gr.Dropdown(choices=states, value=default_state_a, label="Primary State (State A)", info="Select focal State/UT")
                state_b_dropdown = gr.Dropdown(choices=["None"] + states, value=default_state_b, label="Comparator State (State B - Optional)", info="Select comparator State/UT")
                year_slider = gr.Slider(minimum=2017, maximum=2023, step=1, value=2023, label="Survey Year")
                indicator_radio = gr.Radio(choices=["LFPR", "WPR", "Unemployment_Rate"], value="LFPR", label="Indicator")
                
                archetype_output = gr.HTML(value=render_state_badge(default_state_a))
                narrative_output = gr.Markdown(value=render_state_narrative(default_state_a, 2023, "LFPR"))
                
            with gr.Column(scale=2):
                kpi_output = gr.HTML(value=get_state_kpis(default_state_a, 2023, "LFPR"))
                plot_output = gr.Plot(value=render_state_plot(default_state_a, default_state_b, 2023, "LFPR"))
                
        def update_tab2(st_a, st_b, yr, ind):
            badge = render_state_badge(st_a)
            kpis = get_state_kpis(st_a, yr, ind)
            fig = render_state_plot(st_a, st_b, yr, ind)
            nar = render_state_narrative(st_a, yr, ind)
            return badge, kpis, fig, nar

        inputs = [state_a_dropdown, state_b_dropdown, year_slider, indicator_radio]
        outputs = [archetype_output, kpi_output, plot_output, narrative_output]
        
        state_a_dropdown.change(fn=update_tab2, inputs=inputs, outputs=outputs)
        state_b_dropdown.change(fn=update_tab2, inputs=inputs, outputs=outputs)
        year_slider.change(fn=update_tab2, inputs=inputs, outputs=outputs)
        indicator_radio.change(fn=update_tab2, inputs=inputs, outputs=outputs)
