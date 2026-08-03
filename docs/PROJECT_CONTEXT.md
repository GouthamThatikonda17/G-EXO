# Frozen Decisions

- GEXOBrain is the only Brain entry point.
- Brain never depends on UI.
- VoiceRuntime is the orchestrator.
- SpeechToText owns Recorder + VAD + WhisperEngine.
- WhisperEngine is the only module allowed to import faster-whisper.
- TextToSpeech is the only module allowed to import Piper.
- WakeWordDetector is the only module allowed to import OpenWakeWord.
- Face Engine V2 is frozen.# Current Sprint

Sprint:
Current Goal:
Completed:
Blocked:
Next File:

# =========================================================
# PROJECT G-EXO
# MASTER PROJECT CONTEXT
# Version : 1.0
# Developer : Thatikonda Goutham Teja
# =========================================================

# PROJECT NAME

G-EXO

---

# DEVELOPER

Thatikonda Goutham Teja

---

# PROJECT TYPE

Artificial Intelligence Operating System

NOT a chatbot.

NOT a desktop application.

NOT an MVP.

NOT a college project.

G-EXO is intended to become a long-term intelligent operating system capable of running on multiple platforms including desktop, mobile devices, and a future physical robot.

This repository will evolve over several years.

Every architectural decision must prioritize maintainability, portability, scalability, and production quality over short-term convenience.

---

# LONG TERM VISION

The long-term vision of G-EXO is to create an intelligent companion similar to:

• Jarvis
• Friday
• Baymax
• Her

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
- Control desktop
- Control mobile
- Control smart devices
- Execute voice commands
- Automate applications

Example:

"Send WhatsApp message to Mom saying I'll be home in ten minutes."

G-EXO performs the task.

No manual interaction required.

---

# TARGET PLATFORMS

Phase 1

Windows Desktop

Phase 2

Android

Phase 3

Linux

Phase 4

Robot

Future

Web Dashboard

Cloud Synchronization

Smart Home

---

# PRIMARY LANGUAGE

Python

Python remains the source of truth.

Other languages are allowed only when technically justified.

Examples:

Kotlin

Android

Swift

iOS

Rust

High-performance native modules

C++

Hardware interfaces

JavaScript / TypeScript

Future Web UI

The Brain always remains language independent.

---

# CURRENT TECHNOLOGY STACK

Python 3.11.9

GUI

PySide6

LLM

Google Gemini

Speech Recognition

Faster-Whisper

Speech Synthesis

Piper

Wake Word

OpenWakeWord

Memory

SQLite

Desktop API

FastAPI

Vision

OpenCV

YOLO

Future

Face Recognition

Object Detection

Gesture Recognition

---

# PROJECT ARCHITECTURE

Desktop

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

AI

↓

Emotion

↓

Face Engine

↓

Text To Speech

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

Desktop depends on Brain.

Brain never depends on Desktop.

Robot depends on Brain.

Android depends on Brain.

API depends on Brain.

Everything communicates through the Brain.

The Brain never imports UI code.

---

# CURRENT PROJECT STATUS

Completed

✓ Desktop Foundation

✓ Brain

✓ Dispatcher

✓ Request

✓ Response

✓ Intent Routing

✓ Behavior Engine

✓ Face Engine V2

✓ Gemini Integration

✓ Piper Integration

✓ Faster Whisper Integration

✓ Wake Word Foundation

Ongoing

Speech Runtime

Future

Memory Engine

Vision Engine

Robot Runtime

Automation Engine

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

Do not redesign unless explicitly requested.

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

Gemini

↓

Response

↓

Piper

↓

Idle

---

# MEMORY GOALS

Memory is not simple conversation history.

Memory eventually contains:

People

Faces

Voiceprints

Relationships

Preferences

Habits

Locations

Calendar

Tasks

Notes

Conversations

Robot state

Home devices

SQLite is the starting point.

Architecture must allow future migration.

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

# CURRENT DEVELOPMENT WORKFLOW

One sprint.

One subsystem.

One completed implementation.

Commit.

Review.

Next sprint.

---

# CURRENT SPRINT

Subsystem

Speech Runtime

Files

- whisper_engine.py
- recorder.py
- vad.py
- speech_to_text.py

Goal

Production-quality implementation.

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