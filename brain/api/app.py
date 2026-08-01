"""
=========================================================
Project G-EXO
FastAPI Application
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from api.routes.notes import router as notes_router
from api.routes.memory import router as memory_router
from api.routes.memory import router as memory_router
from api.routes.assistant import router as assistant_router
from fastapi import FastAPI

app = FastAPI(
    title="G-EXO API",
    version="2.1"
)
# Register routes here
app.include_router(assistant_router)
app.include_router(memory_router)
app.include_router(notes_router)


@app.get("/")
def home():

    return {
        "project": "G-EXO",
        "status": "Running",
        "version": "2.1"
    }
