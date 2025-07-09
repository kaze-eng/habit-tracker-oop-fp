# db.py

import sqlite3
from pathlib import Path

# Path to the local database file
DB_PATH = Path("habits.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create habits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            habit_description TEXT,
            habit_frequency TEXT NOT NULL,  -- 'daily' or 'weekly'
            start_date TEXT NOT NULL
        )
    """)

    # Create habit_progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_progress (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completion_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
        )
    """)

    conn.commit()
    conn.close()
