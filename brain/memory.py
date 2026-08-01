"""
=========================================================
Project G-EXO
Memory Storage Module
Version : 1.1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os

from config import MEMORY_FILE


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


def remember(key, value):

    memory = load_memory()

    memory[key] = value

    save_memory(memory)


def recall(key):

    memory = load_memory()

    return memory.get(key)


def forget(key):

    memory = load_memory()

    if key in memory:

        del memory[key]

        save_memory(memory)

        return True

    return False


def show_memory():

    return load_memory()