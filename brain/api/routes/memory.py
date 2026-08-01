from fastapi import APIRouter

from api.schemas.memory import MemoryCreate, MemoryResponse
from memory import remember, show_memory, recall

router = APIRouter()


@router.post("/memory", response_model=MemoryResponse)
def add_memory(request: MemoryCreate):

    remember(request.key, request.value)

    return MemoryResponse(
        success=True,
        message="Memory saved successfully."
    )

@router.get("/memory")
def get_memory():

    return show_memory()
@router.get("/memory/{key}")
def get_memory_by_key(key: str):

    value = recall(key)

    if value is None:

        return {
            "success": False,
            "message": "Memory not found."
        }

    return {
        "key": key,
        "value": value
    }