# src/ui/layout.py
import streamlit as st

def aplicar_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0A0F0A 0%, #0D1A0D 100%);
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A0A0A 0%, #0F1F0F 100%);
            border-right: 2px solid #2ECC40;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #7CFC00 !important;
            font-weight: 700 !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #2ECC40 0%, #1B8C2E 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(46, 204, 64, 0.25);
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #7CFC00 0%, #2ECC40 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46, 204, 64, 0.4);
        }
        
        .stMetric {
            background: linear-gradient(145deg, #1A2A1A 0%, #0F1F0F 100%);
            border: 1px solid #2ECC40;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        .stMetric label {
            color: #AAFFAA !important;
            font-weight: 600 !important;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: white !important;
            font-size: 2.2rem !important;
        }
        
        .stDataFrame {
            background: #111A11;
            border: 1px solid #2ECC40;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .stDataFrame th {
            background-color: #1B2E1B !important;
            color: #7CFC00 !important;
            font-weight: 600 !important;
        }
        
        .stTextInput input, .stNumberInput input, .stSelectbox div {
            background-color: #1A2A1A !important;
            color: white !important;
            border: 1px solid #2ECC40 !important;
            border-radius: 6px !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div:focus {
            border-color: #7CFC00 !important;
            box-shadow: 0 0 8px rgba(124, 252, 0, 0.3);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0F1F0F;
            border-radius: 10px 10px 0 0;
            border: 1px solid #2ECC40;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #2ECC40 !important;
            color: black !important;
            border-radius: 8px 8px 0 0;
        }
        
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #1B2E1B 0%, #0F1F0F 100%);
            color: #7CFC00 !important;
            border: 1px solid #2ECC40;
            border-radius: 8px;
            font-weight: 600;
        }
        
        .streamlit-expanderContent {
            background-color: #0A0F0A;
            border: 1px solid #2ECC40;
            border-radius: 0 0 8px 8px;
        }
        
        .stForm {
            background: linear-gradient(145deg, #1A2A1A 0%, #0F1F0F 100%);
            border: 1px solid #2ECC40;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        }
        
        .stAlert {
            border-radius: 8px;
        }
        
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #2ECC40, transparent);
            margin: 20px 0;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0A0A0A;
        }
        ::-webkit-scrollbar-thumb {
            background: #2ECC40;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

def logo_sidebar():
    import os
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=200)
    else:
        st.sidebar.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <span style="font-size:3rem;">🟢</span>
            <h2 style="color:#7CFC00; margin:0;">FITCONTROL</h2>
            <p style="color:#AAFFAA; font-size:0.9rem;">Sistema de Gestão Fitness</p>
        </div>
        """, unsafe_allow_html=True)

def rodape():
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center; color:#7CFC00; padding:10px;">
        <small>© 2026 FitControl</small><br>
        <small style="color:#AAFFAA;">v2.0 Profissional</small>
    </div>
    """, unsafe_allow_html=True)
