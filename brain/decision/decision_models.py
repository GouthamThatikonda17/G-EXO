"""
=========================================================
Project G-EXO
Decision Models
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# =====================================================
# DECISION PRIORITY
# =====================================================

class DecisionPriority(str, Enum):

    CRITICAL = "critical"

    HIGH = "high"

    NORMAL = "normal"

    LOW = "low"


# =====================================================
# DECISION STATUS
# =====================================================

class DecisionStatus(str, Enum):

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# =====================================================
# DECISION RESULT
# =====================================================

@dataclass
class DecisionResult:

    success: bool

    skill: str | None = None

    action: str | None = None

    reason: str = ""

    confidence: float = 1.0

    priority: DecisionPriority = DecisionPriority.NORMAL

    status: DecisionStatus = DecisionStatus.COMPLETED

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================
# DECISION REQUEST
# =====================================================

@dataclass
class DecisionRequest:

    user_input: str

    intent: str

    source: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )