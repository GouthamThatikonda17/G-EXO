"""
=========================================================
Project G-EXO
Working Memory
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from collections import deque

from memory.models import Memory


class WorkingMemory:
    """
    Stores the active conversation memories.

    Working Memory is temporary.
    It only keeps the latest conversation context.

    Future versions may automatically promote
    important memories to Short Memory.
    """

    def __init__(self, capacity: int = 20):

        self.capacity = capacity

        self._memories = deque(maxlen=capacity)

    # =====================================================
    # ADD
    # =====================================================

    def add(self, memory: Memory) -> None:

        self._memories.append(memory)

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(self) -> list[Memory]:

        return list(self._memories)

    # =====================================================
    # GET LAST
    # =====================================================

    def get_last(self) -> Memory | None:

        if not self._memories:

            return None

        return self._memories[-1]

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

        return iter(self._memories)

    # =====================================================
    # LENGTH
    # =====================================================

    def __len__(self):

        return len(self._memories)