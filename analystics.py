# analytics.py

from datetime import datetime, timedelta
from habit_tracker.db import get_connection

def get_completion_dates(habit_id):
    """Get all completion dates for a habit as datetime.date objects."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT completion_date FROM habit_progress
        WHERE habit_id = ?
        ORDER BY completion_date ASC
    """, (habit_id,))
    rows = cursor.fetchall()
    return [datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows]

def get_longest_streak(habit_id, frequency="daily"):
    """Calculate the longest streak for a habit."""
    dates = get_completion_dates(habit_id)

    if not dates:
        return 0

    streak = 1
    max_streak = 1
    step = timedelta(days=1) if frequency == "daily" else timedelta(weeks=1)

    for i in range(1, len(dates)):
        if dates[i] - dates[i-1] == step:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    return max_streak
def get_current_streak(habit_id, frequency="daily"):
    dates = get_completion_dates(habit_id)
    if not dates:
        return 0

    today = datetime.today().date()
    step = timedelta(days=1) if frequency == "daily" else timedelta(weeks=1)
    streak = 1

    for i in range(len(dates)-1, 0, -1):
        if dates[i] - dates[i-1] == step:
            streak += 1
        else:
            break

    # Final check: is the last completion today or yesterday (for daily)?
    last_done = dates[-1]
    expected = today - step
    if last_done < expected:
        return 0  # streak is broken

    return streak

def get_habits_by_frequency(frequency="daily"):
    """Return a list of all habits with a given frequency."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM habits WHERE habit_frequency = ?
    """, (frequency.lower(),))
    return cursor.fetchall()

def get_most_skipped_habit():
    """Return the habit with the lowest completion ratio."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()

    worst_habit = None
    lowest_ratio = 1.0  # perfect completion is 1.0

    today = datetime.today().date()

    for habit in habits:
        habit_id = habit[0]
        start_date = datetime.strptime(habit[4], "%Y-%m-%d").date()
        frequency = habit[3]

        # How many times it *should* have been done
        if frequency == "daily":
            expected = (today - start_date).days + 1
        elif frequency == "weekly":
            expected = ((today - start_date).days // 7) + 1
        else:
            continue

        # How many times it *was* actually done
        cursor.execute("SELECT COUNT(*) FROM habit_progress WHERE habit_id = ?", (habit_id,))
        actual = cursor.fetchone()[0]

        # Avoid division by 0
        ratio = actual / expected if expected > 0 else 0

        if ratio < lowest_ratio:
            lowest_ratio = ratio
            worst_habit = habit

    return worst_habit, lowest_ratio

