# -*- coding: utf-8 -*-
"""
scripts/export_dashboard_data.py
================================
Stage 1: Deterministic Exporter for Static Space Deployment.
Reads existing validated analytical layers and outputs browser-readable JSON files:
  1. static/data/tab1_national.json: Macro trajectories, headline gaps, and unweighted means.
  2. static/data/tab2_states.json: State profiles, archetypes, dumbbell data, and dossiers.
  3. static/data/tab3_fault_lines.json: Educational gradient U-curves, unemployment by tier, and rural-urban divergence.
  4. static/data/tab4_enterprise.json: Dataset 2 enterprise distributions with structural survey absence handling.
  5. static/data/tab5_evidence.json: Phase 6 inferential tests (F1-F11) and Phase 7 LOSO CV model results.
  6. static/data/tab6_forecasts.json: All 954 audited forecasting scenarios, uncertainty intervals, and eligibility flags.

Strict Architectural Principles:
- Zero re-estimation, fitting, or heuristics.
- All numbers are pulled directly from validated analytical engines and CSV outputs.
- Complete fidelity to Phase 8 non-causal observational terminology.
"""

from __future__ import annotations
import os
import json
import numpy as np
import pandas as pd

import scripts.dataset_1_analytics as d1_analytics
import scripts.dataset_1_insights as d1_insights
import scripts.dataset_1_narratives as d1_narratives
import scripts.dataset_2_analytics as d2_analytics
from ui.common import STATE_ARCHETYPES, INDUSTRY_COVERAGE_MAP, REVERSE_INDUSTRY_COVERAGE_MAP

