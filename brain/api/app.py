# brain/api/app.py
"""
=========================================================
Project G-EXO FastAPI Application
Version : 2.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.notes import router as notes_router
from api.routes.memory import router as memory_router
from api.routes.assistant import router as assistant_router
from api.routes.voice import router as voice_router

from runtime.application import Application
from voice.whisper_engine import WhisperEngine
from voice.text_to_speech import TextToSpeech

app = FastAPI(
    title="G-EXO API",
    version="2.2"
)

# Minimal safe CORS configuration for local/Android interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development; secure in future iterations
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce composition root ownership for the API layer
app_root = Application()
app.state.brain = app_root.brain
app.state.stt = WhisperEngine()
app.state.tts = TextToSpeech()

# Register routes here
app.include_router(assistant_router)
app.include_router(memory_router)
app.include_router(notes_router)
app.include_router(voice_router)

@app.get("/")
def home():
    return {
        "project": "G-EXO",
        "status": "Running",
        "version": "2.2",
        "auth": "Not implemented yet - safe for local network only"
    }