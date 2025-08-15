# core/agent.py
import sqlite3
from pydantic_ai import Agent
from pydantic_ai.agent import RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

class DatabaseAgent:
    """
    Sebuah kelas untuk mengenkapsulasi agent AI dan tools-nya
    yang berinteraksi dengan database SQLite.
    """
    def __init__(self, api_key: str, db_path: str):
        """
        Menginisialisasi agent saat sebuah instance dari kelas ini dibuat.
        
        Args:
            api_key (str): API key untuk layanan Groq.
            db_path (str): Path menuju file database SQLite.
        """
        self.db_path = db_path
        print("Initializing Groq Model and Pydantic Agent...")

        model = GroqModel(
            'openai/gpt-oss-20b',
            provider=GroqProvider(api_key=api_key)
        )

        self.agent = Agent(
            model=model,
            tools=[self.get_database_schema, self.run_sql_query]
        )

        print("Agent initialized successfully.")

    def get_database_schema(self, context: RunContext) -> str:
        """
        Tool: Mengambil skema CREATE TABLE dari database SQLite.
        Gunakan ini untuk memahami struktur tabel sebelum membuat query SQL.
        """
        print("Executing tool: get_database_schema")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
                schema_rows = cursor.fetchall()
                return "\n".join([row[0] for row in schema_rows])
        except sqlite3.Error as e:
            return f"Gagal mengambil skema: {e}"

    def run_sql_query(self, context: RunContext, sql_query: str) -> str:
        """
        Tool: Menjalankan query SQL SELECT pada database SQLite dan mengembalikan hasilnya.
        """
        print(f"Executing tool: run_sql_query with query: {sql_query}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                col_names = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(col_names, row)) for row in rows]
                return str(result)
        except sqlite3.Error as e:
            return f"Error saat menjalankan SQL: {e}"

    async def run(self, prompt: str, **kwargs):
        """
        Wrapper method untuk menjalankan agent. 
        """
        return await self.agent.run(prompt, **kwargs)
    