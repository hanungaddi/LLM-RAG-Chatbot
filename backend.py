# backend.py
import os
import asyncio
from flask import Flask, request, jsonify
from core.agent import DatabaseAgent
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

print("🚀 Starting backend server...")

API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.path.join("db", "toko_online.db")

if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set!")
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database not found at {DB_PATH}. Please run 'python db/populate_db.py' first.")

agent = DatabaseAgent(api_key=API_KEY, db_path=DB_PATH)
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
async def chat():
    """
    Endpoint untuk menerima prompt dan histori, lalu mengembalikan respon dari agent.
    """
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Invalid request body, 'prompt' is required."}), 400

        prompt = data["prompt"]

        history_data = data.get("history", [])
        
        history = ModelMessagesTypeAdapter.validate_python(history_data)

        response = await agent.run(prompt, message_history=history)

        new_history_dict = to_jsonable_python(response.all_messages())
        
        response_payload = {
            "output": response.output,
            "history": new_history_dict 
        }
        return jsonify(response_payload)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)