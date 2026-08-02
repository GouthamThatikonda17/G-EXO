"""
=========================================================
Project G-EXO
Configuration
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os

# =====================================================
# PROJECT INFORMATION
# =====================================================

PROJECT_NAME = "G-EXO"

PROJECT_VERSION = "1.0.0"

PROJECT_DEVELOPER = "Thatikonda Goutham Teja"

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# =====================================================
# DIRECTORIES
# =====================================================

DATA_DIR = os.path.join(BASE_DIR, "data")

LOG_DIR = os.path.join(BASE_DIR, "logs")

# =====================================================
# DATA FILES
# =====================================================

MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")

# =====================================================
# LOG FILE
# =====================================================

LOG_FILE = os.path.join(LOG_DIR, "gexo.log")