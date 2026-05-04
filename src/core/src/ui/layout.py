import streamlit as st

def aplicar_css():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0A0A0A 0%, #0D3B0D 100%);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A0A0A 0%, #3D0F5C 100%);
        }
        h1, h2, h3 {
            color: #7CFC00 !important;
        }
        .stButton>button {
            background: linear-gradient(135deg, #2ECC40 0%, #0D3B0D 100%);
            color: white;
            border-radius: 10px;
            border: 2px solid #7CFC00;
        }
        .card {
            background: #1E1E1E;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #2ECC40;
        }
    </style>
    """, unsafe_allow_html=True)

def logo_sidebar():
    import os
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=180)
    else:
        st.sidebar.markdown("<h2 style='color:#7CFC00;'>🟢 FITCONTROL</h2>", unsafe_allow_html=True)

def rodape():
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center; margin-top:20px; color:#7CFC00;">
        <small>© 2026 FitControl — v1.0</small>
    </div>
    """, unsafe_allow_html=True)
