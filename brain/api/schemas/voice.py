# brain/api/schemas/voice.py
"""
=========================================================
Project G-EXO Voice API Schemas
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
from pydantic import BaseModel, field_validator
from typing import Optional

class VoiceTranscribeResponse(BaseModel):
    text: str

class VoiceSpeakRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

class VoiceSpeakResponse(BaseModel):
    status: str
    message: Optional[str] = None