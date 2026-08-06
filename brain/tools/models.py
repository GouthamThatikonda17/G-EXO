# brain/tools/models.py
"""
=========================================================
Project G-EXO Tool Models
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolResult:
    """
    Standardized return contract for the Tool Layer.
    Migration in progress: Newly implemented tools must return this object.
    Legacy tools will be migrated in future sprints.
    """
    success: bool
    message: str
    data: Any = None
    metadata: dict = field(default_factory=dict)