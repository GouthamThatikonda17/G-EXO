# Project G-EXO: Master Implementation Roadmap (Version 1.4)

## 1. Document Authority
This document is the absolute source of truth for the engineering state and implementation roadmap of Project G-EXO. It governs all architectural decisions, subsystem tracking, and sprint planning. No architectural shifts, subsystem replacements, or deviations from the phased implementation may occur without updating this document.

## 2. Executive Summary
This document serves as the official, living roadmap for Project G-EXO. It outlines the current state of the codebase, identifies technical debt, and establishes a strict, phased approach to reaching production quality. The backend contains a structured execution pipeline with planner JSON extraction, validation, retry/error handling, deterministic tool execution, and standardized result handling.

## 3. AI Engineering Rules
All automated and AI-assisted engineering tasks must strictly adhere to the following rules:
*   If a subsystem already exists, the first task is to improve it.
*   Do not rewrite a subsystem unless the current implementation fundamentally cannot satisfy project requirements.
*   Prefer extending existing code over replacing it.
*   Inspect every dependency before modifying a file.
*   Do not invent APIs, methods, or imports.
*   The repository is the absolute source of truth.

## 4. Definition of Done
A task or sprint is considered "Done" when:
*   The code satisfies the project requirements and architectural standards.
*   All existing dependencies have been inspected and remain unbroken.
*   The implementation extends existing systems where possible.
*   Complete, fully functional replacement files are provided.
*   No undocumented technical debt is introduced.

## 5. Sprint Authority
Sprints are strictly scoped. Code modifications must remain absolutely confined to the approved subsystem files for the current sprint. Entering or modifying subsystems outside the active sprint boundaries without explicit Lead Engineer approval is prohibited.

## 6. Engineering Status Legend
*   **Implemented**: The code is written, structurally present in the repository, and functionally self-contained.
*   **Integrated**: The subsystem successfully communicates and coordinates with its required upstream and downstream dependencies.
*   **Production Ready**: The subsystem is fully tested, optimized, handles edge cases safely, and is ready for deployment.

## 7. Repository Health
Overall, the repository maintains a clear, decoupled architecture. The Core Request Pipeline is runtime-verified and heavily stabilized, structuring tool execution predictably. Remaining work focuses on the internal state and personality engines before progressing to mobile and physical hardware integration.

## 8. Current Entry Point
Project G-EXO operates with a decoupled architecture, resulting in dual entry points:
*   **Backend (Brain)**: `brain/main.py` initializes the core dispatchers and CLI (Development/Testing interface).
*   **Frontend (Desktop)**: `desktop/app.py` initializes the PyQt6 application (Development/Testing interface).

## 9. Runtime Flow
The current execution paths and their connection statuses:

### Currently Implemented Architecture Pipeline
1.  **User Input**
2.  **Intent/Command Routing** (`IntentRouter` keyword matching)
3.  **Dispatcher** (Routes to proper handler)
4.  **Planner** (`AIPlanner` with structured JSON planning, extraction, validation, and retries)
5.  **Executor** (`AIExecutor` unpacks parameters)
6.  **Tool Registry** (`ToolRegistry` cross-references available logic)
7.  **Deterministic Tool** (Python tool execution)
8.  **Persistent Storage / External Action** (`data/*.json` updates or system calls)
9.  **ToolResult** (Returns standardized success, message, data)
10. **ResponseBuilder** (Formats payload)
11. **User Response**

### Voice Pipeline
1.  **Audio Capture**: Handled continuously by `brain/voice/recorder.py` and PortAudio via `brain/wakeword/listener.py`.
2.  **Wake Word Detection**: Processed by `brain/wakeword/detector.py`.
3.  **Runtime Orchestration**: Handoff to `brain/runtime/voice_runtime.py`.
4.  **Speech-to-Text (STT)**: Executed by `brain/voice/speech_to_text.py`.
5.  **Backend Processing**: Routed to the Brain (`assistant.py`) for processing.
6.  **Text-to-Speech (TTS)**: Synthesized by `brain/voice/text_to_speech.py`.

## 10. Currently Implemented Foundation
*   **Memory**
*   **Notes**
*   **Tasks**
*   **Reminders**
*   **File operations**
*   **Application operations**
*   **Intent routing**
*   **AI planning** (Structured JSON planning with JSON extraction, validation, retry/error handling, and tool-registry validation.)
*   **Tool registry**
*   **Tool execution**
*   **Response handling**
*   **CLI development interface**

## 11. Next Brain Architecture (Planned Progression)
1. **Emotion State Engine** *(Current Active Sprint)*
2. **Personality Engine**
3. **Decision Engine**
4. **Expression Engine**
5. **Voice Command Integration**
6. **Mobile / Robotic Integration**
7. **Physical Embodiment**

## 12. Sprint History

### Sprint: Command/Tool Stabilization
**Status:** Completed
**Result:** The pipeline was rigorously enforced to execute tools deterministically. Integrated `ToolResult` across all legacy systems (memory, tasks, notes, reminders). Solidified the `AIPlanner` with robust balanced-brace parsing, strict Registry validation, and `PlannerError` fallback decoupling.

### Sprint: Emotion State Engine
**Status:** READY TO BEGIN
**Purpose:** Create a controlled internal emotional state representation owned by G-EXO. It is PLANNED, not implemented. The LLM must not own persistent emotional state. Future Personality, Decision, Expression and hardware systems must consume explicit G-EXO state/interfaces.