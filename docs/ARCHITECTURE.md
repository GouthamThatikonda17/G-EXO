# G-EXO Architecture

## Philosophy

G-EXO is designed using a modular architecture.
Each component has one responsibility.
No module should directly depend on unrelated modules.
The Cognitive Component (LLM) coordinates logic instead of replacing it.

---

# High-Level Architecture

                    User
                      │
                      ▼
              Development/Testing Interfaces
              (CLI / Desktop GUI)
                      │
                      ▼
                Assistant Core
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
     Local Commands  Cognitive     Future API
                     Component
                     (LLM)
                      │
                      ▼
              Internal AI Tools
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
   Memory          Notes            Tasks
      ▼               ▼                ▼
 Configuration     Storage          Storage

---

# Architecture Pipeline

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

# Layers

## Interface Layer
Purpose:
How developers and users communicate with G-EXO.
Examples:
- Development/Testing Interface (CLI)
- Development/Testing Interface (Desktop GUI)
- Android App (Future Mobile Integration)
- Robot Interface (Future Physical Embodiment)

## Assistant Core
Responsibilities:
- Receive user input
- Decide where to send it
- Manage conversations
- Coordinate AI

## Cognitive Component (LLM) Layer
Responsibilities:
- Interpret natural language
- Generate structured plans
- Assist reasoning
- Generate conversational responses

*Note: External AI/LLM providers are cognitive components used by G-EXO. They are NOT the G-EXO Brain itself. The LLM must not become the source of truth for persistent G-EXO state.*

## Tool Layer
Responsibilities:
Allow AI to safely use internal modules. The LLM proposes, G-EXO validates, G-EXO executes, and G-EXO records the actual result.

Examples:
- Calculator
- Notes
- Memory
- Tasks
- Files
- Apps

## Module Layer
Business logic only.
Examples:
- Memory
- Notes
- Tasks
- Reminders
- Calculator
Modules should never depend on AI.

## Storage Layer
Responsible for:
- JSON
- SQLite (future)
- Configuration
- User data

---

# Future Components

Development Interface
↓
Android (Mobile Integration)
↓
Robot (Physical Embodiment)
↓
Cloud
↓
Smart Home

All use the same G-EXO Core.

---

# Critical Architectural Principles

1. G-EXO is a robotic brain/software platform intended for mobile-integrated operation and eventual physical robotic embodiment.
2. The CLI and Desktop GUI are development and testing interfaces only.
3. The final system is intended to operate through mobile and eventually physical robotic interfaces.
4. External AI/LLM providers are cognitive components, not the complete G-EXO brain.
5. G-EXO strictly owns its own internal state, including:
   - Memory
   - Internal State
   - Emotion
   - Personality
   - Decision-making
   - Action state
6. The LLM must not become the source of truth for persistent G-EXO state.
7. Tool execution belongs to deterministic G-EXO software.
8. Future hardware must consume G-EXO decisions/state through explicit interfaces rather than being directly controlled by arbitrary LLM output.

---

# Long-Term Goal
One AI Core.
Mobile Integration.
Robot Embodiment.