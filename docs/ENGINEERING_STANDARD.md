# Project G-EXO Engineering Standard

## 1. Repository First Rule
- The uploaded repository is the highest priority source of truth.
- Documentation guides architecture but does not override the repository.
- If documentation and code disagree, report the conflict before implementation.

## 2. Sprint Rules
- One sprint = one engineering objective.
- Modify the minimum number of files.
- Deliver one independently testable capability.
- Do not continue into another sprint automatically.

## 3. Repository Audit
Before any implementation:
- Read the uploaded documentation.
- Read the uploaded source files.
- Inspect dependencies.
- Identify current implementation.
- Identify repository evidence.
- Explain limitations.
- Justify every modification.

## 4. Architecture Rules
- Preserve subsystem ownership.
- One owner per subsystem.
- High cohesion.
- Low coupling.
- Do not redesign architecture unless explicitly approved.
- Preserve backward compatibility.

## 5. Implementation Rules
- Complete production-ready files only.
- No snippets unless requested.
- No invented APIs.
- No invented imports.
- No invented execution paths.
- Keep naming consistent.
- Preserve constructor signatures.
- Preserve public APIs.

## 6. Runtime Verification
Every sprint must include runtime testing before commit.

Examples:
- Positive tests.
- Negative tests.
- Existing functionality.
- Regression testing.

## 7. Git Workflow
Audit
↓

Implementation Plan
↓

Approval
↓

Implementation
↓

Runtime Tests
↓

Fixes
↓

Commit
↓

Push

A sprint is not complete until the code is runtime tested, committed, and pushed.

## 8. Bug Fix Ownership
Fix defects at the earliest responsible layer.
Do not hide bugs by adding downstream fallbacks.
Do not duplicate responsibilities.

## 9. Evidence Rule
Every proposed modification must include:
- Current implementation.
- Repository evidence.
- Identified limitation.
- Why it blocks the sprint.
- Minimal required modification.

Without repository evidence:
Do not modify the file.
Ask for the required source code instead.