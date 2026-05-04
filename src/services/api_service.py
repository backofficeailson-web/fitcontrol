import requests
import streamlit as st
from src.core.config import API_BASE_URL

class ApiService:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = st.session_state.get("token")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                return True, "Login realizado com sucesso!"
            return False, response.json().get("detail", "Erro ao fazer login")
        except Exception as e:
            return False, f"Erro de conexão: {str(e)}"

    def register(self, email, password, nome):
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={"email": email, "password": password, "nome": nome}
            )
            if response.status_code == 200:
                return True, "Conta criada com sucesso!"
            return False, response.json().get("detail", "Erro ao criar conta")
        except Exception as e:
            return False, f"Erro de conexão: {str(e)}"

    def get_clientes(self):
        try:
            response = requests.get(
                f"{self.base_url}/clientes",
                headers=self._headers()
            )
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def criar_cliente(self, dados):
        try:
            response = requests.post(
                f"{self.base_url}/clientes",
                json=dados,
                headers=self._headers()
            )
            return response.status_code == 200
        except:
            return False

# Singleton
api = ApiService()
