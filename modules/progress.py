import sqlite3
from config.settings import DB_PATH

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
