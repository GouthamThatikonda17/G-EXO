# G-EXO Software Architecture

## Overview

The G-EXO software ecosystem is divided into independent layers.

Each layer can evolve without breaking the others.

---

## Layer 1 — G-EXO Core

Language:
Python

Responsibilities:

- AI
- Memory
- Notes
- Tasks
- Reminders
- File Management
- Logic
- Planning

This is the heart of G-EXO.

---

## Layer 2 — API Layer

Responsibilities:

Expose G-EXO Core to external devices.

Future examples:

- Android
- Robot
- Web Dashboard

Communication:

REST API

or

WebSocket

---

## Layer 3 — Android Application

Responsibilities:

- Chat UI
- Voice Commands
- Notifications
- Camera
- Bluetooth
- GPS
- Contacts
- Calendar

The Android app acts as the brain of the robot.

---

## Layer 4 — Robot Firmware

Responsibilities:

- Motors
- Wheels
- Sensors
- Battery
- Servos
- LEDs

Robot firmware never contains AI.

It only executes commands received from the phone.

---

## Layer 5 — Cloud Services (Optional)

Future:

- AI models
- Music generation
- Image generation
- Cloud backup
- Device synchronization

---

## Data Flow

User

↓

Android App

↓

API Layer

↓

G-EXO Core

↓

Robot

---

## Design Principles

- Modular
- Offline-first
- Secure
- Scalable
- Reusable