# Frozen Decisions

- GEXOBrain is the only Brain entry point.
- Brain never depends on UI.
- VoiceRuntime is the orchestrator.
- SpeechToText owns Recorder + VAD + WhisperEngine.
- WhisperEngine is the only module allowed to import faster-whisper.
- TextToSpeech is the only module allowed to import Piper.
- WakeWordDetector is the only module allowed to import OpenWakeWord.
- Face Engine V2 is frozen.
- The LLM must not become the source of truth for persistent G-EXO state.
- Tool execution belongs to deterministic G-EXO software.

# Current Sprint

Sprint: Emotion State Engine
Current Goal: Create a controlled internal emotional state representation owned by G-EXO.
Completed: Command and Tool Stabilization
Blocked: None
Next File: 

# =========================================================
# PROJECT G-EXO
# MASTER PROJECT CONTEXT
# Version : 1.3
# Developer : Thatikonda Goutham Teja
# =========================================================

# PROJECT NAME

G-EXO

---

# DEVELOPER

Thatikonda Goutham Teja

---

# PROJECT TYPE

G-EXO is a robotic brain/software platform intended for mobile-integrated operation and eventual physical robotic embodiment. 

NOT a chatbot.
NOT a desktop assistant.
NOT a desktop-first product.
NOT an MVP.
NOT a college project.

The current CLI and Desktop GUI are development and testing interfaces only.

This repository will evolve over several years.
Every architectural decision must prioritize maintainability, portability, scalability, and production quality over short-term convenience.

---

# LONG TERM VISION

The long-term vision of G-EXO is to create an intelligent companion similar to:

- Jarvis
- Friday
- Baymax
- Her

G-EXO should eventually become a robotic companion that can:

- Understand natural conversation
- Remember people
- Learn preferences
- Walk autonomously
- Respond emotionally
- Observe surroundings
- Assist daily life
- Operate completely offline whenever possible
- Use cloud AI only when beneficial

The experience should feel like interacting with a living assistant rather than using software.

---

# ROBOT VISION

The intended final product is a mobile-integrated robotic system, with physical embodiment planned for future phases.

The robot is NOT a traditional robot with an embedded computer.
Instead:
A smartphone becomes the brain.
The robot body becomes the hardware extension.

Phone provides:
- CPU
- GPU
- AI acceleration
- Camera
- Display
- Speakers
- Microphones
- Battery
- Internet
- Bluetooth
- WiFi

Robot body provides:
- Wheels or legs
- Charging dock
- Servo motors
- Distance sensors
- Edge detection
- Optional robotic arm
- LEDs
- Additional batteries

This design dramatically reduces hardware cost while leveraging modern smartphone capabilities.

---

# FINAL USER EXPERIENCE

The user should never feel like they are opening software.
Instead they simply say:
"Hey G-EXO"

G-EXO wakes automatically.
Looks at the user.
Listens.
Understands.
Thinks.
Responds naturally.
Returns to idle.

Eventually it should:
- Follow the user
- Come when called
- Recognize family members
- Recognize guests
- Learn routines
- Remind elderly users to take medicines
- Remember birthdays
- Play music
- Generate music (Suno API in future)
- Capture photos
- Capture memorable moments automatically
- Control mobile
- Control smart devices
- Execute voice commands
- Automate applications

---

# TARGET PLATFORMS

IMPLEMENTED:
- Development/Testing Interfaces (CLI and GUI)

FUTURE:
- Android (Mobile Integration)
- Linux
- Robot (Physical Embodiment)
- Web Dashboard
- Cloud Synchronization
- Smart Home

---

# PRIMARY LANGUAGE

Python

Python remains the source of truth.
Other languages are allowed only when technically justified.

Examples:
Kotlin (Android)
Swift (iOS)
Rust (High-performance native modules)
C++ (Hardware interfaces)
JavaScript / TypeScript (Future Web UI)

The Brain always remains language independent.

---

# CURRENT TECHNOLOGY STACK

Python 3.11.9
PySide6 (Development/Testing Interfaces)
Google Gemini / OpenRouter / Ollama
Faster-Whisper (Speech Recognition)
Piper (Speech Synthesis)
OpenWakeWord (Wake Word)
SQLite (Memory - Planned)
FastAPI (Desktop API)
OpenCV / YOLO (Vision - Future)

---

# PROJECT ARCHITECTURE

