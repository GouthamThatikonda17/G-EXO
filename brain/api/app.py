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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce authoritative composition root ownership
app_root = Application()
app.state.brain = app_root.brain
app.state.stt = WhisperEngine()
app.state.tts = TextToSpeech()

# Register active routes; obsolete memory and notes routes are decoupled
app.include_router(assistant_router)
app.include_router(voice_router)

@app.get("/")
def home():
    return {
        "project": "G-EXO",
        "status": "Running",
        "version": "2.2"
    }