from flask import Flask, jsonify, render_template
import requests
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database file placed inside the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quote_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT,
            source TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    # Serve the frontend page
    return render_template("index.html")


@app.route("/quote", methods=["GET"])
def get_quote():
    """Fetch a random quote from the external API and store it in SQLite."""
    api_url = "https://api.quotable.io/random"

    # requests to external APIs can fail (no internet, blocked domain, etc.)
    # Keep the error message simple for the frontend.
    try:
        resp = requests.get(api_url, timeout=10, verify=False)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return jsonify({"error": "Failed to fetch quote. Check your internet connection or try again."}), 500

    quote_text = data.get("content", "").strip()
    author = data.get("author", "Unknown").strip() or "Unknown"

    if not quote_text:
        return jsonify({"error": "Quote API returned empty content."}), 500

    # Save to DB
    created_at = datetime.utcnow().isoformat() + "Z"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO quote_history (quote, author, source, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (quote_text, author, api_url, created_at),
    )
    conn.commit()
    conn.close()

    return jsonify({"quote": quote_text, "author": author, "created_at": created_at})


@app.route("/history", methods=["GET"])
def get_history():
    """Return previously generated quotes (latest first)."""
    limit = 50
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, quote, author, created_at
        FROM quote_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    history = [
        {
            "id": row[0],
            "quote": row[1],
            "author": row[2] or "Unknown",
            "created_at": row[3],
        }
        for row in rows
    ]
    return jsonify({"history": history})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