## Conceptual/Future Brain Pipeline
Development/Testing Interface
↓
Runtime
↓
Voice Runtime
↓
Wake Word
↓
Speech To Text
↓
Brain
↓
Decision Engine
↓
Memory
↓
Emotion
↓
Face Engine
↓
Text To Speech

## Currently Implemented Pipeline
User Input
↓
Intent/Command Routing
↓
Dispatcher
↓
Planner
↓
Executor
↓
Tool Registry
↓
Deterministic Tool
↓
Persistent Storage / External Action
↓
ToolResult
↓
ResponseBuilder
↓
User Response

---

# BRAIN

Single entry point.
assistant.py

Contains:
class GEXOBrain

Every platform communicates ONLY through GEXOBrain.
Never bypass it.

---

# ARCHITECTURAL PRINCIPLES

1. G-EXO is a robotic brain/software platform.
2. The CLI and Desktop GUI are development and testing interfaces only.
3. The final system is intended to operate through mobile and eventually physical robotic interfaces.
4. External AI/LLM providers are cognitive components used by G-EXO. They are NOT the G-EXO Brain itself.
5. G-EXO owns deterministic application state and execution.
   - The LLM proposes.
   - G-EXO validates.
   - G-EXO executes.
   - G-EXO records the actual result.
6. The LLM must NOT become the source of truth for persistent G-EXO state.
7. Tool execution belongs to deterministic G-EXO software.
8. Future hardware must consume G-EXO decisions/state through explicit interfaces rather than being directly controlled by arbitrary LLM output.

---

# CURRENT PROJECT STATUS

Currently Implemented Foundation:
- Memory
- Notes
- Tasks
- Reminders
- File operations
- Application operations
- Intent routing
- AI planning (Structured JSON planning with JSON extraction, validation, retry/error handling, and tool-registry validation.)
- Tool registry
- Tool execution
- Response handling
- CLI development interface

Ongoing / Next Brain Architecture:
1. Emotion State Engine (Planned)
2. Personality Engine (Planned)
3. Decision Engine (Planned)
4. Expression Engine (Planned)
5. Voice Command Integration (Planned)
6. Mobile / Robotic Integration (Future)
7. Physical Embodiment (Future)

---

# FACE ENGINE

States
Idle
Listening
Thinking
Speaking
Error

Face changes automatically according to Behavior Engine.
Face Engine V2 is considered stable.

---

# SPEECH PIPELINE

Wake Word
↓
Recorder
↓
Voice Activity Detection
↓
Whisper Engine
↓
Brain
↓
Cognitive Component (LLM)
↓
Response
↓
Piper
↓
Idle

---

# ENGINEERING PHILOSOPHY

Every subsystem owns exactly one responsibility.
Every subsystem exposes a minimal API.
No third-party library spreads throughout the project.
Only owner modules import external libraries.

Example:
WhisperEngine imports Faster Whisper.
TextToSpeech imports Piper.
WakeWordDetector imports OpenWakeWord.
GeminiProvider imports Google GenAI.

---

# DEVELOPMENT RULES

Provide complete production-ready implementations.
Never create placeholder implementations.
Never create duplicate classes.
Never redesign architecture without explicit approval.
Never bypass GEXOBrain.
Always preserve portability.
Think long term.

Every implementation should still make sense years later.

---

# CURRENT SPRINT

Subsystem:
Emotion State Engine

Purpose:
Create a controlled internal emotional state representation owned by G-EXO.
It is PLANNED, not implemented.
The emotion state must be deterministic and persistent according to the architecture defined during the sprint.
The LLM must not directly own or arbitrarily overwrite the current emotional state.
Future personality, decision, expression systems, and hardware must be able to consume the emotion state through explicit interfaces.
Future hardware must consume explicit G-EXO state/decisions rather than arbitrary raw LLM output.

---

# GITHUB

GitHub repository is the source of truth.
Every completed sprint is committed.
Architecture documentation remains synchronized with implementation.

---

# IMPORTANT FOR AI ASSISTANTS

Before writing any code:

Understand this document completely.
Respect all architectural decisions.
Do not redesign stable components.
Do not introduce technical debt.
Do not provide shortcuts.
Think like the lead software architect of G-EXO.
Every decision should improve the project's long-term quality.
The objective is not merely to make the code work.
The objective is to build an AI operating system that can evolve into a real robotic companion.