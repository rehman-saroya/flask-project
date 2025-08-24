from flask import Blueprint, request, jsonify, session
import os
from openai import OpenAI
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file.")
client = OpenAI(api_key=api_key)

# Blueprint
ai_routes = Blueprint('ai_routes', __name__)
DB_PATH = "cache.db"

# Ensure DB table exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompt_cache (
            prompt TEXT PRIMARY KEY,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@ai_routes.route("/api/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"response": "No prompt received."}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT response FROM prompt_cache WHERE prompt = ?", (prompt,))
        row = c.fetchone()

        if row:
            return jsonify({"response": row[0]})

        response = client.chat.completions.create(
            model="gpt-4omini" \
            "" \
            "" \
            "",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for software engineering topics."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()

        c.execute("INSERT INTO prompt_cache (prompt, response) VALUES (?, ?)", (prompt, answer))
        conn.commit()
        conn.close()

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@ai_routes.route("/api/clear_cache", methods=["POST"])
def clear_cache():
    if not session.get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM prompt_cache")
        conn.commit()
        conn.close()
        return jsonify({"message": "AI cache cleared."})
    except Exception as e:
        return jsonify({"error": f"Error clearing cache: {str(e)}"}), 500
