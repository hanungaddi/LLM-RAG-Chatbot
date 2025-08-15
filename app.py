# app.py
import os
from core.ui import ChatUI
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000/chat")

def main():
    """Fungsi utama untuk menjalankan frontend Streamlit."""
    print(f"🚀 Frontend is connecting to backend at: {BACKEND_URL}")
    
    ui = ChatUI(backend_url=BACKEND_URL)
    ui.run()

if __name__ == "__main__":
    main()