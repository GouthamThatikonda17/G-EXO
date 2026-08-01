"""
=========================================================
Project G-EXO
Memory API Schemas
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    key: str
    value: str


class MemoryResponse(BaseModel):
    success: bool
    message: str