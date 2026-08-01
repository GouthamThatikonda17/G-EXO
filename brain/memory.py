"""
Project G-EXO
Persistent Memory Module v0.3
"""

import json
import os

MEMORY_FILE = "brain/memory.json"


def load_memory():
    """Load memory from JSON file."""

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_memory(memory):
    """Save memory to JSON file."""

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):
    """Store a fact."""

    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    """Retrieve a fact."""

    memory = load_memory()
    return memory.get(key)


def forget(key):
    """Delete a fact."""

    memory = load_memory()

    if key in memory:
        del memory[key]
        save_memory(memory)
        return True

    return False


def show_memory():
    """Return all stored memories."""

    return load_memory()