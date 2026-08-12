"""
=========================================================
Project G-EXO Notes Storage Module
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os
from config import NOTES_FILE
from tools.models import ToolResult

def _ensure_notes_file():
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as file:
            json.dump([], file, indent=4)

def load_notes():
    _ensure_notes_file()
    with open(NOTES_FILE, "r") as file:
        return json.load(file)

def save_notes(notes):
    _ensure_notes_file()
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

def add_note(text) -> ToolResult:
    notes = load_notes()
    notes.append(text)
    save_notes(notes)
    return ToolResult(success=True, message=f"Note added: {text}")

def get_notes() -> ToolResult:
    notes = load_notes()
    if not notes:
        return ToolResult(success=True, message="You have no notes.", data=[])

    msg = "Your notes:\n" + "\n".join(f"  {i+1}. {n}" for i, n in enumerate(notes))
    return ToolResult(success=True, message=msg, data=notes)

def delete_note(index) -> ToolResult:
    notes = load_notes()
    try:
        idx = int(index) - 1
        if 0 <= idx < len(notes):
            deleted = notes.pop(idx)
            save_notes(notes)
            return ToolResult(success=True, message=f"Note deleted: {deleted}")
        return ToolResult(success=False, message=f"Note {index} not found.")
    except (ValueError, TypeError):
        return ToolResult(success=False, message="Invalid note index.")

def clear_notes() -> ToolResult:
    save_notes([])
    return ToolResult(success=True, message="All notes cleared.")
