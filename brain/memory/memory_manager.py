# brain/memory/memory_manager.py
"""
=========================================================
Project G-EXO Memory Manager
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from memory.working_memory import WorkingMemory
from memory.short_memory import ShortMemory
from memory.long_memory import LongMemory
from memory.models import MemorySnapshot

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
    # SNAPSHOT
    # =====================================================
    def get_snapshot(self) -> MemorySnapshot:
        """
        Returns a read-only transport snapshot of current memories.
        Safely copies internal mutable collections into immutable tuples.
        """
        return MemorySnapshot(
            working=tuple(self.working.get_all()),
            short=tuple(self.short.get_all()),
            long=tuple(self.long.get_all()),
        )

    # =====================================================
    # CLEAR ALL
    # =====================================================
    def clear(self):
        self.working.clear()
        self.short.clear()
        self.long.clear()