# core/ui.py
import streamlit as st
import requests

class ChatUI:
    def __init__(self, backend_url: str):
        self.backend_url = backend_url
        self._initialize_page()
        self._initialize_session_state()

    def _initialize_page(self):
        st.set_page_config(page_title="AI Assistant Toko Online", page_icon="🤖")
        st.title("🤖 AI Assistant Frontend")
        st.caption(f"Terhubung ke backend di: {self.backend_url}")

    def _initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Halo! Ada yang bisa saya bantu?"}]
        if "json_history" not in st.session_state:
            st.session_state.json_history = []

    def _display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def _handle_input(self):
        if prompt := st.chat_input("Tanyakan sesuatu..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Menghubungi AI backend..."):
                    payload = {
                        "prompt": prompt,
                        "history": st.session_state.json_history
                    }
                    try:
                        # Panggil API backend
                        response = requests.post(self.backend_url, json=payload)
                        response.raise_for_status() # Cek jika ada error HTTP (spt 404, 500)
                        
                        data = response.json()
                        response_text = data["output"]
                        
                        st.session_state.json_history = data["history"]
                        
                    except requests.exceptions.RequestException as e:
                        response_text = f" Gagal terhubung ke backend: {e}"
                        st.error(response_text)
                    except Exception as e:
                        response_text = f" Terjadi error: {e}"
                        st.error(response_text)

                    st.markdown(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    def run(self):
        self._display_messages()
        self._handle_input()