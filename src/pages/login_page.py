import streamlit as st
import os
from datetime import datetime
from src.core.auth import autenticar, criar_usuario, gerar_token_reset, resetar_senha

def tela_login():
    st.markdown("""
    <style>
        .stApp { background: #111111; }
        .auth-box {
            max-width: 400px;
            margin: 40px auto;
            padding: 35px 30px;
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 12px;
        }
        .auth-box h1 {
            color: #E5E7EB;
            font-size: 1.4rem;
            margin-bottom: 4px;
            text-align: center;
        }
        .auth-box p {
            color: #9CA3AF;
            font-size: 0.85rem;
            margin-bottom: 20px;
            text-align: center;
        }
        .auth-link {
            text-align: center;
            margin-top: 15px;
            color: #9CA3AF;
            font-size: 0.85rem;
        }
        .auth-link a {
            color: #22D3EE;
            text-decoration: none;
        }
        .auth-link a:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    # Inicializa estado da tela
    if "auth_tela" not in st.session_state:
        st.session_state.auth_tela = "login"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        
        logo_path = "assets/logo.png" if os.path.exists("assets/logo.png") else None
        if logo_path:
            st.image(logo_path, width=150)
        else:
            st.markdown("<div style='text-align:center;font-size:3rem;'>⚫</div>", unsafe_allow_html=True)

        # ========== TELA DE LOGIN ==========
        if st.session_state.auth_tela == "login":
            st.markdown("<h1>Entrar</h1>", unsafe_allow_html=True)
            st.markdown("<p>Acesse seu painel de gestão</p>", unsafe_allow_html=True)
            
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pass")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔐 Entrar", use_container_width=True, type="primary"):
                    if not usuario or not senha:
                        st.error("⚠️ Preencha todos os campos.")
                    else:
                        with st.spinner("Autenticando..."):
                            if autenticar(usuario, senha):
                                st.session_state.logado = True
                                st.session_state.usuario = usuario
                                st.session_state.ultima_atividade = datetime.now()
                                st.rerun()
                            else:
                                st.error("❌ Usuário ou senha inválidos.")
            
            st.markdown("""
            <div class="auth-link">
                <a href="#" onclick="alert('Em breve!')">Esqueceu a senha?</a>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📝 Criar nova conta", use_container_width=True):
                st.session_state.auth_tela = "cadastro"
                st.rerun()

        # ========== TELA DE CADASTRO ==========
        elif st.session_state.auth_tela == "cadastro":
            st.markdown("<h1>Criar Conta</h1>", unsafe_allow_html=True)
            st.markdown("<p>Comece agora mesmo</p>", unsafe_allow_html=True)
            
            nome = st.text_input("Nome completo", placeholder="Seu nome", key="cad_nome")
            email = st.text_input("Email", placeholder="seu@email.com", key="cad_email")
            senha = st.text_input("Senha", type="password", placeholder="Mínimo 4 caracteres", key="cad_senha")
            confirmar = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha", key="cad_confirmar")
            
            if st.button("✅ Criar conta", use_container_width=True, type="primary"):
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
            
            if st.button("← Voltar para login", use_container_width=True):
                st.session_state.auth_tela = "login"
                st.rerun()

        # ========== TELA DE RESET ==========
        elif st.session_state.auth_tela == "reset":
            st.markdown("<h1>Recuperar Senha</h1>", unsafe_allow_html=True)
            st.markdown("<p>Enviaremos um código de recuperação</p>", unsafe_allow_html=True)
            
            if "reset_token" not in st.session_state:
                email = st.text_input("Email cadastrado", placeholder="seu@email.com", key="reset_email")
                
                if st.button("📩 Enviar código", use_container_width=True, type="primary"):
                    if not email:
                        st.error("⚠️ Informe seu email.")
                    else:
                        token = gerar_token_reset(email)
                        st.session_state.reset_token = token
                        st.session_state.reset_email = email
                        st.success(f"✅ Código gerado: **{token}**")
                        st.info("💡 Em produção, este código seria enviado por email.")
                
                if st.button("← Voltar para login", use_container_width=True):
                    st.session_state.auth_tela = "login"
                    st.rerun()
            else:
                st.info(f"📧 Email: {st.session_state.reset_email}")
                codigo = st.text_input("Código recebido", placeholder="Digite o código", key="reset_codigo")
                nova_senha = st.text_input("Nova senha", type="password", placeholder="Nova senha", key="reset_nova")
                
                if st.button("✅ Alterar senha", use_container_width=True, type="primary"):
                    if not codigo or not nova_senha:
                        st.error("⚠️ Preencha todos os campos.")
                    elif len(nova_senha) < 4:
                        st.error("⚠️ Senha muito curta.")
                    else:
                        sucesso, msg = resetar_senha(codigo, nova_senha)
                        if sucesso:
                            st.success(f"✅ {msg}")
                            del st.session_state.reset_token
                            del st.session_state.reset_email
                            st.session_state.auth_tela = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                
                if st.button("← Cancelar", use_container_width=True):
                    if "reset_token" in st.session_state:
                        del st.session_state.reset_token
                    if "reset_email" in st.session_state:
                        del st.session_state.reset_email
                    st.session_state.auth_tela = "login"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


# Função para abrir o reset de senha a partir do login
def abrir_reset():
    st.session_state.auth_tela = "reset"
