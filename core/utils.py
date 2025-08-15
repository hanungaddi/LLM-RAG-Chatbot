# core/utils.py
import streamlit as st
import os

def ensure_database_exists(db_path: str):
    """
    Memeriksa apakah file database ada. Jika tidak, hentikan aplikasi
    dengan pesan error yang informatif.
    """
    if not os.path.exists(db_path):
        st.error(f"Database tidak ditemukan di '{db_path}'. Harap jalankan 'python db/populate_db.py' terlebih dahulu.")
        st.stop()