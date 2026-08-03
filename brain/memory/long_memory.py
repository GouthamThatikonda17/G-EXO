"""
=========================================================
Project G-EXO
Long Memory
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from datetime import datetime

from memory.models import Memory


class LongMemory:
    """
    Stores permanent memories.

    Examples:
        - User profile
        - Family members
        - Birthdays
        - Preferences
        - Long-term goals
        - Important life events
    """

    def __init__(self):

        self._memories: dict[str, Memory] = {}

    # =====================================================
    # ADD
    # =====================================================

    def add(self, memory: Memory) -> None:

        self._memories[memory.id] = memory

    # =====================================================
    # GET
    # =====================================================

    def get(self, memory_id: str) -> Memory | None:

        memory = self._memories.get(memory_id)

        if memory:

            memory.last_accessed = datetime.utcnow()

        return memory

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(self) -> list[Memory]:

        return list(self._memories.values())

    # =====================================================
    # REMOVE
    # =====================================================

    def remove(self, memory_id: str) -> bool:

        if memory_id not in self._memories:

            return False

        del self._memories[memory_id]

        return True

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self) -> None:

        self._memories.clear()

    # =====================================================
    # SIZE
    # =====================================================

    def size(self) -> int:

        return len(self._memories)

    # =====================================================
    # EMPTY
    # =====================================================

    def is_empty(self) -> bool:

        return len(self._memories) == 0

    # =====================================================
    # ITERATOR
    # =====================================================

    def __iter__(self):

        return iter(self._memories.values())

    # =====================================================
    # LENGTH
    # =====================================================

    def __len__(self):

        return len(self._memories)