"""
=========================================================
Project G-EXO Reminder Storage Module
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os
import shutil
from config import REMINDERS_FILE
from logger import log

def _ensure_file():
    os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
    if not os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "w") as file:
            json.dump([], file, indent=4)

def _repair_duplicate_ids(reminders):
    """
    Safely resolves historical duplicate/malformed IDs.
    Creates a backup, assigns new unique integer IDs to collisions,
    and leaves valid storage untouched.
    """
    if not isinstance(reminders, list):
        log("[Reminders] Storage is not a valid list. Resetting to empty.", "WARNING")
        return []

    seen_ids = set()
    needs_repair = False
    max_id = 0

    # Pass 1: Detect corruption
    for r in reminders:
        rid = r.get("id")
        if not isinstance(rid, int) or rid in seen_ids:
            needs_repair = True
        else:
            seen_ids.add(rid)
            if rid > max_id:
                max_id = rid

    # Pass 2: Repair safely
    if needs_repair:
        backup_file = f"{REMINDERS_FILE}.bak"
        try:
            shutil.copy2(REMINDERS_FILE, backup_file)
            log(f"[Reminders] Storage corruption detected. Backup created at {backup_file}", "WARNING")
        except Exception as e:
            log(f"[Reminders] Could not create backup: {e}", "ERROR")

        seen_ids.clear()
        for r in reminders:
            rid = r.get("id")
            if not isinstance(rid, int) or rid in seen_ids:
                max_id += 1
                r["id"] = max_id
            seen_ids.add(r["id"])

        # Save the repaired list
        _ensure_file()
        with open(REMINDERS_FILE, "w") as file:
            json.dump(reminders, file, indent=4)
        log("[Reminders] Storage repaired and saved successfully.", "INFO")

    return reminders

def load_reminders():
    _ensure_file()
    try:
        with open(REMINDERS_FILE, "r") as file:
            reminders = json.load(file)
    except (json.JSONDecodeError, ValueError):
        log("[Reminders] Storage file corrupted. Resetting.", "WARNING")
        reminders = []
        save_reminders(reminders)
        return reminders

    return _repair_duplicate_ids(reminders)

def save_reminders(reminders):
    _ensure_file()
    with open(REMINDERS_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def add_reminder(date, time, message):
    reminders = load_reminders()

    # Safe ID generation resistant to list shrinking
    next_id = max((r.get("id", 0) for r in reminders if isinstance(r.get("id"), int)), default=0) + 1

    reminders.append(
        {
            "id": next_id,
            "date": date,
            "time": time,
            "message": message,
            "status": "Pending"
        }
    )
    save_reminders(reminders)

def get_reminders():
    return load_reminders()

def complete_reminder(reminder_id):
    reminders = load_reminders()
    try:
        rid = int(reminder_id)
    except (ValueError, TypeError):
        return False

    for reminder in reminders:
        if reminder.get("id") == rid:
            reminder["status"] = "Completed"
            save_reminders(reminders)
            return True
    return False

def delete_reminder(reminder_id):
    reminders = load_reminders()
    try:
        rid = int(reminder_id)
    except (ValueError, TypeError):
        return False

    for reminder in reminders:
        if reminder.get("id") == rid:
            reminders.remove(reminder)
            save_reminders(reminders)
            return True
    return False

def clear_reminders():
    save_reminders([])
