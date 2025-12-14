from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("iot.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/data", methods=["POST"])
def receive_data():
    d = request.get_json()

    conn = sqlite3.connect("iot.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO data VALUES (NULL, ?, ?, ?)",
        (d["temperature"], d["humidity"], datetime.now())
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
