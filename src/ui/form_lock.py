import streamlit as st

def is_locked(key: str) -> bool:
    return st.session_state.get(key, False)

def lock(key: str):
    st.session_state[key] = True

def unlock(key: str):
    st.session_state[key] = False
