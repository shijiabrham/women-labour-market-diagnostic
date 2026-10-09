# -*- coding: utf-8 -*-
"""
app.py
Main entry point for Women's Labour Market Diagnostic in India Gradio Application.
Hugging Face Spaces compatible.
Consumes authoritative analytical engines, Phase 1-8 outputs, and Phase 7 forecasting results.
"""

# Conditional ZeroGPU startup probe for Hugging Face Spaces
try:
    import spaces
    @spaces.GPU
    def _zerogpu_probe():
        pass
except ImportError:
    pass

import sys
import os

# Ensure project root is in sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import gradio as gr

from ui.tab1_overview import build_tab1
from ui.tab2_state_explorer import build_tab2
from ui.tab3_structural_faults import build_tab3
from ui.tab4_enterprise_structure import build_tab4
from ui.tab5_evidence import build_tab5
from ui.tab6_forecasting import build_tab6

def build_app():
    custom_css = """
    .gradio-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    """
    with gr.Blocks(title="Women's Labour Market Diagnostic in India", css=custom_css, theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🇮🇳 Women’s Labour Market Diagnostic in India
            ### Understanding women’s labour-market outcomes across States, education levels, and rural-urban contexts.
            """
        )
        
        with gr.Tabs():
            build_tab1()
            build_tab2()
            build_tab3()
            build_tab4()
            build_tab5()
            build_tab6()
            
        gr.Markdown(
            """
            ---
            <div style='text-align:center; color:#64748b; font-size:12px;'>
                Women's Labour Market Diagnostic in India • Capstone Research Diagnostic • Data Sources: PLFS NDAP Datasets 7129 & 7131 (2017–2023)
            </div>
            """
        )
    return demo

demo = build_app()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
