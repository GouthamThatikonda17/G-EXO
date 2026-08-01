"""
=========================================================
Project G-EXO
Notes API Schemas
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from pydantic import BaseModel


class NoteCreate(BaseModel):
    text: str


class NoteResponse(BaseModel):
    success: bool
    message: str