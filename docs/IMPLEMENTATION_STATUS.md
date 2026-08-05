# Project G-EXO: Master Implementation Roadmap (Version 1.1)

## 1. Document Authority
This document is the absolute source of truth for the engineering state and implementation roadmap of Project G-EXO. It governs all architectural decisions, subsystem tracking, and sprint planning. No architectural shifts, subsystem replacements, or deviations from the phased implementation may occur without updating this document.

## 2. Executive Summary
This document serves as the official, living roadmap for Project G-EXO. It outlines the current state of the codebase, identifies technical debt, and establishes a strict, phased approach to reaching production quality. The backend now features a fully operational Voice Pipeline and a verified Core Request Pipeline, advancing the system toward true multi-modal, thread-safe interaction.

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
Overall, the repository maintains a clear, decoupled architecture separating the PyQt6 frontend (`desktop/`) from the FastAPI/Core backend (`brain/`). The backend execution loops are runtime-verified, and the speech pipeline operates safely on dedicated worker threads without blocking PortAudio callbacks. Minor legacy redundancies require audit and deprecation.

## 8. Current Entry Point
Project G-EXO operates with a decoupled architecture, resulting in dual entry points:
*   **Backend (Brain)**: `brain/main.py` initializes the FastAPI server, core dispatchers, and background runtimes (Voice, Memory).
*   **Frontend (Desktop)**: `desktop/app.py` initializes the PyQt6 application, launching the visual engine and connecting to the backend via asynchronous workers.

## 9. Runtime Flow
The current execution paths and their connection statuses:

### Request Pipeline
1.  **User Input**: Captured via `desktop/widgets/message_input.py`.
2.  **Dispatching**: Routed through `brain/api/app.py` -> `brain/core/dispatcher.py` -> `brain/core/handlers/`.
3.  **AI & Processing**: Handoff from `brain/core/handlers/` -> `brain/ai/planner.py` -> `brain/tools/`.
4.  **Response & Action**: Returned via `brain/core/response_builder.py` -> `desktop/workers/chat_worker.py` -> UI/Visuals.
*   **Status**: Fully implemented and runtime verified. The execution loop seamlessly connects the dispatcher to the AI planner and tool executor. Responses trigger appropriate downstream behavior, though UI visual binding remains partial.

### Voice Pipeline
1.  **Audio Capture**: Handled continuously by `brain/voice/recorder.py` and PortAudio via `brain/wakeword/listener.py`.
2.  **Wake Word Detection**: Processed by `brain/wakeword/detector.py`.
3.  **Runtime Orchestration**: Handoff to `brain/runtime/voice_runtime.py`, which spawns a dedicated worker thread and stops the wake-word listener safely. Thread-safe interaction locking prevents concurrent wake events.
4.  **Speech-to-Text (STT)**: Executed by `brain/voice/speech_to_text.py` utilizing `brain/voice/vad.py` and `brain/voice/whisper_engine.py`.
5.  **Backend Processing**: Routed to the Brain (`assistant.py`) for processing.
6.  **Text-to-Speech (TTS)**: Synthesized by `brain/voice/text_to_speech.py`.
7.  **Completion**: Wake-word listener restarts safely.
*   **Status**: Fully operational and runtime verified. The listener lifecycle is robust, avoiding PortAudio deadlocks, and the end-to-end system runs smoothly via the orchestrating worker thread.

## 10. Current State of Subsystems

| Subsystem | Implemented | Integrated | Production Ready | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop UI & Visuals** | Yes | Partial | No | UI scaffolding and vector face engine exist. Needs binding to backend state. |
| **API & Schemas** | Yes | Partial | No | FastAPI routes and Pydantic schemas are well-defined. |
| **AI & Planner** | Yes | Yes | No | Gemini integration and tool registry exist. Execution loop is wired and runtime verified. |
| **Memory System** | Partial | No | No | Tiered architecture exists. Requires background consolidation logic. |
| **Voice Runtime** | Yes | Yes | No | Fully operational. Uses background thread, thread-safe locking, and stable listener lifecycles. |
| **Decision Engine** | No | No | No | Rules and context evaluation require significant expansion. |
| **Emotion & Personality** | No | No | No | Modules are currently empty stubs. |
| **Testing Suite** | Partial | No | No | Test files exist as structural stubs only. |

## 11. Technical Debt to Resolve
* **[PRIORITY]** Audit, deprecate, then remove if unused the `brain/legacy_*.py` files to enforce the use of `brain/memory/` and `brain/tools/`.
* Audit ownership, determine why duplicate implementations exist, and consolidate only if architectural responsibilities overlap between `brain/voice/wake_word.py` and `brain/wakeword/`.
* Improve Text-to-Speech Unicode handling.
* Prevent wake-word self-triggering during speaker playback.
* Replace remaining runtime print statements with structured logging.
* Expand automated runtime integration tests.

## 12. Future Scalability Tasks
*   Migrate JSON storage (`data/*.json`) to a thread-safe local database (e.g., SQLite or a vector database) to support memory scaling and concurrent operations.

## 13. Implementation Phases

### Phase 1: Core Consolidation & Cleanup (Completed)
*   **Goal**: Stabilize the foundation by removing duplicate code and finalizing module boundaries.
*   **Tasks**:
    *   Audit, deprecate, then remove if unused legacy memory/task files.
    *   Audit and consolidate the Wake Word pipeline overlapping logic.
    *   Ensure all configuration is loaded via environment variables rather than hardcoded fallbacks.

### Phase 2: Intelligence & Memory Wiring (Completed)
*   **Goal**: Stabilize the memory lifecycle and expand AI capabilities.
*   **Tasks**:
    *   Extend `brain/memory/memory_manager.py` to handle Working -> Short -> Long term consolidation.

### Phase 3: Runtimes & UI Synchronization (Current)
*   **Goal**: Ensure the backend and frontend runtimes communicate safely without blocking threads.
*   **Tasks**:
    *   Extend `desktop/workers/chat_worker.py` to handle bidirectional streaming from the FastAPI layer.

### Phase 4: Emotion, Behavior, and State Generation
*   **Goal**: Bring the robot to life by connecting backend decisions to frontend visuals.
*   **Tasks**:
    *   Implement `brain/emotion/` and `brain/personality/` (extend existing state architectures).
    *   Wire the Decision Engine to emit state changes to `desktop/visual/engine/face_controller.py`.

### Phase 5: Hardening & Hardware
*   **Goal**: Production readiness and physical robot integration.
*   **Tasks**:
    *   Complete the PyTest suite across all modules.
    *   Implement hardware I/O interfaces per hardware specifications.

## 14. Sprint History

### Sprint 1 – Speech Runtime & Pipeline

Status: Completed

Scope:
- brain/voice/whisper_engine.py
- brain/voice/speech_to_text.py
- brain/voice/recorder.py
- brain/voice/vad.py
- brain/runtime/voice_runtime.py

Result:
End-to-end speech pipeline has been implemented and runtime verified. VoiceRuntime utilizes a dedicated worker thread with thread-safe interaction locking and safely manages the WakeWord listener lifecycle without deadlocking PortAudio.

Commit:
Completed

Approved:
Yes

### Sprint 2 – Core Request Pipeline Integration

Status: Completed

Scope

- brain/core/dispatcher.py
- brain/core/handlers/
- brain/ai/planner.py
- brain/tools/
- brain/memory/
- assistant.py

Result

Dispatcher, planner, tool execution, memory execution, and Gemini processing were fully integrated into the request pipeline. Runtime verification confirms successful end-to-end request processing across local tools and AI responses.

Commit

Completed

Approved

Yes