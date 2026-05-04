import streamlit as st
import os
from datetime import datetime
from src.core.auth import autenticar

def tela_login():
    st.markdown("""
    <style>
        .stApp {
            background: #111111;
        }
        .login-box {
            max-width: 380px;
            margin: 60px auto;
            padding: 40px 30px;
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 12px;
            text-align: center;
        }
        .login-box h1 {
            color: #E5E7EB;
            font-size: 1.5rem;
            margin-bottom: 5px;
        }
        .login-box p {
            color: #9CA3AF;
            font-size: 0.85rem;
            margin-bottom: 25px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        logo_path = "assets/logo.png" if os.path.exists("assets/logo.png") else None
        if logo_path:
            st.image(logo_path, width=180)
        else:
            st.markdown("<span style='font-size:3rem;'>⚫</span>", unsafe_allow_html=True)
        
        st.markdown("<h1>FitControl</h1>", unsafe_allow_html=True)
        st.markdown("<p>Sistema de Gestão Fitness</p>", unsafe_allow_html=True)
        
        usuario = st.text_input("Usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar", use_container_width=True, type="primary"):
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
