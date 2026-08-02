"""
=========================================================
Project G-EXO
Request Model
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Request:

    message: str

    source: str = "desktop"

    user: str = "default"

    session_id: str = "default"

    timestamp: datetime = field(default_factory=datetime.now)