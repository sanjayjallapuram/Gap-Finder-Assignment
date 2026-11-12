import sqlite3
from pathlib import Path
from datetime import datetime
from config.settings import DB_PATH


# =========================================================
# 2. DATABASE
# =========================================================

def initialize_database():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_date TEXT,
            topic TEXT,
            score REAL,
            total_questions INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_attempt(results):

    conn = sqlite3.connect(DB_PATH)

    for topic, data in results.items():

        conn.execute("""
            INSERT INTO attempts
            (attempt_date, topic, score, total_questions)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            topic,
            data["score"],
            data["total"]
        ))

    conn.commit()
    conn.close()


def show_progress():

    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute("""
        SELECT topic, AVG(score), COUNT(*)
        FROM attempts
        GROUP BY topic
        ORDER BY topic
    """).fetchall()

    conn.close()

    print("\n========== LEARNING PROGRESS ==========")

    if not rows:
        print("No quiz attempts found.")
        return

    for topic, score, attempts in rows:

        print(
            f"{topic}: {score:.1f}% "
            f"| Attempts: {attempts}"
        )
