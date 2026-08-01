"""
=========================================================
Project G-EXO
Configuration
Version : 1.1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================================
# DATA DIRECTORY
# =====================================================

DATA_DIR = os.path.join(BASE_DIR, "data")

# =====================================================
# LOG DIRECTORY
# =====================================================

LOG_DIR = os.path.join(BASE_DIR, "logs")

# =====================================================
# FILES
# =====================================================

MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

LOG_FILE = os.path.join(LOG_DIR, "gexo.log")