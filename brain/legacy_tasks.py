"""
=========================================================
Project G-EXO Tasks Storage Module
Version : 1.2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os
from datetime import datetime
from config import TASKS_FILE

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

def add_task(task):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "task": task,
        "status": "Pending",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)

def get_tasks():
    return load_tasks()

def complete_task(task_id):
    tasks = load_tasks()
    
    # Defense in depth: Sanitize type mapping from LLM planner JSON
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        return False
        
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            save_tasks(tasks)
            return True
    return False

def delete_task(task_id):
    tasks = load_tasks()
    
    # Defense in depth: Sanitize type mapping from LLM planner JSON
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        return False
        
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False

def clear_tasks():
    save_tasks([])