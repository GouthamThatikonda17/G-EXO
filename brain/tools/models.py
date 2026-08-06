"""
=========================================================
Project G-EXO Tool Models
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolResult:
    """
    Standardized return contract for the Tool Layer.
    Ensures ResponseBuilder can format UI messages agnostically.
    """
    success: bool
    message: str
    data: Any = None
    metadata: dict = field(default_factory=dict)