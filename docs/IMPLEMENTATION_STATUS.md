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
Overall, the repository maintains a clear, decoupled architecture separating the PyQt6 frontend (`desktop/`) from the backend (`brain/`). The Core Request Pipeline, Voice Runtime, and Desktop asynchronous execution pipeline are now runtime-verified. Desktop requests execute safely on dedicated worker threads without blocking the PyQt event loop, and worker lifecycle management has been validated through graceful shutdown testing. Remaining work focuses on full desktop UI integration, backend/frontend synchronization, and production hardening.

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
| **Desktop UI & Visuals** | Yes | Partial | No | Vector face engine exists. Asynchronous Brain execution is integrated. Chat widgets remain disconnected pending Sprint 3.3. |
| **API & Schemas** | Yes | Partial | No | FastAPI routes and schemas are implemented. Desktop currently follows the direct `GEXOBrain` architecture. |
| **AI & Planner** | Yes | Yes | No | Dispatcher, planner, Gemini provider, and tool execution are fully integrated and runtime verified. |
| **Memory System** | Partial | Partial | No | Memory execution is integrated. Background consolidation lifecycle remains incomplete. |
| **Voice Runtime** | Yes | Yes | No | Fully operational. Thread-safe worker architecture verified. |
| **Decision Engine** | No | No | No | Rules and context evaluation require expansion. |
| **Emotion & Personality** | No | No | No | Modules remain structural stubs. |
| **Testing Suite** | Partial | Partial | No | Runtime validation completed for core execution paths. Automated test coverage remains limited. |

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

### Phase 3: Runtimes & UI Synchronization (In Progress)

**Goal**

Ensure the backend and frontend runtimes communicate safely without blocking execution while progressively integrating the desktop interface.

**Completed**

- Sprint 3.1 — Voice Runtime thread safety completed.
- Sprint 3.2 — Desktop asynchronous Brain execution completed.
- ChatWorker integrated with `MainWindow`.
- Dedicated `QThread` execution verified.
- Worker lifecycle cleanup implemented.
- Graceful shutdown verified.
- Concurrent request protection implemented.

**Remaining**

- Sprint 3.3 — Integrate existing desktop widgets (`ChatArea`, `MessageInput`, `Sidebar`, `TopBar`).
- Synchronize desktop message lifecycle with `BehaviorEngine`.
- Connect desktop widgets to `ChatWorker`.
- Complete frontend/backend runtime synchronization.

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


### Sprint 3.1 – Voice Runtime Thread Safety

Status: Completed

Scope

- brain/runtime/voice_runtime.py

Result

Introduced a dedicated interaction worker thread for the Voice Runtime, eliminating PortAudio callback blocking and microphone contention. Implemented thread-safe interaction locking, safe listener lifecycle management, and verified end-to-end voice execution.

Commit

Completed

Approved

Yes

---

### Sprint 3.2 – Desktop Asynchronous Brain Execution

Status: Completed

Scope

- desktop/main_window.py

Result

Integrated asynchronous desktop execution using `ChatWorker` and `QThread` while preserving the direct `GEXOBrain` architecture. Implemented concurrency protection, centralized worker lifecycle cleanup, behavior state synchronization, temporary development trigger, and graceful shutdown handling. Runtime testing verified responsive UI, correct worker lifecycle management, and clean application shutdown.

Verified

✓ Desktop remains responsive during AI execution

✓ `ChatWorker` executes `GEXOBrain.process()`

✓ Concurrent requests are rejected safely

✓ Worker lifecycle cleanup centralized

✓ Graceful shutdown verified

✓ Behavior synchronization (Idle → Thinking → Speaking → Idle)

Commit

Completed

Approved

Yes