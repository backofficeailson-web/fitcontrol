import streamlit as st
from src.core.config import BG_DARK, BG_CARD, PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING, DANGER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER

def aplicar_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{
            background: {BG_DARK};
        }}
        
        section[data-testid="stSidebar"] {{
            background: #0D0D0D;
            border-right: 1px solid {BORDER};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_PRIMARY} !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
        }}
        
        h1 {{
            font-size: 1.8rem !important;
            border-bottom: 1px solid {BORDER};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        p, label, span, div {{
            color: {TEXT_PRIMARY} !important;
        }}
        
        .stButton>button {{
            background: {BG_CARD} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }}
        
        .stButton>button:hover {{
            border-color: {ACCENT} !important;
            color: {ACCENT} !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(34, 211, 238, 0.15) !important;
        }}
        
        .stButton>button[kind="primary"] {{
            background: {ACCENT} !important;
            color: #000 !important;
            border: 1px solid {ACCENT} !important;
            font-weight: 600 !important;
        }}
        
        .stButton>button[kind="primary"]:hover {{
            background: #38D9F5 !important;
            box-shadow: 0 4px 16px rgba(34, 211, 238, 0.3) !important;
        }}
        
        .stMetric {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 16px;
        }}
        
        .stMetric label {{
            color: {TEXT_SECONDARY} !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            color: {TEXT_PRIMARY} !important;
            font-size: 1.8rem !important;
            font-weight: 600 !important;
        }}
        
        .stMetric [data-testid="stMetricDelta"] {{
            color: {ACCENT} !important;
        }}
        
        .stDataFrame {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .stDataFrame th {{
            background: #141414 !important;
            color: {TEXT_SECONDARY} !important;
            font-weight: 500 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stDataFrame td {{
            color: {TEXT_PRIMARY} !important;
            font-size: 0.9rem !important;
        }}
        
        .stTextInput input, .stNumberInput input {{
            background: {BG_CARD} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 6px !important;
            font-size: 0.9rem !important;
        }}
        
        .stTextInput input:focus, .stNumberInput input:focus {{
            border-color: {ACCENT} !important;
            box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.15) !important;
        }}
        
        .stSelectbox > div > div {{
            background: {BG_CARD} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 6px !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background: transparent;
            border-bottom: 1px solid {BORDER};
            gap: 0;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {TEXT_SECONDARY} !important;
            font-weight: 500 !important;
            padding: 8px 16px !important;
            border-radius: 6px 6px 0 0 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {BG_CARD} !important;
            color: {ACCENT} !important;
            border: 1px solid {BORDER};
            border-bottom: 1px solid {BG_CARD};
        }}
        
        .streamlit-expanderHeader {{
            background: {BG_CARD};
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER};
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.9rem;
        }}
        
        .streamlit-expanderContent {{
            background: {BG_DARK};
            border: 1px solid {BORDER};
            border-top: none;
            border-radius: 0 0 6px 6px;
        }}
        
        .stForm {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 24px;
        }}
        
        .stAlert {{
            border-radius: 6px;
        }}
        
        .stSuccess {{
            background: rgba(74, 222, 128, 0.1) !important;
            border-left: 3px solid {SUCCESS} !important;
        }}
        
        .stWarning {{
            background: rgba(251, 191, 36, 0.1) !important;
            border-left: 3px solid {WARNING} !important;
        }}
        
        .stError {{
            background: rgba(248, 113, 113, 0.1) !important;
            border-left: 3px solid {DANGER} !important;
        }}
        
        .stInfo {{
            background: rgba(34, 211, 238, 0.1) !important;
            border-left: 3px solid {ACCENT} !important;
        }}
        
        hr {{
            border: none;
            height: 1px;
            background: {BORDER};
            margin: 24px 0;
        }}
        
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: {BG_DARK};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {BORDER};
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {PRIMARY};
        }}
        
        .stRadio > div {{
            gap: 10px;
        }}
        
        .stCheckbox {{
            color: {TEXT_PRIMARY} !important;
        }}
        
        .stDateInput > div > div {{
            background: {BG_CARD} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 6px !important;
        }}
        
        .stSlider > div > div > div {{
            background: {ACCENT} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def logo_sidebar():
    import os
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=180)
    else:
        st.sidebar.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <span style="font-size: 2.5rem;">⚫</span>
            <h3 style="color:#E5E7EB; margin:5px 0; font-weight:600;">FITCONTROL</h3>
            <p style="color:#9CA3AF; font-size:0.8rem;">Gestão Fitness</p>
        </div>
        """, unsafe_allow_html=True)

def rodape():
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center; padding:10px;">
        <small style="color:#9CA3AF;">© 2026 FitControl</small><br>
        <small style="color:#6B7280;">v2.0</small>
    </div>
    """, unsafe_allow_html=True)
