import streamlit as st
import os
from datetime import datetime
from src.core.auth import autenticar

def tela_login():
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0A0A0A 0%, #0D3B0D 100%); }
        h1, p, label { color: #7CFC00 !important; }
        .stButton > button {
            background: linear-gradient(135deg, #2ECC40 0%, #0D3B0D 100%);
            color: white !important;
            border: 2px solid #7CFC00;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_path = "assets/logo.png" if os.path.exists("assets/logo.png") else None
        if logo_path:
            st.image(logo_path, width=250)
        else:
            st.markdown("<h1 style='text-align:center;color:#7CFC00;'>🟢 FITCONTROL</h1>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center;color:#7CFC00;'>Acesso ao Sistema</h3>", unsafe_allow_html=True)

        usuario = st.text_input("Usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", use_container_width=True):
            if not usuario or not senha:
                st.warning("Preencha usuário e senha.")
                return
            if autenticar(usuario, senha):
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.ultima_atividade = datetime.now()
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
