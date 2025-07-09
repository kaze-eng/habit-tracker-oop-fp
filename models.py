# models.py

from datetime import datetime

class Habit:
    def __init__(self, name: str, description: str, frequency: str, start_date: str = None):
        self.name = name
        self.description = description
        self.frequency = frequency.lower()  # daily or weekly
        self.start_date = start_date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "habit_name": self.name,
            "habit_description": self.description,
            "habit_frequency": self.frequency,
            "start_date": self.start_date
        }

    def __str__(self):
        return f"[{self.name}] ({self.frequency}) - {self.description} | Started on {self.start_date}"
