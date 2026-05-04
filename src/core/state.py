import streamlit as st

def get_cache_version():
    if "cache_version" not in st.session_state:
        st.session_state.cache_version = 1
    return st.session_state.cache_version

def bump_cache():
    st.session_state.cache_version = get_cache_version() + 1
