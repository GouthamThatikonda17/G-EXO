"""
=========================================================
Project G-EXO
Reminder Storage Module
Version : 1.3
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os

from config import REMINDERS_FILE


def _ensure_file():

    os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)

    if not os.path.exists(REMINDERS_FILE):

        with open(REMINDERS_FILE, "w") as file:

            json.dump([], file, indent=4)


def load_reminders():

    _ensure_file()

    with open(REMINDERS_FILE, "r") as file:

        return json.load(file)


def save_reminders(reminders):

    _ensure_file()

    with open(REMINDERS_FILE, "w") as file:

        json.dump(reminders, file, indent=4)


def add_reminder(date, time, message):

    reminders = load_reminders()

    reminders.append(
        {
            "id": len(reminders) + 1,
            "date": date,
            "time": time,
            "message": message,
        }
    )

    save_reminders(reminders)


def get_reminders():

    return load_reminders()


def delete_reminder(reminder_id):

    reminders = load_reminders()

    for reminder in reminders:

        if reminder["id"] == reminder_id:

            reminders.remove(reminder)

            save_reminders(reminders)

            return True

    return False


def clear_reminders():

    save_reminders([])