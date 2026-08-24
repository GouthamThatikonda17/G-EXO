# Sprint 4.4 — Emotion State Engine

## Objective

Create a controlled internal emotional state representation owned entirely by G-EXO.

The Emotion State Engine must provide a deterministic, persistent, platform-independent emotional state that can be consumed by future Personality, Decision, Expression, Voice, Mobile, and Physical Embodiment systems.

The LLM must not own, directly mutate, or arbitrarily overwrite G-EXO's persistent emotional state.

The Emotion Engine must remain independent from AI providers, UI rendering, voice hardware, and desktop-specific implementation.

---

# 1. Architectural Principles

The following principles are mandatory.

### 1.1 G-EXO owns emotional state

The emotional state belongs to the G-EXO core architecture.

It must not belong to:

- AIService
- Gemini provider
- Ollama provider
- OpenRouter provider
- Desktop UI
- VoiceRuntime
- ChatWorker
- individual tools
- individual handlers

### 1.2 LLM does not own emotion

AI-generated text may provide contextual information that can eventually influence emotional evaluation, but the LLM must never directly assign or persist G-EXO's internal emotional state.

The Emotion Engine owns state transitions.

### 1.3 Deterministic behavior

Given the same initial state and the same sequence of emotional inputs, the Emotion Engine must produce the same resulting state.

There must be no random or provider-dependent state mutation.

### 1.4 Platform independence

The Emotion Engine must contain no:

- PySide6 imports
- Android imports
- audio-device dependencies
- rendering dependencies
- UI callbacks
- hardware-specific code

It must be usable from:

- CLI
- Desktop
- Voice Runtime
- Android
- future physical robot systems

### 1.5 Explicit interfaces

Future systems must consume the emotional state through explicit APIs.

They must not access private implementation details of the Emotion Engine.

---

# 2. Emotion Model

Create a strongly typed emotional state representation.

The initial supported emotional states are:

- NEUTRAL
- HAPPY
- SAD
- ANGRY

The model must be extensible so additional emotional states can be introduced later without redesigning the entire architecture.

The emotional state must be represented independently from `FaceState`.

`EmotionState` represents the internal passive emotional condition.

`FaceState` represents the currently rendered/active presentation condition.

These two concepts must not be conflated.

---

# 3. EmotionEngine

Create:

`brain/emotion/emotion_engine.py`

The `EmotionEngine` is responsible for:

- owning the current emotional state
- initializing the state deterministically
- receiving controlled emotional inputs
- evaluating state transitions
- persisting the resulting state for the lifetime of the engine
- exposing the current state through a public API
- providing a controlled reset operation if required

The engine must not perform:

- LLM calls
- tool execution
- UI rendering
- voice recording
- speech synthesis
- file persistence
- hardware operations

---

# 4. EmotionState Model

Create the required emotional state model under:

`brain/emotion/`

The implementation must provide a clear representation of:

- current emotion
- confidence/intensity information where required by the existing architecture
- deterministic state information required for future consumers

The representation must be immutable where appropriate for transport.

Do not expose mutable internal state directly.

Consumers should receive a safe state representation rather than a reference that allows arbitrary mutation.

---

# 5. Emotion Input

The Emotion Engine must expose an explicit method for receiving an emotional event/input.

The exact API should follow existing project naming and engineering conventions.

Do not invent unnecessary abstraction layers.

The input mechanism must allow future systems to communicate events such as:

- successful interaction
- failed interaction
- positive user interaction
- negative user interaction
- successful task completion
- task failure
- conversational engagement

The initial implementation must remain intentionally small.

Do not implement speculative machine-learning emotion detection.

Do not implement facial recognition.

Do not implement sentiment analysis using an external LLM.

Do not implement long-term mood prediction.

Those belong to future milestones.

---

# 6. Deterministic Transition Rules

Emotion transitions must be controlled by deterministic rules owned by G-EXO.

The initial rules must be simple and explicit.

Examples of permitted deterministic transitions include:

- successful positive interaction → HAPPY
- unsuccessful/error interaction → SAD
- explicit hostile/error condition → ANGRY
- neutral interaction → NEUTRAL

The exact transition table must be represented explicitly in the implementation rather than hidden inside arbitrary LLM output.

The engine must never accept an arbitrary string such as:

`"You are angry now"`

as authoritative state mutation.

Only recognized and validated emotional events may affect state.

---

# 7. Persistence Semantics

For Sprint 4.4, "persistent" means the emotional state survives across multiple operations during the lifetime of the G-EXO core instance.

Example:

```text
Initial:
NEUTRAL

Interaction 1:
positive event
→ HAPPY

Interaction 2:
neutral event
→ HAPPY

Interaction 3:
negative event
→ SAD