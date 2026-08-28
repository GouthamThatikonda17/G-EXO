# brain/api/routes/assistant.py
from fastapi import APIRouter, Request
from api.schemas.chat import ChatRequest, ChatResponse
import asyncio

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request_body: ChatRequest, request: Request):
    brain = request.app.state.brain

    # Execute off the event loop as brain.process is synchronous and heavy
    response = await asyncio.to_thread(
        brain.process,
        request_body.message,
        source=request_body.source
    )

    # Extract state safely
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
