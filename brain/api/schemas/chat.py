# brain/api/schemas/chat.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    source: str = "android"
    session_id: str = "default"

class ChatResponse(BaseModel):
    success: bool = True
    response: str
    face_state: Optional[str] = None
    emotion: Optional[str] = None