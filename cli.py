# cli.py

import typer
from models import Habit
from tracker import HabitTracker
from habit_tracker.analystics import get_current_streak, get_longest_streak, get_habits_by_frequency, get_most_skipped_habit

app = typer.Typer()
tracker = HabitTracker()

@app.command()
def hello():
    """Simple test command to verify CLI is working."""
    typer.echo("Hello from your Habit Tracker CLI!")

@app.command()
def test_habit():
    habit = Habit(name="Read Book", description="Read 10 pages", frequency="daily")
    typer.echo(habit)
    typer.echo(habit.to_dict())

@app.command()
def add_habit(
    name: str = typer.Option(..., help="Name of the habit"),
    description: str = typer.Option("", help="Short description"),
    frequency: str = typer.Option(..., help="daily or weekly")
):
    """Add a new habit to the tracker."""
    habit = Habit(name=name, description=description, frequency=frequency)
    tracker.add_habit(habit)
    typer.echo(f"✅ Habit '{name}' added successfully!")

@app.command()
def list_habits():
    """List all saved habits."""
    habits = tracker.list_habits()
    if not habits:
        typer.echo("No habits found.")
        return
    for habit in habits:
        typer.echo(f"{habit[0]}. {habit[1]} ({habit[3]}) - {habit[2]}")

@app.command()
def mark_complete(habit_id: int):
    """Mark a habit as complete for today."""
    habit = tracker.find_habit(habit_id)
    if habit:
        tracker.mark_complete(habit_id)
        typer.echo(f"✅ Marked habit {habit[1]} as complete for today.")
    else:
        typer.echo("❌ Habit not found.")

@app.command()
def current_streak(habit_id: int, frequency: str = "daily"):
    """Show the current active streak for a habit."""
    streak = get_current_streak(habit_id, frequency)
    if streak == 0:
        typer.echo(f"⚠️ No active {frequency} streak for habit {habit_id}.")
    else:
        typer.echo(f"🔥 Current {frequency} streak for habit {habit_id}: {streak}")


@app.command()
def longest_streak(habit_id: int, frequency: str = "daily"):
    """Show the longest historical streak for a habit."""
    streak = get_longest_streak(habit_id, frequency)
    if streak == 0:
        typer.echo(f"⚠️ No streaks found for habit {habit_id}.")
    else:
        typer.echo(f"🏆 Longest {frequency} streak for habit {habit_id}: {streak}")


@app.command()
def list_by_frequency(frequency: str = "daily"):
    """List all habits with a specific frequency."""
    habits = get_habits_by_frequency(frequency)
    if not habits:
        typer.echo(f"⚠️ No {frequency} habits found.")
        return
    typer.echo(f"📋 {frequency.capitalize()} habits:")
    for habit in habits:
        typer.echo(f"{habit[0]}. {habit[1]} - {habit[2]}")


@app.command()
def most_skipped():
    """Show the habit with the worst completion rate."""
    habit, ratio = get_most_skipped_habit()
    if habit:
        typer.echo(f"🚨 Most skipped habit: {habit[1]} ({habit[3]})")
        typer.echo(f"📉 Completion rate: {round(ratio * 100)}%")
    else:
        typer.echo("✅ No habits found or tracked yet.")
