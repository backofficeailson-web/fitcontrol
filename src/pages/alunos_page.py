import streamlit as st
import pandas as pd
from src.services.cliente_service import (
    listar_clientes_cache,
    buscar_cliente_cache,
    criar_cliente,
    desativar_cliente,
    reativar_cliente,
)
from src.models.dto.cliente_dto import ClienteCreateDTO
from src.ui.feedback import sucesso, erro, aviso

def pagina_alunos():
    st.title("👥 Gestão de Alunos")
    tab1, tab2 = st.tabs(["➕ Cadastrar", "📋 Listar / Gerenciar"])

    with tab1:
        with st.form("form_cadastro", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome completo")
            telefone = col2.text_input("Telefone")
            col1, col2 = st.columns(2)
            mensalidade = col1.number_input("Mensalidade (R$)", min_value=0.0, step=10.0, value=100.0)
            vencimento = col2.text_input("Vencimento (ex: dia 10)", value="10")
            idade = st.number_input("Idade", 12, 100, 30)
            nivel = st.selectbox("Nível de experiência", [
                "Iniciante (Nível 1)", "Básico (Nível 2)", "Intermediário (Nível 3)",
                "Avançado (Nível 4)", "Elite (Nível 5)", "Competitivo (Nível 6)"
            ])
            objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Força Máxima", "Potência"])
            st.markdown("#### Testes de Força (1RM)")
            col1, col2, col3 = st.columns(3)
            agach = col1.number_input("Agachamento (kg)", 0.0, 500.0, 80.0)
            sup = col2.number_input("Supino (kg)", 0.0, 500.0, 60.0)
            terra = col3.number_input("Terra (kg)", 0.0, 500.0, 100.0)
            peg_dir = st.number_input("Pegada Mão Direita (kg)", 0.0, 200.0, 40.0)
            peg_esq = st.number_input("Pegada Mão Esquerda (kg)", 0.0, 200.0, 38.0)

            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if not nome.strip():
                    aviso("O nome não pode ficar vazio.")
                    return
                dto = ClienteCreateDTO(
                    nome=nome.strip(), telefone=telefone, mensalidade=mensalidade,
                    vencimento=vencimento, idade=idade, nivel=nivel, objetivo=objetivo,
                    agachamento_1rm=agach, supino_1rm=sup, terra_1rm=terra,
                    pegada_direita=peg_dir, pegada_esquerda=peg_esq
                )
                try:
                    criar_cliente(dto)
                    sucesso(f"Aluno {nome} cadastrado com sucesso!")
                except Exception as e:
                    erro(f"Erro ao cadastrar: {e}")

    with tab2:
        clientes = listar_clientes_cache()
        if not clientes:
            st.info("Nenhum aluno ativo encontrado.")
            return
        df = pd.DataFrame(clientes)
        st.dataframe(df[['id', 'nome', 'telefone', 'mensalidade', 'vencimento', 'nivel', 'objetivo']], use_container_width=True, hide_index=True)

        st.subheader("⚙️ Ações")
        ids_validos = [c['id'] for c in clientes]
        aluno_id = st.selectbox("Selecione o ID do aluno", ids_validos, format_func=lambda x: f"#{x}", key="sel_aluno_id")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Desativar", key="btn_desativar"):
                if aluno_id:
                    desativar_cliente(aluno_id)
                    sucesso(f"Aluno #{aluno_id} desativado.")
                    st.rerun()
        with col2:
            if st.button("✅ Reativar", key="btn_reativar"):
                if aluno_id:
                    reativar_cliente(aluno_id)
                    sucesso(f"Aluno #{aluno_id} reativado.")
                    st.rerun()
