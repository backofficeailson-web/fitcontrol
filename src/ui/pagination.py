import streamlit as st
import pandas as pd
from src.core.database import execute_query

DEFAULT_PAGE_SIZE = 20

def paginated_dataframe(query, count_query, params=(), columns=None, page_size=DEFAULT_PAGE_SIZE, key="page"):
    count_result = execute_query(count_query, params, fetchone=True)
    total = list(count_result.values())[0] if count_result else 0
    total_pages = max(1, -(-total // page_size))

    if key not in st.session_state:
        st.session_state[key] = 1

    page = st.session_state[key]
    page = max(1, min(page, total_pages))
    st.session_state[key] = page

    offset = (page - 1) * page_size
    rows = execute_query(query + " LIMIT ? OFFSET ?", params + (page_size, offset), fetch=True)

    if not rows:
        df = pd.DataFrame(columns=columns) if columns else pd.DataFrame()
    else:
        df = pd.DataFrame(rows)
        if columns:
            existing = [c for c in columns if c in df.columns]
            df = df[existing]

    return df, page, total_pages

def renderizar_controles_paginacao(page, total_pages, key="page"):
    if total_pages <= 1:
        return
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    with col1:
        if st.button("⏮", key=f"{key}_first", disabled=(page == 1)):
            st.session_state[key] = 1
            st.rerun()
    with col2:
        if st.button("◀", key=f"{key}_prev", disabled=(page == 1)):
            st.session_state[key] = page - 1
            st.rerun()
    with col3:
        st.markdown(f"<p style='text-align:center; color:#7CFC00;'>Página {page} de {total_pages}</p>", unsafe_allow_html=True)
    with col4:
        if st.button("▶", key=f"{key}_next", disabled=(page == total_pages)):
            st.session_state[key] = page + 1
            st.rerun()
    with col5:
        if st.button("⏭", key=f"{key}_last", disabled=(page == total_pages)):
            st.session_state[key] = total_pages
            st.rerun()
