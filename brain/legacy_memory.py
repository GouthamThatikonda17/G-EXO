"""
=========================================================
Project G-EXO Memory Storage Module
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os
from config import MEMORY_FILE
from tools.models import ToolResult

def _ensure_memory_file():
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as file:
            json.dump({}, file, indent=4)

def load_memory():
    _ensure_memory_file()
    with open(MEMORY_FILE, "r") as file:
        return json.load(file)

def save_memory(memory):
    _ensure_memory_file()
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def remember(key, value) -> ToolResult:
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return ToolResult(
        success=True,
        message=f"I'll remember that your {key.replace('_', ' ')} is {value}."
    )

def recall(key) -> ToolResult:
    memory = load_memory()
    value = memory.get(key)
    if value is not None:
        return ToolResult(
            success=True,
            message=f"Your {key.replace('_', ' ')} is {value}.",
            data=value
        )
    return ToolResult(
        success=False,
        message=f"I don't have a memory of your {key.replace('_', ' ')}."
    )

def forget(key) -> ToolResult:
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)
        return ToolResult(
            success=True,
            message=f"I have forgotten your {key.replace('_', ' ')}."
        )
    return ToolResult(
        success=False,
        message=f"I don't have a memory of your {key.replace('_', ' ')}."
    )

def show_memory() -> ToolResult:
    memory = load_memory()
    if not memory:
        return ToolResult(success=True, message="You have no stored memories.", data={})

    msg = "Your memories:\n" + "\n".join(f"  {k.replace('_', ' ')}: {v}" for k, v in memory.items())
    return ToolResult(success=True, message=msg, data=memory)
