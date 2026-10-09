# -*- coding: utf-8 -*-
"""
ui/tab3_structural_faults.py
Tab 3: Structural Fault Lines
Implements the 3 approved sub-sections:
  A. Education and female participation (The U-Curve)
  B. Higher educated women's unemployment
  C. Rural-urban divergence
Uses scripts/dataset_1_analytics.py directly.
"""

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import scripts.dataset_1_analytics as d1_analytics

EDU_ORDER = [
    'Not Literate', 'Literate & Upto Primary', 'Middle', 'Secondary',
    'Higher Secondary', 'Diploma/ Certificate Course', 'Graduate', 'Post Graduate & Above'
]

def render_education_ucurve(area_type="Rural + Urban", year=2023):
    df = d1_analytics.load()
    sub = df[(df.Year == year) & (df.Area_Type == area_type) & (df.Education.isin(EDU_ORDER))]
    
    # Unweighted state averages
    f_means = [sub[(sub.Education == ed) & (sub.Gender == "Female")]["LFPR"].mean() for ed in EDU_ORDER]
    m_means = [sub[(sub.Education == ed) & (sub.Gender == "Male")]["LFPR"].mean() for ed in EDU_ORDER]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=EDU_ORDER, y=f_means,
        name='Female LFPR',
        marker_color='#2563eb',
        text=[f"{v:.1f}%" for v in f_means],
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=EDU_ORDER, y=m_means,
        name='Male LFPR',
        marker_color='#94a3b8',
        text=[f"{v:.1f}%" for v in m_means],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"The Education Gradient: Labour Force Participation Rate by Education Tier ({area_type}, {year})",
        xaxis_title="Educational Attainment",
        yaxis_title="LFPR (%) [Unweighted Analytical Mean]",
        yaxis=dict(range=[0, 100]),
        barmode='group',
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=100),
        height=420
    )
    return fig

def render_educated_unemployment(year=2023):
    df = d1_analytics.load()
    sub = df[(df.Year == year) & (df.Area_Type == "Rural + Urban") & (df.Education.isin(EDU_ORDER))]
    
    f_ur = [sub[(sub.Education == ed) & (sub.Gender == "Female")]["Unemployment_Rate"].mean() for ed in EDU_ORDER]
    m_ur = [sub[(sub.Education == ed) & (sub.Gender == "Male")]["Unemployment_Rate"].mean() for ed in EDU_ORDER]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=EDU_ORDER, y=f_ur,
        mode='lines+markers+text',
        name='Female Unemployment Rate',
        line=dict(color='#dc2626', width=3),
        marker=dict(size=9, color='#dc2626'),
        text=[f"{v:.1f}%" for v in f_ur],
        textposition='top center'
    ))
    fig.add_trace(go.Scatter(
        x=EDU_ORDER, y=m_ur,
        mode='lines+markers+text',
        name='Male Unemployment Rate',
        line=dict(color='#0284c7', width=2, dash='dash'),
        marker=dict(size=7, color='#0284c7'),
        text=[f"{v:.1f}%" for v in m_ur],
        textposition='bottom center'
    ))
    
    fig.update_layout(
        title=f"The Educated Unemployment Friction Gap across Education Tiers (Rural + Urban, {year})",
        xaxis_title="Educational Attainment",
        yaxis_title="Unemployment Rate (%) [Unweighted Mean]",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=100),
        height=420
    )
    return fig

def render_rural_urban_divergence():
    df = d1_analytics.load()
    sub = df[df.Education == "All"]
    years = sorted(sub.Year.unique())
    
    r_means = [sub[(sub.Year == y) & (sub.Gender == "Female") & (sub.Area_Type == "Rural")]["LFPR"].mean() for y in years]
    u_means = [sub[(sub.Year == y) & (sub.Gender == "Female") & (sub.Area_Type == "Urban")]["LFPR"].mean() for y in years]
    gap = [r - u for r, u in zip(r_means, u_means)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=r_means,
        mode='lines+markers',
        name='Rural Female LFPR',
        line=dict(color='#16a34a', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=years, y=u_means,
        mode='lines+markers',
        name='Urban Female LFPR',
        line=dict(color='#d97706', width=3)
    ))
    fig.add_trace(go.Bar(
        x=years, y=gap,
        name='Rural − Urban Gap (pp)',
        marker_color='#cbd5e1',
        text=[f"{g:.1f} pp" for g in gap],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Rural vs. Urban Female LFPR Trajectory and Gap Expansion (2017–2023)",
        xaxis_title="Survey Year",
        yaxis_title="LFPR / Gap (%)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=420
    )
    return fig

def build_tab3():
    with gr.Tab("3. Structural Fault Lines"):
        gr.Markdown("## Structural Fault Lines in India's Labour Market")
        gr.Markdown(
            "Explore the multidimensional structural divides established in the empirical analysis: "
            "the non-monotonic education participation gradient, the graduate unemployment bottleneck, "
            "and the widening rural-urban divergence."
        )
        
        with gr.Tabs():
            with gr.Tab("3.1 Education Gradient & U-Curve"):
                with gr.Row():
                    area_radio = gr.Radio(choices=["Rural + Urban", "Rural", "Urban"], value="Rural + Urban", label="Area Type")
                    year_slider = gr.Slider(minimum=2017, maximum=2023, step=1, value=2023, label="Survey Year")
                plot_u = gr.Plot(value=render_education_ucurve("Rural + Urban", 2023))
                gr.Markdown(
                    "> **Statistical Validation (Finding F5 & F8):** The Friedman test confirms that female LFPR varies systematically "
                    "> across education levels ($\chi^2 = 958.79, p < 0.001, \epsilon^2 = 0.542$). "
                    "> Participation troughs at Secondary (23.7%) and Higher Secondary (24.0%), well below non-literate women (36.5%). "
                    "> Furthermore, temporal expansion between 2017 and 2023 accrued disproportionately to lower-educated women (Finding F8: $\chi^2 = 66.36, p < 0.001$)."
                )
                
                area_radio.change(fn=render_education_ucurve, inputs=[area_radio, year_slider], outputs=plot_u)
                year_slider.change(fn=render_education_ucurve, inputs=[area_radio, year_slider], outputs=plot_u)
                
            with gr.Tab("3.2 Educated Unemployment Friction"):
                year_slider_ur = gr.Slider(minimum=2017, maximum=2023, step=1, value=2023, label="Survey Year")
                plot_ur = gr.Plot(value=render_educated_unemployment(2023))
                gr.Markdown(
                    "> **Statistical Validation (Finding F6):** The female-male unemployment difference varies systematically across education tiers "
                    "> (Friedman test $\chi^2 = 467.27, p < 0.001, \epsilon^2 = 0.262$). "
                    "> Open unemployment is negligible for non-literate workers ($< 0.5\%$), but surges to 23.3% for female graduates "
                    "> (compared to 10.7% for male graduates)—a gender gap of $+12.6$ pp."
                )
                year_slider_ur.change(fn=render_educated_unemployment, inputs=[year_slider_ur], outputs=plot_ur)
                
            with gr.Tab("3.3 Rural-Urban Divergence"):
                plot_ru = gr.Plot(value=render_rural_urban_divergence())
                gr.Markdown(
                    "> **Statistical Validation (Finding F4):** Rural female LFPR is systematically higher than Urban (Wilcoxon $W = 29,213.0, p < 0.001, r = 0.735$), "
                    "> and the rural-urban gap widened significantly across states from $4.7$ pp in 2017 to $19.8$ pp in 2023 "
                    "> (Wilcoxon change test $W = 625.0, p < 0.001, r = 0.858$)."
                )
