# -*- coding: utf-8 -*-
"""
ui/tab4_enterprise_structure.py
Tab 4: Employment & Enterprise Structure
Implements Dataset 2 non-agricultural enterprise distribution view.
Uses scripts/dataset_2_analytics.py directly.
Includes official source terminology and explicit handling of structural survey absence.
"""

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import scripts.dataset_2_analytics as d2_analytics
from ui.common import INDUSTRY_COVERAGE_MAP, REVERSE_INDUSTRY_COVERAGE_MAP

def render_enterprise_chart(ind_cov_label, year, area_type):
    # Map back to internal Dataset 2 value
    internal_ind = REVERSE_INDUSTRY_COVERAGE_MAP.get(ind_cov_label, "(05-99)")
    
    # Check for structural survey absence
    if internal_ind == "(014, 016, 017, 02-99)" and year in [2022, 2023]:
        # Return empty plot and explicit warning
        fig = go.Figure()
        fig.update_layout(
            title="Structural Survey Absence in PLFS Dataset 7131",
            template="plotly_white",
            height=380,
            annotations=[dict(
                text="⚠️ Structural Survey Absence: Industry Coverage (014, 016, 017, 02-99)<br>was not surveyed / reported in PLFS 2022–23 and 2023–24.<br>Data are available for 2017–2021 only.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="#b91c1c")
            )]
        )
        warning_msg = (
            "⚠️ **Structural Survey Absence Notice:** This industry coverage category is not available in the validated "
            "PLFS Dataset 7131 for 2022–2023. Data are available for 2017–2021 only. "
            "Values are NOT zero; the survey wave did not report this industry grouping."
        )
        return fig, warning_msg
        
    df = d2_analytics.load()
    sub = df[(df.Year == year) & (df.Industry_Division_Type == internal_ind) & (df.Area_Type == area_type)]
    
    ent_types = sorted(sub.Enterprise_Type.unique())
    
    f_shares = [sub[(sub.Enterprise_Type == et) & (sub.Gender == "Female")]["Percentage_Engaged"].mean() for et in ent_types]
    m_shares = [sub[(sub.Enterprise_Type == et) & (sub.Gender == "Male")]["Percentage_Engaged"].mean() for et in ent_types]
    
    # Clean NaNs to None
    f_clean = [v if not np.isnan(v) else 0.0 for v in f_shares]
    m_clean = [v if not np.isnan(v) else 0.0 for v in m_shares]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=ent_types, x=f_clean,
        orientation='h',
        name='Female % Engaged',
        marker_color='#2563eb',
        text=[f"{v:.1f}%" for v in f_clean],
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        y=ent_types, x=m_clean,
        orientation='h',
        name='Male % Engaged',
        marker_color='#94a3b8',
        text=[f"{v:.1f}%" for v in m_clean],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"Employment Distribution by Enterprise Type ({ind_cov_label}, {year}, {area_type})",
        xaxis_title="Persons Engaged by Enterprise Type (%) [Unweighted State Mean]",
        yaxis_title="Enterprise Category",
        barmode='group',
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=220, r=40, t=60, b=40),
        height=420
    )
    
    warning_msg = (
        "ℹ️ **Methodological Note on Dataset 2:** Metric represents *Persons engaged in the industry groups by enterprise type (%)* "
        "(Usual principal + subsidiary status ps+ss, NDAP Dataset 7131). "
        "Enterprise percentages are compositional shares within each subgroup; they do not represent absolute headcounts or population totals. "
        "Reported values are unweighted analytical state means."
    )
    return fig, warning_msg

def build_tab4():
    with gr.Tab("4. Employment & Enterprise Structure"):
        gr.Markdown("## Employment & Enterprise Structure (Dataset 2)")
        gr.Markdown(
            "Examine the institutional and enterprise landscape of non-agricultural employment using authoritative "
            "PLFS Dataset 7131 data. Analyzes how women and men are differently distributed across public, corporate, "
            "proprietary, and household enterprise types."
        )
        
        with gr.Row():
            ind_cov_dropdown = gr.Dropdown(
                choices=list(INDUSTRY_COVERAGE_MAP.values()),
                value="Non-agriculture, NIC 05–99",
                label="Industry Coverage",
                info="Mapped from Dataset 2 Industry Division Type"
            )
            year_dropdown = gr.Dropdown(
                choices=[2023, 2022, 2021, 2020, 2019, 2018, 2017],
                value=2023,
                label="Survey Year"
            )
            area_radio = gr.Radio(
                choices=["Rural + Urban", "Rural", "Urban"],
                value="Rural + Urban",
                label="Area Type"
            )
            
        initial_fig, initial_warn = render_enterprise_chart("Non-agriculture, NIC 05–99", 2023, "Rural + Urban")
        plot_ent = gr.Plot(value=initial_fig)
        warning_box = gr.Markdown(value=initial_warn)
        
        gr.Markdown("### Core Enterprise Patterns from Phase 6 Statistical Tests")
        with gr.Row():
            with gr.Column():
                gr.Markdown(
                    "**1. The Public Sector Anchor (Finding F11):**\n"
                    "Women are substantially more reliant on Government / Local Body / Public Sector enterprises "
                    "than men (24.9% vs. 16.0% nationwide in 2023, reaching over 33% in rural areas). "
                    "The gender enterprise distribution difference is statistically systematic (Wilcoxon $W = 31,878.0, p < 0.001, r = 0.867$)."
                )
            with gr.Column():
                gr.Markdown(
                    "**2. Proprietary Concentration & Domestic Service (Finding F10 & F11):**\n"
                    "Non-farm work is overwhelmingly informal, with 56.6% of women in Proprietary & Partnership enterprises. "
                    "Women are also $7\\times$ more likely than men to work in Employer Households (domestic staff: 6.3% vs. 0.8%), "
                    "while private corporate companies absorb only 8.3% of working women."
                )
                
        def update_tab4(ind, yr, ar):
            return render_enterprise_chart(ind, yr, ar)
            
        ind_cov_dropdown.change(fn=update_tab4, inputs=[ind_cov_dropdown, year_dropdown, area_radio], outputs=[plot_ent, warning_box])
        year_dropdown.change(fn=update_tab4, inputs=[ind_cov_dropdown, year_dropdown, area_radio], outputs=[plot_ent, warning_box])
        area_radio.change(fn=update_tab4, inputs=[ind_cov_dropdown, year_dropdown, area_radio], outputs=[plot_ent, warning_box])
