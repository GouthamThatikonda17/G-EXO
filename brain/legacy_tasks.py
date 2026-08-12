"""
=========================================================
Project G-EXO Tasks Storage Module
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os
from datetime import datetime
from config import TASKS_FILE
from tools.models import ToolResult

def _ensure_tasks_file():
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file, indent=4)

def load_tasks():
    _ensure_tasks_file()
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    _ensure_tasks_file()
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(task) -> ToolResult:
    tasks = load_tasks()

    # Safe ID generation avoiding duplicates
    next_id = max((t.get("id", 0) for t in tasks if isinstance(t.get("id"), int)), default=0) + 1

    new_task = {
        "id": next_id,
        "task": task,
        "status": "Pending",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return ToolResult(success=True, message=f"Task added: {task}")

def get_tasks() -> ToolResult:
    tasks = load_tasks()
    if not tasks:
        return ToolResult(success=True, message="You have no tasks.", data=[])

    msg = "Your tasks:\n" + "\n".join(f"  {t['id']}. [{t['status']}] {t['task']}" for t in tasks)
    return ToolResult(success=True, message=msg, data=tasks)

def complete_task(task_id) -> ToolResult:
    tasks = load_tasks()
    try:
        tid = int(task_id)
        for task in tasks:
            if task.get("id") == tid:
                task["status"] = "Completed"
                save_tasks(tasks)
                return ToolResult(success=True, message=f"Task {tid} marked as completed.")
        return ToolResult(success=False, message=f"Task {task_id} not found.")
    except (ValueError, TypeError):
        return ToolResult(success=False, message="Invalid task ID.")

def delete_task(task_id) -> ToolResult:
    tasks = load_tasks()
    try:
        tid = int(task_id)
        for task in tasks:
            if task.get("id") == tid:
                tasks.remove(task)
                save_tasks(tasks)
                return ToolResult(success=True, message=f"Task {tid} deleted.")
        return ToolResult(success=False, message=f"Task {task_id} not found.")
    except (ValueError, TypeError):
        return ToolResult(success=False, message="Invalid task ID.")

def clear_tasks() -> ToolResult:
    save_tasks([])
    return ToolResult(success=True, message="All tasks cleared.")
