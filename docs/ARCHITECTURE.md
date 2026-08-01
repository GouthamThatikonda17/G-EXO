# G-EXO Architecture

## Philosophy

G-EXO is designed using a modular architecture.

Each component has one responsibility.

No module should directly depend on unrelated modules.

The AI coordinates modules instead of replacing them.

---

# High-Level Architecture

                    User
                      │
                      ▼
              Interface Layer
      (Desktop / Mobile / Voice)
                      │
                      ▼
                Assistant Core
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
     Local Commands  AI Engine   Future API
                      │
                      ▼
               Gemini Provider
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

# Layers

## Interface Layer

Purpose:

How users communicate with G-EXO.

Examples:

- Desktop CLI
- Android App
- Voice Interface
- Robot Interface

---

## Assistant Core

Responsibilities:

- Receive user input
- Decide where to send it
- Manage conversations
- Coordinate AI

---

## AI Layer

Responsibilities:

- Chat
- Reasoning
- Planning
- Tool selection

---

## Tool Layer

Responsibilities:

Allow AI to safely use internal modules.

Examples:

- Calculator
- Notes
- Memory
- Tasks

---

## Module Layer

Business logic only.

Examples:

- Memory
- Notes
- Tasks
- Reminders
- Calculator

Modules should never depend on AI.

---

## Storage Layer

Responsible for:

- JSON
- SQLite (future)
- Configuration
- User data

---

# Future Components

Desktop

↓

Android

↓

Robot

↓

Cloud

↓

Smart Home

All use the same G-EXO Core.

---

# Development Rules

1. Every feature belongs to one module.

2. Modules expose clean Python functions.

3. AI never directly edits files.

4. AI only uses approved tools.

5. Business logic and user interface remain separate.

6. Keep modules small and focused.

7. Prefer reusable components over duplicate code.

---

# Long-Term Goal

One AI Core.

Multiple interfaces.

Desktop.

Mobile.

Robot.

Future devices.