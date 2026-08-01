"""
=========================================================
Project G-EXO
Notes API
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from fastapi import APIRouter

from notes import add_note, get_notes, delete_note
from api.schemas.notes import NoteCreate, NoteResponse

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
def create_note(request: NoteCreate):

    add_note(request.text)

    return NoteResponse(
        success=True,
        message="Note added successfully."
    )
@router.get("/notes")
def read_notes():

    return get_notes()
@router.delete("/notes/{index}", response_model=NoteResponse)
def remove_note(index: int):

    success = delete_note(index)

    if success:

        return NoteResponse(
            success=True,
            message="Note deleted successfully."
        )

    return NoteResponse(
        success=False,
        message="Note not found."
    )