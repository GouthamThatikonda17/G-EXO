# brain/memory/models.py
"""
=========================================================
Project G-EXO Memory Models
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# =====================================================
# MEMORY METADATA
# =====================================================
@dataclass
class MemoryMetadata:
    confidence: float = 1.0
    access_count: int = 0
    archived: bool = False
    favorite: bool = False
    custom: dict[str, Any] = field(
        default_factory=dict
    )

# =====================================================
# MEMORY
# =====================================================
@dataclass
class Memory:
    id: str
    type: str
    title: str
    content: str
    importance: int
    source: str
    tags: list[str] = field(
        default_factory=list
    )
    metadata: MemoryMetadata = field(
        default_factory=MemoryMetadata
    )
    created_at: datetime = field(
        default_factory=datetime.utcnow
    )
    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )
    last_accessed: datetime = field(
        default_factory=datetime.utcnow
    )
    expires_at: datetime | None = None

# =====================================================
# MEMORY SEARCH RESULT
# =====================================================
@dataclass
class MemorySearchResult:
    memory: Memory
    score: float
    matched_tags: list[str] = field(
        default_factory=list
    )

# =====================================================
# MEMORY SNAPSHOT
# =====================================================
@dataclass(frozen=True)
class MemorySnapshot:
    """
    Immutable representation of the memory engine state.
    Used exclusively as a transport object to the Decision Engine.
    Exposes data strictly as immutable tuples.
    """
    working: tuple[Memory, ...]
    short: tuple[Memory, ...]
    long: tuple[Memory, ...]