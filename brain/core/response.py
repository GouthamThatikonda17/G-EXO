"""
=========================================================
Project G-EXO
Response Model
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class Response:

    success: bool = True

    message: str = ""

    data: Any = None

    source: str = "g-exo"

    timestamp: datetime = field(default_factory=datetime.now)