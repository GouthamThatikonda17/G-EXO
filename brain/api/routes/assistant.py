from fastapi import APIRouter

from ai.router import AIRouter
from api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

ai = AIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = ai.chat(request.message)

    return ChatResponse(response=response)