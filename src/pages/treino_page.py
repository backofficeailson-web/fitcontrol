import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from datetime import datetime
from src.services.cliente_service import listar_clientes_cache, buscar_cliente_cache
from src.core.database import execute_query
from src.ui.feedback import sucesso, aviso

def _gerar_planilha(cliente, semanas=4, frequencia=3):
    objetivo = cliente.get('objetivo', 'Hipertrofia')
    agach = cliente.get('agachamento_1rm', 80)
    sup = cliente.get('supino_1rm', 60)
    terra = cliente.get('terra_1rm', 100)

    if objetivo == "Hipertrofia":
        fases = [
            {'series': 3, 'reps': '12-15', 'intensidade': 0.60, 'descanso': '45-60s'},
            {'series': 4, 'reps': '8-10', 'intensidade': 0.70, 'descanso': '60-90s'},
            {'series': 4, 'reps': '10-12', 'intensidade': 0.65, 'descanso': '45-60s'},
            {'series': 5, 'reps': '6-8', 'intensidade': 0.75, 'descanso': '90s'}
        ]
    elif objetivo == "Força Máxima":
        fases = [
            {'series': 4, 'reps': '6-8', 'intensidade': 0.75, 'descanso': '2-3min'},
            {'series': 5, 'reps': '4-5', 'intensidade': 0.85, 'descanso': '3-4min'},
            {'series': 6, 'reps': '2-3', 'intensidade': 0.92, 'descanso': '4-5min'},
            {'series': 3, 'reps': '3-4', 'intensidade': 0.80, 'descanso': '2-3min'}
        ]
    else:
        fases = [
            {'series': 5, 'reps': '3-5', 'intensidade': 0.50, 'descanso': '2min'},
            {'series': 6, 'reps': '2-3', 'intensidade': 0.60, 'descanso': '2-3min'},
            {'series': 4, 'reps': '3-4', 'intensidade': 0.55, 'descanso': '2min'},
            {'series': 5, 'reps': '5-6', 'intensidade': 0.45, 'descanso': '90s'}
        ]

    exercicios_base = {
        1: ["Agachamento Livre", "Agachamento Frontal", "Stiff", "Gêmeos"],
        2: ["Supino Reto", "Supino Fechado", "Desenvolvimento", "Tríceps"],
        3: ["Levantamento Terra", "Remada Curvada", "Barra Fixa", "Rosca Direta"],
    }
    if frequencia >= 4:
        exercicios_base[4] = ["Terra Déficit", "Box Squat", "Afundo", "Dips"]
    if frequencia == 5:
        exercicios_base[5] = ["Board Press", "Puxada Alta", "Crucifixo", "Remada Alta"]

    planilhas = {}
    for semana in range(1, semanas + 1):
        fase = fases[(semana - 1) % 4]
        registros = []
        for dia in range(1, frequencia + 1):
            registros.append({"DIA": f"▶ DIA {dia}", "EXERCÍCIO": f"DIA {dia}", "SÉRIES": "", "REPS": "", "CARGA (kg)": "", "DESCANSO": ""})
            for ex in exercicios_base.get(dia, exercicios_base[1]):
                if "Agachamento" in ex or "Box" in ex:
                    carga = round(agach * fase['intensidade'])
                elif "Supino" in ex or "Board" in ex:
                    carga = round(sup * fase['intensidade'])
                elif "Terra" in ex or "Stiff" in ex:
                    carga = round(terra * fase['intensidade'])
                else:
                    carga = round(agach * 0.4 * fase['intensidade'])
                registros.append({"DIA": f"  {dia}", "EXERCÍCIO": ex, "SÉRIES": fase['series'], "REPS": fase['reps'], "CARGA (kg)": f"{max(carga, 1)} kg", "DESCANSO": fase['descanso']})
            registros.append({"DIA": "", "EXERCÍCIO": "─" * 40, "SÉRIES": "", "REPS": "", "CARGA (kg)": "", "DESCANSO": ""})
        planilhas[f'Semana {semana:02d}'] = pd.DataFrame(registros)
    return planilhas

def _exportar_excel(planilhas, nome_cliente):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for nome_aba, df in planilhas.items():
            df.to_excel(writer, sheet_name=nome_aba.replace(' ', '_')[:31], index=False)
    b64 = base64.b64encode(output.getvalue()).decode()
    nome_arquivo = f"TREINO_{nome_cliente}_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
    return f'''
    <div style="text-align:center; padding:20px;">
        <a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}"
           download="{nome_arquivo}"
           style="background:linear-gradient(135deg,#6A1B9A 0%,#2ECC40 100%);color:white;padding:15px 30px;
                  text-decoration:none;border-radius:10px;font-size:18px;font-weight:bold;display:inline-block;
                  margin:10px;border:2px solid #7CFC00;">
            🟢 BAIXAR PLANILHA COMPLETA 🟢
        </a>
    </div>
    '''

def pagina_geracao_treino():
    st.title("📋 Gerar Planilha de Treino")
    clientes = listar_clientes_cache()
    if not clientes:
        aviso("Nenhum aluno ativo.")
        return
    opcoes = {c["nome"]: c["id"] for c in clientes}
    nome_sel = st.selectbox("Aluno", list(opcoes.keys()))
    cliente_id = opcoes[nome_sel]
    cliente = buscar_cliente_cache(cliente_id)
    if not cliente:
        st.error("Cliente não encontrado.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Objetivo", cliente.get('objetivo', '-'))
    col2.metric("📊 Nível", cliente.get('nivel', '-'))
    col3.metric("🏋️ Agachamento", f"{cliente.get('agachamento_1rm', '-')} kg")
    col4.metric("🏋️ Supino", f"{cliente.get('supino_1rm', '-')} kg")

    c1, c2, c3 = st.columns(3)
    with c1:
        semanas = st.select_slider("Semanas", options=[4, 8, 12, 16], value=4)
    with c2:
        freq = st.radio("Dias/semana", [3, 4, 5], horizontal=True)
    with c3:
        if st.button("🚀 GERAR", use_container_width=True):
            planilhas = _gerar_planilha(cliente, semanas=semanas, frequencia=freq)
            sucesso(f"Planilha gerada com {len(planilhas)} semanas!")
            st.markdown(_exportar_excel(planilhas, nome_sel), unsafe_allow_html=True)
            tabs = st.tabs(list(planilhas.keys()))
            for i, (nome, df) in enumerate(planilhas.items()):
                with tabs[i]:
                    df_display = df[df['EXERCÍCIO'].str.contains('─') == False]
                    dias_unicos = df_display[df_display['DIA'].str.startswith('▶', na=False)]['DIA'].tolist()
                    for dia_header in dias_unicos:
                        with st.expander(dia_header):
                            idx_inicio = df_display[df_display['DIA'] == dia_header].index[0]
                            idx_dias = df_display[df_display['DIA'].str.startswith('▶', na=False)].index
                            idx_fim = idx_dias[idx_dias > idx_inicio].min() if any(idx_dias > idx_inicio) else len(df_display)
                            df_dia = df_display.iloc[idx_inicio+1:idx_fim]
                            df_dia = df_dia[df_dia['EXERCÍCIO'] != '']
                            if not df_dia.empty:
                                st.dataframe(df_dia[['EXERCÍCIO','SÉRIES','REPS','CARGA (kg)','DESCANSO']], use_container_width=True, hide_index=True)
