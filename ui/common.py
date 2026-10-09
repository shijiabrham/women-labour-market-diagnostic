# -*- coding: utf-8 -*-
"""
ui/common.py
Common mappings, archetypes, and styling helpers for Phase 9.3 Gradio Dashboard.
Preserves non-causal, observational terminology and reusable engine mappings.
"""

# Official UI mapping for Dataset 2 Industry Coverage
# Internal value in D2 -> User-facing display label
INDUSTRY_COVERAGE_MAP = {
    "(05-99)": "Non-agriculture, NIC 05–99",
    "(014, 016, 017, 02-99)": "AGEGC + non-agriculture, NIC 014, 016, 017, 02–99"
}

# Reverse mapping for sending user selection back to dataset_2_analytics.py
REVERSE_INDUSTRY_COVERAGE_MAP = {
    v: k for k, v in INDUSTRY_COVERAGE_MAP.items()
}

# Descriptive Labour-Market Archetypes defined in Phase 8 Synthesis
# (Not mathematical or machine-learning clusters)
STATE_ARCHETYPES = {
    # 1. High-Participation Agrarian & Hill Context
    "Meghalaya": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Himachal Pradesh": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Sikkim": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Arunachal Pradesh": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Nagaland": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Chhattisgarh": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>55%), relatively narrow gender gaps (-10 to -24 pp), high rural engagement (>70%), and substantial public/community enterprise engagement."
    },
    "Ladakh": {
        "name": "High-Participation Agrarian & Hill Context",
        "icon": "🏔️",
        "desc": "High female participation (>50%), relatively narrow gender gaps, and high rural participation."
    },

    # 2. Rapid-Catchup Northern & Eastern Agrarian Context
    "Bihar": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Jharkhand": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Assam": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Odisha": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Madhya Pradesh": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Rajasthan": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, persistent substantial gender gaps (-27 to -35 pp in 2023), and pronounced rural-urban differences."
    },
    "Tripura": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, and persistent substantial gender gaps."
    },
    "Uttarakhand": {
        "name": "Rapid-Catchup Northern & Eastern Agrarian Context",
        "icon": "🌾",
        "desc": "Substantial temporal expansion (+20 to +38 pp since 2017) from historically low baselines, and persistent substantial gender gaps."
    },

    # 3. Moderate-Participation Peninsular & Diversified Context
    "Tamil Nadu": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and a marked gap in graduate unemployment."
    },
    "Andhra Pradesh": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and a marked gap in graduate unemployment."
    },
    "Telangana": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and a marked gap in graduate unemployment."
    },
    "Maharashtra": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and a marked gap in graduate unemployment."
    },
    "Karnataka": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and a marked gap in graduate unemployment."
    },
    "Kerala": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and marked female graduate unemployment exceeding 30%."
    },
    "Gujarat": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in corporate company employment in Dataset 2, and steady expansion."
    },
    "West Bengal": {
        "name": "Moderate-Participation Peninsular & Diversified Context",
        "icon": "🏭",
        "desc": "Moderate female participation (38%–47% in 2023), higher shares in non-farm employment, and persistent gender gaps."
    },

    # 4. Low-Participation Urban & Northern Enclave Context
    "Delhi": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), low urban female participation (<21%), and below-average temporal change."
    },
    "Haryana": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), low urban female participation (<21%), and below-average temporal change."
    },
    "Punjab": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), low urban female participation (<21%), and below-average temporal change."
    },
    "Uttar Pradesh": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), low urban female participation (<21%), and below-average temporal change."
    },
    "Goa": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), and slight decline in participation between 2017 and 2023."
    },
    "Lakshadweep": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps (-45 to -58 pp), and slight decline in participation between 2017 and 2023."
    },
    "Chandigarh": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps, and urban concentration."
    },
    "Puducherry": {
        "name": "Low-Participation Urban & Northern Enclave Context",
        "icon": "🏙️",
        "desc": "Persistently low female participation (<35%), wide gender gaps, and moderate temporal change."
    }
}

DEFAULT_ARCHETYPE = {
    "name": "Descriptive State-Level Context",
    "icon": "📊",
    "desc": "Descriptive labour-market profile from PLFS data."
}

def get_state_archetype(state_name: str) -> dict:
    return STATE_ARCHETYPES.get(state_name, DEFAULT_ARCHETYPE)

# Custom card styling helper for KPI cards
def render_kpi_card(title: str, value: str, subtext: str = "", badge: str = "") -> str:
    badge_html = f"<span style='background:#e2e8f0; color:#334155; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600;'>{badge}</span>" if badge else ""
    return f"""
    <div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px 20px; box-shadow:0 1px 3px rgba(0,0,0,0.05); margin-bottom:12px;'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>
            <span style='color:#64748b; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>{title}</span>
            {badge_html}
        </div>
        <div style='color:#0f172a; font-size:28px; font-weight:700; line-height:1.2;'>{value}</div>
        <div style='color:#64748b; font-size:12px; margin-top:4px;'>{subtext}</div>
    </div>
    """
