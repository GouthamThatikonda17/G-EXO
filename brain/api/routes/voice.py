# brain/api/routes/voice.py
"""
=========================================================
Project G-EXO Voice API Routes
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import io
import wave
import asyncio
import numpy as np
from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import Response as FastAPIResponse
from api.schemas.voice import VoiceSpeakRequest, VoiceTranscribeResponse

router = APIRouter(prefix="/api/v1/voice")

SUPPORTED_SAMPLE_RATE = 16000
SUPPORTED_SAMPLE_WIDTH = 2  # 16-bit signed PCM

@router.post("/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe_audio(request: Request, file: UploadFile = File(...)):
    stt_engine = request.app.state.stt
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio payload provided.")

    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()

            if sample_width != SUPPORTED_SAMPLE_WIDTH:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported audio encoding: expected 16-bit PCM, got {sample_width * 8}-bit."
                )

            if framerate != SUPPORTED_SAMPLE_RATE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported sample rate: expected {SUPPORTED_SAMPLE_RATE} Hz, got {framerate} Hz."
                )

            if channels not in (1, 2):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported channel count: expected 1 (mono) or 2 (stereo), got {channels}."
                )

            raw_frames = wf.readframes(n_frames)
            expected_bytes = n_frames * channels * sample_width
            if len(raw_frames) != expected_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Corrupt or truncated audio: expected {expected_bytes} bytes, got {len(raw_frames)}."
                )
    except wave.Error as e:
        raise HTTPException(status_code=400, detail=f"Malformed or invalid WAV container: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode audio payload: {str(e)}")

    audio_array = np.frombuffer(raw_frames, dtype=np.int16).astype(np.float32) / 32768.0

    if channels > 1:
        audio_array = audio_array.reshape(-1, channels).mean(axis=1)

    try:
        text = await asyncio.to_thread(stt_engine.transcribe, audio_array)
        return VoiceTranscribeResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT processing error: {str(e)}")

@router.post("/synthesize")
async def synthesize_audio(request_body: VoiceSpeakRequest, request: Request):
    tts_engine = request.app.state.tts
    try:
        wav_bytes = await asyncio.to_thread(tts_engine.synthesize_bytes, request_body.text)
        return FastAPIResponse(content=wav_bytes, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis error: {str(e)}")