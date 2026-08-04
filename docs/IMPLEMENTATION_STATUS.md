# docs/IMPLEMENTATION_STATUS.md

# Project G-EXO: Master Implementation Roadmap (Version 1.0)

## 1. Document Authority
This document is the absolute source of truth for the engineering state and implementation roadmap of Project G-EXO. It governs all architectural decisions, subsystem tracking, and sprint planning. No architectural shifts, subsystem replacements, or deviations from the phased implementation may occur without updating this document.

## 2. Executive Summary
This document serves as the official, living roadmap for Project G-EXO. It outlines the current state of the codebase, identifies technical debt, and establishes a strict, phased approach to reaching production quality[cite: 2]. 

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
Overall, the repository maintains a clear, decoupled architecture separating the PyQt6 frontend (`desktop/`) from the FastAPI/Core backend (`brain/`)[cite: 2]. However, repository health is currently impacted by disconnected execution loops between the dispatcher and AI planner, as well as unresolved legacy redundancies that require immediate audit and deprecation[cite: 2].

## 8. Current Entry Point
Project G-EXO operates with a decoupled architecture, resulting in dual entry points:
*   **Backend (Brain)**: `brain/main.py` initializes the FastAPI server, core dispatchers, and background runtimes (Voice, Memory)[cite: 2].
*   **Frontend (Desktop)**: `desktop/app.py` initializes the PyQt6 application, launching the visual engine and connecting to the backend via asynchronous workers[cite: 2].

## 9. Runtime Flow
The current execution paths and their connection statuses:

### Request Pipeline
1.  **User Input**: Captured via `desktop/widgets/message_input.py`[cite: 2].
2.  **Dispatching**: Routed through `brain/api/app.py` -> `brain/core/dispatcher.py` -> `brain/core/handlers/`[cite: 2].
3.  **AI & Processing**: Handoff from `brain/core/handlers/` -> `brain/ai/planner.py` -> `brain/tools/`[cite: 2].
4.  **Response & Action**: Returned via `brain/core/response_builder.py` -> `desktop/workers/chat_worker.py` -> UI/Visuals[cite: 2].
*   **Status**: Implemented structurally, but disconnected. Tool registries and Gemini providers exist, but the execution loop connecting the dispatcher to the planner is not fully wired[cite: 2]. Responses do not yet seamlessly trigger `face_controller.py` state changes[cite: 2].

### Voice Pipeline
1.  **Audio Capture**: Handled by `brain/voice/recorder.py`[cite: 2].
2.  **Wake Word Detection**: Processed via `brain/wakeword/listener.py` and `brain/voice/wake_word.py`[cite: 2].
3.  **Speech-to-Text (STT)**: Executed by `brain/voice/speech_to_text.py` utilizing `brain/voice/whisper_engine.py`[cite: 2].
4.  **Backend Handoff**: Needs routing to `brain/core/dispatcher.py`[cite: 2].
5.  **Text-to-Speech (TTS)**: Synthesized by `brain/voice/text_to_speech.py`[cite: 2].
*   **Status**: Implemented but not fully integrated. STT and TTS engines are coded, but the continuous, thread-safe asynchronous state machine routing audio through the full pipeline is incomplete[cite: 2].

## 10. Current State of Subsystems

| Subsystem | Implemented | Integrated | Production Ready | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop UI & Visuals** | Yes | Partial | No | UI scaffolding and vector face engine exist[cite: 2]. Needs binding to backend state. |
| **API & Schemas** | Yes | Partial | No | FastAPI routes and Pydantic schemas are well-defined[cite: 2]. |
| **AI & Planner** | Partial | No | No | Gemini integration and tool registry exist[cite: 2]. Execution loop needs wiring. |
| **Memory System** | Partial | No | No | Tiered architecture exists[cite: 2]. Requires background consolidation logic. |
| **Voice Runtime** | Yes | No | No | Implemented but not fully integrated. Whisper STT completed; TTS and VAD exist[cite: 2]. |
| **Decision Engine** | No | No | No | Rules and context evaluation require significant expansion[cite: 2]. |
| **Emotion & Personality** | No | No | No | Modules are currently empty stubs[cite: 2]. |
| **Testing Suite** | Partial | No | No | Test files exist as structural stubs only[cite: 2]. |

## 11. Technical Debt to Resolve
*   **[PRIORITY]** Audit, deprecate, then remove if unused the `brain/legacy_*.py` files to enforce the use of `brain/memory/` and `brain/tools/`[cite: 2].
*   Audit ownership, determine why duplicate implementations exist, and consolidate only if architectural responsibilities overlap between `brain/voice/wake_word.py` and `brain/wakeword/`[cite: 2].

## 12. Future Scalability Tasks
*   Migrate JSON storage (`data/*.json`) to a thread-safe local database (e.g., SQLite or a vector database) to support memory scaling and concurrent operations[cite: 2].

## 13. Implementation Phases

### Phase 1: Core Consolidation & Cleanup (Current)
*   **Goal**: Stabilize the foundation by removing duplicate code and finalizing module boundaries.
*   **Tasks**:
    *   Audit, deprecate, then remove if unused legacy memory/task files[cite: 2].
    *   Audit and consolidate the Wake Word pipeline overlapping logic[cite: 2].
    *   Ensure all configuration is loaded via environment variables rather than hardcoded fallbacks[cite: 2].

### Phase 2: Intelligence & Memory Wiring
*   **Goal**: Connect the AI planner to the execution tools and stabilize the memory lifecycle.
*   **Tasks**:
    *   Wire `brain/core/dispatcher.py` to seamlessly pass payloads to `brain/ai/planner.py`[cite: 2].
    *   Extend `brain/memory/memory_manager.py` to handle Working -> Short -> Long term consolidation[cite: 2].

### Phase 3: Runtimes & UI Synchronization
*   **Goal**: Ensure the backend and frontend runtimes communicate safely without blocking threads.
*   **Tasks**:
    *   Extend `desktop/workers/chat_worker.py` to handle bidirectional streaming from the FastAPI layer[cite: 2].
    *   Lock down thread-safety between the Voice Runtime and the Core Dispatcher.

### Phase 4: Emotion, Behavior, and State Generation
*   **Goal**: Bring the robot to life by connecting backend decisions to frontend visuals.
*   **Tasks**:
    *   Implement `brain/emotion/` and `brain/personality/` (extend existing state architectures)[cite: 2].
    *   Wire the Decision Engine to emit state changes to `desktop/visual/engine/face_controller.py`[cite: 2].

### Phase 5: Hardening & Hardware
*   **Goal**: Production readiness and physical robot integration.
*   **Tasks**:
    *   Complete the PyTest suite across all modules.
    *   Implement hardware I/O interfaces per hardware specifications.

## 14. Sprint History

Sprint 1: Speech Runtime

Status: Completed

Verified:
✓ Recorder
✓ Voice Activity Detector
✓ SpeechToText
✓ WhisperEngine
✓ Runtime Tested
✓ End-to-End Speech Pipeline Operational