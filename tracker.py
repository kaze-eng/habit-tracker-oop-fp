# tracker.py

from habit_tracker.db import get_connection
from habit_tracker.models import Habit
from datetime import datetime


class HabitTracker:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def add_habit(self, habit: Habit):
        data = habit.to_dict()
        self.cursor.execute("""
            INSERT INTO habits (habit_name, habit_description, habit_frequency, start_date)
            VALUES (?, ?, ?, ?)
        """, (data["habit_name"], data["habit_description"], data["habit_frequency"], data["start_date"]))
        self.conn.commit()

    def list_habits(self):
        self.cursor.execute("SELECT * FROM habits")
        return self.cursor.fetchall()

    def find_habit(self, habit_id):
        self.cursor.execute("SELECT * FROM habits WHERE habit_id = ?", (habit_id,))
        return self.cursor.fetchone()

    def mark_complete(self, habit_id):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            INSERT INTO habit_progress (habit_id, completion_date)
            VALUES (?, ?)
        """, (habit_id, today))
        self.conn.commit()
