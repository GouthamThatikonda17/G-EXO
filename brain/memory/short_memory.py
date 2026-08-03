"""
=========================================================
Project G-EXO
Short Memory
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from datetime import datetime, timedelta

from memory.models import Memory


class ShortMemory:
    """
    Stores memories that remain relevant
    for a limited period of time.

    Examples:
        - Current projects
        - Recent conversations
        - Active reminders
        - This week's goals

    Future versions may automatically
    promote important memories to
    Long Memory.
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
    # CLEANUP
    # =====================================================

    def cleanup(self, days: int = 30) -> None:

        cutoff = datetime.utcnow() - timedelta(days=days)

        expired = []

        for memory in self._memories.values():

            if memory.last_accessed < cutoff:

                expired.append(memory.id)

        for memory_id in expired:

            del self._memories[memory_id]

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