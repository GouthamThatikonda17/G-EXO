# brain/api/routes/assistant.py
"""
=========================================================
Project G-EXO Assistant API Routes
Version : 2.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
import asyncio
from fastapi import APIRouter, Request
from api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request_body: ChatRequest, request: Request):
    brain = request.app.state.brain

    # Execute synchronously off the event loop via worker thread
    response = await asyncio.to_thread(
        brain.process,
        request_body.message,
        source=request_body.source
    )

    face_state = "idle"
    if brain.behavior.get_state():
        face_state = brain.behavior.get_state().value

    emotion = "neutral"
    if brain.emotion_engine.state and brain.emotion_engine.state.categorical:
        emotion = brain.emotion_engine.state.categorical.value

    return ChatResponse(
        success=response.success,
        response=response.message,
        face_state=face_state,
        emotion=emotion
    )