import streamlit as st
import os
from datetime import datetime
from src.core.auth import autenticar, criar_usuario, gerar_token_reset, resetar_senha

def tela_login():
    st.markdown("""
    <style>
        .stApp { 
            background: #111111; 
        }
        
        .auth-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            padding: 20px;
        }
        
        .auth-box {
            max-width: 420px;
            width: 100%;
            padding: 40px 32px;
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 16px;
            text-align: center;
        }
        
        .auth-logo {
            font-size: 3rem;
            margin-bottom: 8px;
        }
        
        .auth-title {
            color: #E5E7EB;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }
        
        .auth-subtitle {
            color: #9CA3AF;
            font-size: 0.9rem;
            margin-bottom: 28px;
        }
        
        .auth-divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: #6B7280;
            font-size: 0.8rem;
        }
        
        .auth-divider::before,
        .auth-divider::after {
            content: "";
            flex: 1;
            height: 1px;
            background: #2D2D2D;
        }
        
        .auth-divider span {
            padding: 0 12px;
        }
        
        .auth-footer {
            text-align: center;
            margin-top: 16px;
            color: #6B7280;
            font-size: 0.8rem;
        }
        
        .auth-footer button {
            background: none;
            border: none;
            color: #22D3EE;
            cursor: pointer;
            font-size: 0.8rem;
            padding: 0;
            text-decoration: none;
        }
        
        .auth-footer button:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    # Inicializa estado da tela
    if "auth_tela" not in st.session_state:
        st.session_state.auth_tela = "login"

    # Centraliza o conteúdo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        
        # Logo e nome sempre visíveis
        logo_path = "assets/logo.png" if os.path.exists("assets/logo.png") else None
        if logo_path:
            st.image(logo_path, width=120)
        else:
            st.markdown('<div class="auth-logo">⚫</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="auth-title">FitControl</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Sistema de Gestão Fitness</div>', unsafe_allow_html=True)

        # ========== TELA DE LOGIN ==========
        if st.session_state.auth_tela == "login":
            usuario = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário",
                key="login_user",
                label_visibility="collapsed"
            )
            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                key="login_pass",
                label_visibility="collapsed"
            )
            
            if st.button("Entrar", use_container_width=True, type="primary"):
                if not usuario or not senha:
                    st.error("⚠️ Preencha todos os campos.")
                else:
                    with st.spinner("Entrando..."):
                        if autenticar(usuario, senha):
                            st.session_state.logado = True
                            st.session_state.usuario = usuario
                            st.session_state.ultima_atividade = datetime.now()
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha inválidos.")
            
            # Esqueci senha
            st.markdown('<div class="auth-footer">', unsafe_allow_html=True)
            if st.button("Esqueceu a senha?", key="btn_esqueci"):
                st.session_state.auth_tela = "reset"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Divisor
            st.markdown('<div class="auth-divider"><span>ou</span></div>', unsafe_allow_html=True)
            
            # Criar conta
            if st.button("Criar nova conta", use_container_width=True):
                st.session_state.auth_tela = "cadastro"
                st.rerun()

        # ========== TELA DE CADASTRO ==========
        elif st.session_state.auth_tela == "cadastro":
            nome = st.text_input("Nome completo", placeholder="Seu nome completo", key="cad_nome", label_visibility="collapsed")
            email = st.text_input("Email", placeholder="seu@email.com", key="cad_email", label_visibility="collapsed")
            senha = st.text_input("Senha", type="password", placeholder="Mínimo 4 caracteres", key="cad_senha", label_visibility="collapsed")
            confirmar = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha", key="cad_confirmar", label_visibility="collapsed")
            
            if st.button("Criar conta", use_container_width=True, type="primary"):
                if not nome or not email or not senha:
                    st.error("⚠️ Preencha todos os campos.")
                elif len(senha) < 4:
                    st.error("⚠️ A senha deve ter pelo menos 4 caracteres.")
                elif senha != confirmar:
                    st.error("⚠️ As senhas não coincidem.")
                else:
                    with st.spinner("Criando conta..."):
                        sucesso, msg = criar_usuario(email, nome, senha)
                        if sucesso:
                            st.success(f"✅ {msg}")
                            st.session_state.auth_tela = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
            
            st.markdown('<div class="auth-footer">', unsafe_allow_html=True)
            if st.button("← Já tenho uma conta", key="btn_voltar_cad"):
                st.session_state.auth_tela = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ========== TELA DE RESET ==========
        elif st.session_state.auth_tela == "reset":
            if "reset_token" not in st.session_state:
                st.markdown('<p style="color:#9CA3AF;font-size:0.85rem;">Digite seu email para receber o código</p>', unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="seu@email.com", key="reset_email", label_visibility="collapsed")
                
                if st.button("Enviar código", use_container_width=True, type="primary"):
                    if not email:
                        st.error("⚠️ Informe seu email.")
                    else:
                        token = gerar_token_reset(email)
                        st.session_state.reset_token = token
                        st.session_state.reset_email = email
                        st.success(f"✅ Código: **{token}**")
                
                st.markdown('<div class="auth-footer">', unsafe_allow_html=True)
                if st.button("← Voltar", key="btn_voltar_reset"):
                    st.session_state.auth_tela = "login"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info(f"📧 {st.session_state.reset_email}")
                codigo = st.text_input("Código", placeholder="Digite o código", key="reset_codigo", label_visibility="collapsed")
                nova = st.text_input("Nova senha", type="password", placeholder="Nova senha", key="reset_nova", label_visibility="collapsed")
                
                if st.button("Alterar senha", use_container_width=True, type="primary"):
                    if not codigo or not nova:
                        st.error("⚠️ Preencha todos os campos.")
                    elif len(nova) < 4:
                        st.error("⚠️ Senha muito curta.")
                    else:
                        sucesso, msg = resetar_senha(codigo, nova)
                        if sucesso:
                            st.success(f"✅ {msg}")
                            del st.session_state.reset_token
                            del st.session_state.reset_email
                            st.session_state.auth_tela = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                
                st.markdown('<div class="auth-footer">', unsafe_allow_html=True)
                if st.button("← Cancelar", key="btn_cancelar_reset"):
                    if "reset_token" in st.session_state:
                        del st.session_state.reset_token
                    if "reset_email" in st.session_state:
                        del st.session_state.reset_email
                    st.session_state.auth_tela = "login"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer global
    st.markdown("""
    <div style="text-align:center; margin-top:20px; color:#6B7280; font-size:0.75rem;">
        © 2026 FitControl · v2.0
    </div>
    """, unsafe_allow_html=True)
