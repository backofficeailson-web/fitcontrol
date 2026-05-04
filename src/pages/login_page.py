# src/pages/login_page.py
import streamlit as st
import os
from datetime import datetime
from src.core.auth import autenticar

def tela_login():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0A0F0A 0%, #0D1A0D 100%);
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px 30px;
            background: rgba(15, 30, 15, 0.9);
            border: 2px solid #2ECC40;
            border-radius: 16px;
            box-shadow: 0 0 30px rgba(46, 204, 64, 0.2);
            text-align: center;
        }
        .login-container h1 {
            color: #7CFC00;
            margin-bottom: 5px;
        }
        .login-container p {
            color: #AAFFAA;
            margin-bottom: 25px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        logo_path = "assets/logo.png" if os.path.exists("assets/logo.png") else None
        if logo_path:
            st.image(logo_path, width=200)
        else:
            st.markdown("<span style='font-size:4rem;'>🟢</span>", unsafe_allow_html=True)
        
        st.markdown("<h1>FitControl</h1>", unsafe_allow_html=True)
        st.markdown("<p>Sistema de Gestão Fitness</p>", unsafe_allow_html=True)
        
        usuario = st.text_input("Usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar", use_container_width=True):
            if not usuario or not senha:
                st.warning("Preencha todos os campos.")
                return
            if autenticar(usuario, senha):
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.ultima_atividade = datetime.now()
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
        
        st.markdown('</div>', unsafe_allow_html=True)
