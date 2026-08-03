"""
=========================================================
Project G-EXO
Memory Manager
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from memory.working_memory import WorkingMemory
from memory.short_memory import ShortMemory
from memory.long_memory import LongMemory


class MemoryManager:
    """
    Central memory controller for G-EXO.

    Responsibilities
    ----------------
    - Manage Working Memory
    - Manage Short Memory
    - Manage Long Memory

    Future Responsibilities
    -----------------------
    - Importance Scoring
    - Memory Promotion
    - Semantic Search
    - Memory Relationships
    """

    def __init__(self):

        self.working = WorkingMemory()

        self.short = ShortMemory()

        self.long = LongMemory()

    # =====================================================
    # WORKING MEMORY
    # =====================================================

    def working_memory(self):

        return self.working

    # =====================================================
    # SHORT MEMORY
    # =====================================================

    def short_memory(self):

        return self.short

    # =====================================================
    # LONG MEMORY
    # =====================================================

    def long_memory(self):

        return self.long

    # =====================================================
    # CLEAR ALL
    # =====================================================

    def clear(self):

        self.working.clear()

        self.short.clear()

        self.long.clear()