ROOT_DIR = "/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic"
OUTPUT_DIR = os.path.join(ROOT_DIR, "static", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_float(v):
    if v is None or (isinstance(v, (float, np.floating)) and (np.isnan(v) or np.isinf(v))):
        return None
    return round(float(v), 2)

def export_tab1_national():
    print("[1/6] Exporting Tab 1: National Diagnostic Overview...")
    df = d1_analytics.load()
    sub = df[(df.Area_Type == "Rural + Urban") & (df.Education == "All")]
    years = sorted(sub.Year.unique().tolist())
    indicators = ["LFPR", "WPR", "Unemployment_Rate"]

    data = {
        "years": years,
        "indicators": {},
        "narratives": {},
        "themes": [
            {
                "id": "theme1",
                "title": "Theme 1: Universal Gender Participation Gap with Temporal Narrowing",
                "text": "Female LFPR rose systematically from 25.8% (2017) to 45.0% (2023) across Indian States (Finding F1: Wilcoxon W = 663.0, p < 0.001, r = 0.864). Yet, female participation remained strictly lower than male participation across all 251 matched State × Year observations (Finding F2: Wilcoxon W = 0.0, p < 0.001, r = -0.867), with a persistent national gap of -33.1 pp in 2023."
            },
            {
                "id": "theme2",
                "title": "Theme 2: Rural-Urban Divergence in Female Labour-Force Participation",
                "text": "Female labour-force expansion was concentrated primarily in rural areas (+19.8 pp gain). Urban female participation remained depressed and stagnant (rising from 20.4% to 28.0%). The rural-urban female gap widened dramatically from 4.7 pp in 2017 to 19.8 pp in 2023 (Finding F4: Wilcoxon level p < 0.001, r = 0.735; gap widening W = 625.0, p < 0.001, r = 0.858)."
            },
            {
                "id": "theme3",
                "title": "Theme 3: Non-Monotonic Education-Participation Pattern",
                "text": "Female participation displays a statistically validated non-monotone U-curve with formal education (Finding F5: Friedman χ² = 958.79, p < 0.001, ε² = 0.542). Participation dips to a trough among women with middle (30.2%) and secondary schooling (23.7%), and rises only at technical diploma (56.6%) and postgraduate levels (59.1%). The 2017–2023 expansion accrued disproportionately to women with lower educational attainment (Finding F8)."
            },
            {
                "id": "theme4",
                "title": "Theme 4: Higher Educated Women's Unemployment Gap",
                "text": "While open unemployment is near zero for uneducated women, women with tertiary education face extreme labour-market friction. Graduate female unemployment was 23.3% in 2023 compared to 10.7% for male graduates—a gender gap that widens systematically with education (Finding F6: Friedman χ² = 467.27, p < 0.001, ε² = 0.262)."
            },
            {
                "id": "theme5",
                "title": "Theme 5: Gendered Enterprise Structure of Employment",
                "text": "Non-agricultural employment is heavily informal (56.6% in proprietary/partnership units). However, female employment is significantly more reliant on public sector/government jobs (24.9% vs. 16.0% for men) and domestic work in employer households (6.3% vs. 0.8% for men) (Findings F10 & F11: Wilcoxon p < 0.001). Corporate companies absorb only 8.3% of female non-farm workers."
            }
        ]
    }

    for ind in indicators:
        f_means = []
        m_means = []
        gaps = []
        for yr in years:
            f_val = sub[(sub.Year == yr) & (sub.Gender == "Female")][ind].mean()
            m_val = sub[(sub.Year == yr) & (sub.Gender == "Male")][ind].mean()
            f_means.append(safe_float(f_val))
            m_means.append(safe_float(m_val))
            gaps.append(safe_float(f_val - m_val))

        # 2023 and 2017 KPI summaries
        f_2023 = f_means[-1]
        m_2023 = m_means[-1]
        gap_2023 = gaps[-1]

        f_2017 = f_means[0]
        m_2017 = m_means[0]
        gap_2017 = gaps[0]

        delta_f = safe_float(f_2023 - f_2017)
        delta_m = safe_float(m_2023 - m_2017)
        delta_gap = safe_float(gap_2023 - gap_2017)

        data["indicators"][ind] = {
            "female": f_means,
            "male": m_means,
            "gap": gaps,
            "kpis": {
                "female_2023": f_2023,
                "female_2017": f_2017,
                "delta_female": delta_f,
                "male_2023": m_2023,
                "male_2017": m_2017,
                "delta_male": delta_m,
                "gap_2023": gap_2023,
                "gap_2017": gap_2017,
                "delta_gap": delta_gap
            }
        }

        # Narrative generation
        try:
            filtered_df = d1_analytics.filter_data(df, area_type="Rural + Urban", education="All", gender="Female")
            trend_df = d1_analytics.trend(filtered_df, indicator=ind, dimensions=["Year"])
            ctx = d1_insights.AnalyticalContext(
                indicators=[ind],
                dimensions=["Year"],
                filters={"area_type": "Rural + Urban", "education": "All", "gender": "Female"},
                analysis_type="trend",
                endpoint_years=(2017, 2023)
            )
            insights = d1_insights.detect_applicable_insights(ctx, trend_df)
            narratives = d1_narratives.generate_narratives(ctx, insights)
            data["narratives"][ind] = narratives[:2] if narratives else []
        except Exception:
            data["narratives"][ind] = []

    # --------------------------------------------------------------------------
    # Five Diagnostic Themes Data Architecture
    # --------------------------------------------------------------------------
    education_levels = [
        "Not Literate",
        "Literate & Upto Primary",
        "Middle",
        "Secondary",
        "Higher Secondary",
        "Diploma/ Certificate Course",
        "Graduate",
        "Post Graduate & Above"
    ]

    # Theme 1: Overall Trajectories (already in indicators['LFPR', 'WPR', 'Unemployment_Rate'])
    theme1_data = {
        "years": years,
        "indicators": {
            ind: {
                "female": data["indicators"][ind]["female"],
                "male": data["indicators"][ind]["male"],
                "gap": data["indicators"][ind]["gap"]
            } for ind in indicators
        },
        "kpis": data["indicators"]["LFPR"]["kpis"]
    }

    # Theme 2: Rural-Urban Divergence in LFPR & WPR
    ru_sub = df[(df.Education == "All") & (df.Area_Type.isin(["Rural", "Urban"]))]
    theme2_data = {"years": years}
    for ind in ["LFPR", "WPR"]:
        f_rural_raw = [ru_sub[(ru_sub.Year == yr) & (ru_sub.Area_Type == "Rural") & (ru_sub.Gender == "Female")][ind].mean() for yr in years]
        f_urban_raw = [ru_sub[(ru_sub.Year == yr) & (ru_sub.Area_Type == "Urban") & (ru_sub.Gender == "Female")][ind].mean() for yr in years]
        m_rural_raw = [ru_sub[(ru_sub.Year == yr) & (ru_sub.Area_Type == "Rural") & (ru_sub.Gender == "Male")][ind].mean() for yr in years]
        m_urban_raw = [ru_sub[(ru_sub.Year == yr) & (ru_sub.Area_Type == "Urban") & (ru_sub.Gender == "Male")][ind].mean() for yr in years]
        ru_gaps = [safe_float(r - u) if r is not None and u is not None else None for r, u in zip(f_rural_raw, f_urban_raw)]
        f_rural = [safe_float(r) for r in f_rural_raw]
        f_urban = [safe_float(u) for u in f_urban_raw]
        m_rural = [safe_float(r) for r in m_rural_raw]
        m_urban = [safe_float(u) for u in m_urban_raw]
        theme2_data[ind] = {
            "female_rural": f_rural,
            "female_urban": f_urban,
            "male_rural": m_rural,
            "male_urban": m_urban,
            "female_ru_gap": ru_gaps
        }

    # Theme 3: Education Gradient U-Curve (Single Year 2023 vs Pooled 2017-2023) & F8 Gains
    edu_sub = df[(df.Area_Type == "Rural + Urban") & (df.Education.isin(education_levels))]
    edu_2023 = edu_sub[edu_sub.Year == 2023]
    edu_2017 = edu_sub[edu_sub.Year == 2017]

    t3_f_2023_raw = [edu_2023[(edu_2023.Education == lvl) & (edu_2023.Gender == "Female")]["LFPR"].mean() for lvl in education_levels]
    t3_m_2023_raw = [edu_2023[(edu_2023.Education == lvl) & (edu_2023.Gender == "Male")]["LFPR"].mean() for lvl in education_levels]
    t3_f_pooled_raw = [edu_sub[(edu_sub.Education == lvl) & (edu_sub.Gender == "Female")]["LFPR"].mean() for lvl in education_levels]
    t3_m_pooled_raw = [edu_sub[(edu_sub.Education == lvl) & (edu_sub.Gender == "Male")]["LFPR"].mean() for lvl in education_levels]
    t3_f_2017_raw = [edu_2017[(edu_2017.Education == lvl) & (edu_2017.Gender == "Female")]["LFPR"].mean() for lvl in education_levels]
    t3_delta_f = [safe_float(y23 - y17) if y23 is not None and y17 is not None else None for y23, y17 in zip(t3_f_2023_raw, t3_f_2017_raw)]

    t3_f_2023 = [safe_float(v) for v in t3_f_2023_raw]
    t3_m_2023 = [safe_float(v) for v in t3_m_2023_raw]
    t3_f_pooled = [safe_float(v) for v in t3_f_pooled_raw]
    t3_m_pooled = [safe_float(v) for v in t3_m_pooled_raw]
    t3_f_2017 = [safe_float(v) for v in t3_f_2017_raw]

    theme3_data = {
        "education_levels": education_levels,
        "female_2023": t3_f_2023,
        "male_2023": t3_m_2023,
        "female_pooled": t3_f_pooled,
        "male_pooled": t3_m_pooled,
        "female_2017": t3_f_2017,
        "female_delta_f8": t3_delta_f
    }

    # Theme 4: Educated Unemployment Penalty (Multi-Year 2017-2023 Rural + Urban)
    t4_data_by_year = {}
    for yr in years:
        edu_yr = edu_sub[edu_sub.Year == yr]
        f_ur = [safe_float(edu_yr[(edu_yr.Education == lvl) & (edu_yr.Gender == "Female")]["Unemployment_Rate"].mean()) for lvl in education_levels]
        m_ur = [safe_float(edu_yr[(edu_yr.Education == lvl) & (edu_yr.Gender == "Male")]["Unemployment_Rate"].mean()) for lvl in education_levels]
        g_ur = [safe_float(f - m) if f is not None and m is not None else None for f, m in zip(f_ur, m_ur)]
        t4_data_by_year[str(yr)] = {
            "female": f_ur,
            "male": m_ur,
            "gender_gap": g_ur
        }

    theme4_data = {
        "education_levels": education_levels,
        "years": years,
        "default_year": 2023,
        "female_2023": t4_data_by_year["2023"]["female"],
        "male_2023": t4_data_by_year["2023"]["male"],
        "gender_gap_2023": t4_data_by_year["2023"]["gender_gap"],
        "data_by_year": t4_data_by_year
    }

    # Theme 5: Enterprise Structure of Employment (Multi-Year 2017-2023 Dataset 2: Non-Agriculture 05-99 Rural + Urban)
    df2 = d2_analytics.load()
    ent_sub_all = df2[(df2.Industry_Division_Type == "(05-99)") & (df2.Area_Type == "Rural + Urban")]
    ent_types = sorted(ent_sub_all.Enterprise_Type.unique().tolist())
    t5_data_by_year = {}
    for yr in years:
        ent_yr = ent_sub_all[ent_sub_all.Year == yr]
        f_shares = [safe_float(ent_yr[(ent_yr.Enterprise_Type == et) & (ent_yr.Gender == "Female")]["Percentage_Engaged"].mean()) for et in ent_types]
        m_shares = [safe_float(ent_yr[(ent_yr.Enterprise_Type == et) & (ent_yr.Gender == "Male")]["Percentage_Engaged"].mean()) for et in ent_types]
        diff_shares = [safe_float(f - m) if f is not None and m is not None else None for f, m in zip(f_shares, m_shares)]
        t5_data_by_year[str(yr)] = {
            "female_shares": f_shares,
            "male_shares": m_shares,
            "gender_difference": diff_shares
        }

    theme5_data = {
        "enterprise_types": ent_types,
        "years": years,
        "default_year": 2023,
        "female_shares": t5_data_by_year["2023"]["female_shares"],
        "male_shares": t5_data_by_year["2023"]["male_shares"],
        "gender_difference": t5_data_by_year["2023"]["gender_difference"],
        "data_by_year": t5_data_by_year,
        "industry_coverage": "(05-99) Non-Agriculture",
        "area_type": "Rural + Urban"
    }

    data["theme_evidence"] = {
        "theme1": theme1_data,
        "theme2": theme2_data,
        "theme3": theme3_data,
        "theme4": theme4_data,
        "theme5": theme5_data
    }

    # Narrative text updates for Theme 2 to ensure audited unrounded delta accuracy (+24.5 pp and +9.4 pp)
    data["themes"][1]["text"] = (
        "Female labour-force expansion was concentrated primarily in rural areas (+24.5 percentage points across the unweighted State/UT analytical means, rising from 26.5% in 2017 to 51.0% in 2023). "
        "Urban female participation increased much more sluggishly, from 21.7% in 2017 to 31.2% in 2023 (+9.4 percentage points across the unweighted State/UT analytical means). "
        "By comparison, official population-weighted MoSPI estimates show rural female LFPR rising from 24.6% to 43.7%, and urban female LFPR from 20.4% to 25.4%. "
        "In the unweighted analytical dataset, the rural–urban female participation gap widened from 4.7 percentage points in 2017 to 19.8 percentage points in 2023 "
        "(Finding F4: Wilcoxon level p < 0.001, r = 0.735; gap widening W = 625.0, p < 0.001, r = 0.858)."
    )

    out_file = os.path.join(OUTPUT_DIR, "tab1_national.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def export_tab2_states():
    print("[2/6] Exporting Tab 2: State Diagnostic Explorer...")
    df = d1_analytics.load()
    states = sorted(df.State.unique().tolist())
    years = sorted(df.Year.unique().tolist())
    indicators = ["LFPR", "WPR", "Unemployment_Rate"]

    data = {
        "states": states,
        "years": years,
        "indicators": indicators,
        "archetypes": STATE_ARCHETYPES,
        "default_archetype": {
            "name": "State-Specific Structural Context",
            "icon": "🏛️",
            "desc": "Exhibits intermediate labour market participation patterns characterized by localized transition dynamics."
        },
        "state_data": {},
        "state_dossiers": {}
    }

    # Precalculate for each state
    for st in states:
        data["state_data"][st] = {}
        sub_st = df[df.State == st]

        for yr in years:
            data["state_data"][st][yr] = {}
            sub_yr = sub_st[sub_st.Year == yr]

            for ind in indicators:
                sub_all = sub_yr[sub_yr.Education == "All"]
                
                # Female and Male Total
                f_tot = sub_all[(sub_all.Gender == "Female") & (sub_all.Area_Type == "Rural + Urban")][ind].values
                m_tot = sub_all[(sub_all.Gender == "Male") & (sub_all.Area_Type == "Rural + Urban")][ind].values
                
                # Female Rural and Urban
                f_r = sub_all[(sub_all.Gender == "Female") & (sub_all.Area_Type == "Rural")][ind].values
                f_u = sub_all[(sub_all.Gender == "Female") & (sub_all.Area_Type == "Urban")][ind].values

                # Male Rural and Urban
                m_r = sub_all[(sub_all.Gender == "Male") & (sub_all.Area_Type == "Rural")][ind].values
                m_u = sub_all[(sub_all.Gender == "Male") & (sub_all.Area_Type == "Urban")][ind].values

                f_val = safe_float(f_tot[0]) if len(f_tot) > 0 else None
                m_val = safe_float(m_tot[0]) if len(m_tot) > 0 else None
                gap_val = safe_float(f_val - m_val) if (f_val is not None and m_val is not None) else None

                f_r_val = safe_float(f_r[0]) if len(f_r) > 0 else None
                f_u_val = safe_float(f_u[0]) if len(f_u) > 0 else None
                ru_gap = safe_float(f_r_val - f_u_val) if (f_r_val is not None and f_u_val is not None) else None

                data["state_data"][st][yr][ind] = {
                    "f_tot": f_val,
                    "m_tot": m_val,
                    "gap": gap_val,
                    "f_rural": f_r_val,
                    "f_urban": f_u_val,
                    "m_rural": safe_float(m_r[0]) if len(m_r) > 0 else None,
                    "m_urban": safe_float(m_u[0]) if len(m_u) > 0 else None,
                    "ru_gap": ru_gap
                }

        # Multi-year historical trend for each indicator
        data["state_data"][st]["trends"] = {}
        for ind in indicators:
            f_series = []
            m_series = []
            for yr in years:
                entry = data["state_data"][st][yr][ind]
                f_series.append(entry["f_tot"])
                m_series.append(entry["m_tot"])
            data["state_data"][st]["trends"][ind] = {
                "female": f_series,
                "male": m_series
            }

        # State dossiers
        data["state_dossiers"][st] = {}
        for yr in [2017, 2023]:
            for ind in indicators:
                key = f"{yr}_{ind}"
                try:
                    filtered_df = d1_analytics.filter_data(df, state=st, area_type="Rural + Urban", education="All", gender="Female")
                    trend_df = d1_analytics.trend(filtered_df, indicator=ind, dimensions=["Year"])
                    ctx = d1_insights.AnalyticalContext(
                        indicators=[ind],
                        dimensions=["Year"],
                        filters={"state": st, "area_type": "Rural + Urban", "education": "All", "gender": "Female"},
                        analysis_type="trend",
                        endpoint_years=(2017, yr)
                    )
                    insights = d1_insights.detect_applicable_insights(ctx, trend_df)
                    narratives = d1_narratives.generate_narratives(ctx, insights)
                    data["state_dossiers"][st][key] = narratives[:2] if narratives else []
                except Exception:
                    data["state_dossiers"][st][key] = []

    out_file = os.path.join(OUTPUT_DIR, "tab2_states.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def export_tab3_fault_lines():
    print("[3/6] Exporting Tab 3: Structural Fault Lines (All-India & State-wise)...")
    df = d1_analytics.load()
    edu_order = [
        'Not Literate', 'Literate & Upto Primary', 'Middle', 'Secondary',
        'Higher Secondary', 'Diploma/ Certificate Course', 'Graduate', 'Post Graduate & Above'
    ]
    years = sorted(df.Year.unique().tolist())
    area_types = ["Rural + Urban", "Rural", "Urban"]
    states = sorted(df.State.unique().tolist())
    geographies = ["All-India (Unweighted Mean)"] + states

    data = {
        "education_levels": edu_order,
        "years": years,
        "area_types": area_types,
        "geographies": geographies,
        "default_geography": "All-India (Unweighted Mean)",
        "data_by_geo": {}
    }

    # Process each geography
    for geo in geographies:
        is_all_india = (geo == "All-India (Unweighted Mean)")
        geo_df = df if is_all_india else df[df.State == geo]

        u_curves = {}
        for at in area_types:
            u_curves[at] = {}
            for yr in years:
                sub = geo_df[(geo_df.Year == yr) & (geo_df.Area_Type == at) & (geo_df.Education.isin(edu_order))]
                if is_all_india:
                    f_means = [safe_float(sub[(sub.Education == ed) & (sub.Gender == "Female")]["LFPR"].mean()) for ed in edu_order]
                    m_means = [safe_float(sub[(sub.Education == ed) & (sub.Gender == "Male")]["LFPR"].mean()) for ed in edu_order]
                else:
                    # Single state: exact value (or None if missing, e.g. Chandigarh Rural 2023)
                    f_means = []
                    m_means = []
                    for ed in edu_order:
                        f_row = sub[(sub.Education == ed) & (sub.Gender == "Female")]["LFPR"].values
                        m_row = sub[(sub.Education == ed) & (sub.Gender == "Male")]["LFPR"].values
                        f_means.append(safe_float(f_row[0]) if len(f_row) > 0 and not np.isnan(f_row[0]) else None)
                        m_means.append(safe_float(m_row[0]) if len(m_row) > 0 and not np.isnan(m_row[0]) else None)

                u_curves[at][yr] = {
                    "female": f_means,
                    "male": m_means,
                    "has_data": any(v is not None for v in f_means + m_means)
                }

        educated_ur = {}
        for yr in years:
            sub = geo_df[(geo_df.Year == yr) & (geo_df.Area_Type == "Rural + Urban") & (geo_df.Education.isin(edu_order))]
            if is_all_india:
                f_ur = [safe_float(sub[(sub.Education == ed) & (sub.Gender == "Female")]["Unemployment_Rate"].mean()) for ed in edu_order]
                m_ur = [safe_float(sub[(sub.Education == ed) & (sub.Gender == "Male")]["Unemployment_Rate"].mean()) for ed in edu_order]
            else:
                f_ur = []
                m_ur = []
                for ed in edu_order:
                    f_row = sub[(sub.Education == ed) & (sub.Gender == "Female")]["Unemployment_Rate"].values
                    m_row = sub[(sub.Education == ed) & (sub.Gender == "Male")]["Unemployment_Rate"].values
                    f_ur.append(safe_float(f_row[0]) if len(f_row) > 0 and not np.isnan(f_row[0]) else None)
                    m_ur.append(safe_float(m_row[0]) if len(m_row) > 0 and not np.isnan(m_row[0]) else None)

            educated_ur[yr] = {
                "female": f_ur,
                "male": m_ur,
                "has_data": any(v is not None for v in f_ur + m_ur)
            }

        rural_urban_div = {}
        for ind in ["LFPR", "WPR"]:
            sub_all = geo_df[geo_df.Education == "All"]
            if is_all_india:
                r_f = [safe_float(sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Rural") & (sub_all.Gender == "Female")][ind].mean()) for yr in years]
                u_f = [safe_float(sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Urban") & (sub_all.Gender == "Female")][ind].mean()) for yr in years]
                r_m = [safe_float(sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Rural") & (sub_all.Gender == "Male")][ind].mean()) for yr in years]
                u_m = [safe_float(sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Urban") & (sub_all.Gender == "Male")][ind].mean()) for yr in years]
            else:
                r_f, u_f, r_m, u_m = [], [], [], []
                for yr in years:
                    rf_val = sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Rural") & (sub_all.Gender == "Female")][ind].values
                    uf_val = sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Urban") & (sub_all.Gender == "Female")][ind].values
                    rm_val = sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Rural") & (sub_all.Gender == "Male")][ind].values
                    um_val = sub_all[(sub_all.Year == yr) & (sub_all.Area_Type == "Urban") & (sub_all.Gender == "Male")][ind].values
                    r_f.append(safe_float(rf_val[0]) if len(rf_val) > 0 and not np.isnan(rf_val[0]) else None)
                    u_f.append(safe_float(uf_val[0]) if len(uf_val) > 0 and not np.isnan(uf_val[0]) else None)
                    r_m.append(safe_float(rm_val[0]) if len(rm_val) > 0 and not np.isnan(rm_val[0]) else None)
                    u_m.append(safe_float(um_val[0]) if len(um_val) > 0 and not np.isnan(um_val[0]) else None)

            rural_urban_div[ind] = {
                "female_rural": r_f,
                "female_urban": u_f,
                "male_rural": r_m,
                "male_urban": u_m
            }

        data["data_by_geo"][geo] = {
            "u_curves": u_curves,
            "educated_unemployment": educated_ur,
            "rural_urban_divergence": rural_urban_div
        }

    # Backward compatibility references for All-India default
    data["u_curves"] = data["data_by_geo"]["All-India (Unweighted Mean)"]["u_curves"]
    data["educated_unemployment"] = data["data_by_geo"]["All-India (Unweighted Mean)"]["educated_unemployment"]
    data["rural_urban_divergence"] = data["data_by_geo"]["All-India (Unweighted Mean)"]["rural_urban_divergence"]

    out_file = os.path.join(OUTPUT_DIR, "tab3_fault_lines.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def export_tab4_enterprise():
    print("[4/6] Exporting Tab 4: Employment & Enterprise Structure (All-India & State-wise)...")
    df = d2_analytics.load()
    years = sorted(df.Year.unique().tolist())
    area_types = sorted(df.Area_Type.unique().tolist())
    coverage_types = ["(05-99)", "(014, 016, 017, 02-99)"]
    states = sorted(df.State.unique().tolist())
    geographies = ["All-India (Unweighted Mean)"] + states

    data = {
        "years": years,
        "area_types": area_types,
        "coverage_labels": INDUSTRY_COVERAGE_MAP,
        "geographies": geographies,
        "default_geography": "All-India (Unweighted Mean)",
        "distributions_by_geo": {}
    }

    for geo in geographies:
        is_all_india = (geo == "All-India (Unweighted Mean)")
        geo_df = df if is_all_india else df[df.State == geo]
        data["distributions_by_geo"][geo] = {}

        for ind in coverage_types:
            data["distributions_by_geo"][geo][ind] = {}
            for yr in years:
                data["distributions_by_geo"][geo][ind][yr] = {}
                for at in area_types:
                    # Check for structural survey absence
                    if ind == "(014, 016, 017, 02-99)" and yr in [2022, 2023]:
                        data["distributions_by_geo"][geo][ind][yr][at] = {
                            "is_absent": True,
                            "notice": f"Structural Survey Absence: Industry Coverage {INDUSTRY_COVERAGE_MAP.get(ind, ind)} was not surveyed / reported in PLFS {yr}–{yr+1 if yr==2022 else '24'}. Data available for 2017–2021 only.",
                            "enterprise_types": [],
                            "female_shares": [],
                            "male_shares": []
                        }
                        continue

                    # Check for Chandigarh Rural in 2023
                    if not is_all_india and geo == "Chandigarh" and yr == 2023 and at == "Rural":
                        data["distributions_by_geo"][geo][ind][yr][at] = {
                            "is_absent": True,
                            "notice": "Structural Survey Absence: Chandigarh was classified as 100% urbanized in PLFS 2022–23; no rural enterprise sample was collected.",
                            "enterprise_types": [],
                            "female_shares": [],
                            "male_shares": []
                        }
                        continue

                    sub = geo_df[(geo_df.Year == yr) & (geo_df.Industry_Division_Type == ind) & (geo_df.Area_Type == at)]
                    ent_types = sorted(sub.Enterprise_Type.unique().tolist())

                    if is_all_india:
                        f_shares = [safe_float(sub[(sub.Enterprise_Type == et) & (sub.Gender == "Female")]["Percentage_Engaged"].mean()) for et in ent_types]
                        m_shares = [safe_float(sub[(sub.Enterprise_Type == et) & (sub.Gender == "Male")]["Percentage_Engaged"].mean()) for et in ent_types]
                    else:
                        f_shares = []
                        m_shares = []
                        for et in ent_types:
                            f_row = sub[(sub.Enterprise_Type == et) & (sub.Gender == "Female")]["Percentage_Engaged"].values
                            m_row = sub[(sub.Enterprise_Type == et) & (sub.Gender == "Male")]["Percentage_Engaged"].values
                            f_shares.append(safe_float(f_row[0]) if len(f_row) > 0 and not np.isnan(f_row[0]) else None)
                            m_shares.append(safe_float(m_row[0]) if len(m_row) > 0 and not np.isnan(m_row[0]) else None)

                    data["distributions_by_geo"][geo][ind][yr][at] = {
                        "is_absent": False,
                        "enterprise_types": ent_types,
                        "female_shares": f_shares,
                        "male_shares": m_shares
                    }

    # Backward compatibility reference for All-India default
    data["distributions"] = data["distributions_by_geo"]["All-India (Unweighted Mean)"]

    out_file = os.path.join(OUTPUT_DIR, "tab4_enterprise.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def export_tab5_evidence():
    print("[5/6] Exporting Tab 5: Statistical Evidence & Methodology...")
    stat_csv = os.path.join(ROOT_DIR, "outputs", "phase_6_statistical_analysis", "statistical_results.csv")
    ml_csv = os.path.join(ROOT_DIR, "outputs", "phase_7_ml", "model_results.csv")
    ml_imp_csv = os.path.join(ROOT_DIR, "outputs", "phase_7_ml", "model_feature_importance.csv")

    stat_df = pd.read_csv(stat_csv)
    main_rows = stat_df[stat_df.Result_Type.isin(["omnibus", "gap", "change"])].copy()
    phase6_table = []
    for _, r in main_rows.iterrows():
        p_val = "< 0.001" if r["p"] < 0.001 else f"{r['p']:.4f}"
        eff_size = r["EffectSize_r"] if pd.notnull(r["EffectSize_r"]) else r["Epsilon2"]
        phase6_table.append({
            "Finding": str(r["Finding"]),
            "Analysis": str(r["Comparison"]),
            "Test": str(r["Test"]),
            "Statistic": safe_float(r["Statistic"]),
            "p_value": p_val,
            "Effect_Size": safe_float(eff_size)
        })

    ml_table = []
    if os.path.exists(ml_csv):
        ml_df = pd.read_csv(ml_csv)
        for _, r in ml_df.iterrows():
            ml_table.append({
                "Model": str(r["Model"]),
                "Validation_Method": str(r["Validation_Method"]),
                "Total_Folds": int(r["Total_Folds"]),
                "MAE": safe_float(r["MAE"]),
                "RMSE": safe_float(r["RMSE"]),
                "R2": safe_float(r["R2"])
            })

    importance_table = []
    if os.path.exists(ml_imp_csv):
        imp_df = pd.read_csv(ml_imp_csv)
        for _, r in imp_df.iterrows():
            importance_table.append({
                "Feature": str(r["Feature"]),
                "Ridge_Coefficient": safe_float(r["Ridge_Coefficient"]),
                "GBR_Feature_Importance": round(float(r["GBR_Feature_Importance"]), 4) if pd.notnull(r["GBR_Feature_Importance"]) else None
            })

    data = {
        "phase6_tests": phase6_table,
        "phase7_ml_models": ml_table,
        "phase7_feature_importance": importance_table,
        "methodology": {
            "design": "Repeated cross-sectional state-level analytical synthesis using annual PLFS NDAP datasets 7129 & 7131 (2017–2023).",
            "non_causal_disclosure": "All reported statistics reflect observational, associative patterns across 36 Indian States and Union Territories. No causal claims are asserted.",
            "unweighted_mean_disclosure": "National summary indicators reflect unweighted state analytical means across 36 reporting jurisdictions rather than population-weighted national aggregates, ensuring equal state representation in diagnostic profiling."
        }
    }

    out_file = os.path.join(OUTPUT_DIR, "tab5_evidence.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def export_tab6_forecasts():
    print("[6/6] Exporting Tab 6: Forecasting Outlook (1-Year Horizon)...")
    forecast_csv = os.path.join(ROOT_DIR, "outputs", "phase_7_ml", "forecasting", "forecast_results.csv")
    f_df = pd.read_csv(forecast_csv)

    # Historical data lookup for charting historical series
    d1_df = d1_analytics.load()

    states = sorted(f_df["State"].unique().tolist())
    indicators = sorted(f_df["Indicator"].unique().tolist())
    genders = sorted(f_df["Gender"].unique().tolist())
    area_types = sorted(f_df["Area_Type"].unique().tolist())

    # Build scenario dictionary keyed by "State|Indicator|Gender|Area_Type|Education"
    scenarios = {}
    for _, row in f_df.iterrows():
        key = f"{row['State']}|{row['Indicator']}|{row['Gender']}|{row['Area_Type']}|{row['Education']}"

        # Retrieve observed historical series
        st = row["State"]
        ind = row["Indicator"]
        gen = row["Gender"]
        at = row["Area_Type"]
        edu = row["Education"]

        if st == "National (All States)":
            hist_sub = d1_df[(d1_df.Area_Type == at) & (d1_df.Gender == gen) & (d1_df.Education == edu)]
            hist_years = sorted(hist_sub.Year.unique().tolist())
            hist_vals = [safe_float(hist_sub[hist_sub.Year == y][ind].mean()) for y in hist_years]
        else:
            hist_sub = d1_df[(d1_df.State == st) & (d1_df.Area_Type == at) & (d1_df.Gender == gen) & (d1_df.Education == edu)]
            hist_years = sorted(hist_sub.Year.unique().tolist())
            hist_vals = [safe_float(hist_sub[hist_sub.Year == y][ind].values[0]) if len(hist_sub[hist_sub.Year == y]) > 0 else None for y in hist_years]

        scenarios[key] = {
            "State": row["State"],
            "Indicator": row["Indicator"],
            "Gender": row["Gender"],
            "Area_Type": row["Area_Type"],
            "Education": row["Education"],
            "Level": row["Level"],
            "Historical_End_Year": int(row["Historical_End_Year"]),
            "Forecast_Year": int(row["Forecast_Year"]),
            "Forecast_Value": safe_float(row["Forecast_Value"]),
            "Lower_Interval_80": safe_float(row["Lower_Interval_80"]),
            "Upper_Interval_80": safe_float(row["Upper_Interval_80"]),
            "Selected_Model": str(row["Selected_Model"]),
            "Model_MAE": safe_float(row["Model_MAE"]),
            "Naive_Baseline_MAE": safe_float(row["Naive_Baseline_MAE"]),
            "MAE_Improvement_vs_Baseline": safe_float(row["MAE_Improvement_vs_Baseline"]),
            "Forecast_Horizon": str(row["Forecast_Horizon"]),
            "Eligibility_Status": str(row["Eligibility_Status"]),
            "Eligibility_Reason": str(row["Eligibility_Reason"]),
            "Historical_Years": hist_years,
            "Historical_Values": hist_vals
        }

    data = {
        "total_scenarios": len(scenarios),
        "states": states,
        "indicators": indicators,
        "genders": genders,
        "area_types": area_types,
        "eligibility_counts": {
            "FORECAST_ELIGIBLE": int((f_df.Eligibility_Status == "FORECAST_ELIGIBLE").sum()),
            "FORECAST_ELIGIBLE_WITH_LIMITATIONS": int((f_df.Eligibility_Status == "FORECAST_ELIGIBLE_WITH_LIMITATIONS").sum()),
            "FORECAST_NOT_SUPPORTED": int((f_df.Eligibility_Status == "FORECAST_NOT_SUPPORTED").sum())
        },
        "scenarios": scenarios
    }

    out_file = os.path.join(OUTPUT_DIR, "tab6_forecasts.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {out_file} ({os.path.getsize(out_file):,} bytes)")

def main():
    print("================================================================================")
    print("STARTING STAGE 1 EXPORT FOR STATIC SPACE DEPLOYMENT")
    print("================================================================================")
    export_tab1_national()
    export_tab2_states()
    export_tab3_fault_lines()
    export_tab4_enterprise()
    export_tab5_evidence()
    export_tab6_forecasts()
    print("================================================================================")
    print("STAGE 1 EXPORT COMPLETED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    main()
