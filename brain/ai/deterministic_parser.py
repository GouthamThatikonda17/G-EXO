"""
=========================================================
Project G-EXO Deterministic Command Parser
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

import re
from tools.app_metadata import SUPPORTED_APPS

class DeterministicParser:
    """
    Parses unambiguous operational commands using strict regex grammar.
    Produces the exact JSON-equivalent dict expected by ToolRegistry.
    Contains NO business logic, storage access, or LLM provider calls.
    """
    def __init__(self):
        # Dynamically build exact-match app pattern
        apps_pattern = "|".join(re.escape(app) for app in SUPPORTED_APPS.keys())
        
        # Strict grammar mappings to exact ToolRegistry signatures.
        self.patterns = [
            # =====================================================
            # MEMORY
            # =====================================================
            (re.compile(r"^(?:what is|what's|do you remember) my (.+)$", re.IGNORECASE),
             lambda m: {"intent": "memory", "tool": "memory", "action": "recall", "arguments": {"key": m.group(1).strip()}}),
             
            (re.compile(r"^remember my (.+) is (.+)$", re.IGNORECASE),
             lambda m: {"intent": "memory", "tool": "memory", "action": "remember", "arguments": {"key": m.group(1).strip(), "value": m.group(2).strip()}}),
             
            (re.compile(r"^forget my (.+)$", re.IGNORECASE),
             lambda m: {"intent": "memory", "tool": "memory", "action": "forget", "arguments": {"key": m.group(1).strip()}}),

            # =====================================================
            # NOTES
            # =====================================================
            (re.compile(r"^(?:take a note|create a note|add note)\s+(.+)$", re.IGNORECASE),
             lambda m: {"intent": "notes", "tool": "notes", "action": "add", "arguments": {"text": m.group(1).strip()}}),
             
            (re.compile(r"^(?:show notes|list notes)$", re.IGNORECASE),
             lambda m: {"intent": "notes", "tool": "notes", "action": "show", "arguments": {}}),
             
            (re.compile(r"^delete note (\d+)$", re.IGNORECASE),
             lambda m: {"intent": "notes", "tool": "notes", "action": "delete", "arguments": {"index": int(m.group(1))}}),

            # =====================================================
            # TASKS
            # =====================================================
            (re.compile(r"^add task (.+)$", re.IGNORECASE),
             lambda m: {"intent": "tasks", "tool": "tasks", "action": "add", "arguments": {"task": m.group(1).strip()}}),
             
            (re.compile(r"^(?:show tasks|list tasks)$", re.IGNORECASE),
             lambda m: {"intent": "tasks", "tool": "tasks", "action": "show", "arguments": {}}),
             
            (re.compile(r"^(?:complete task|finish task) (\d+)$", re.IGNORECASE),
             lambda m: {"intent": "tasks", "tool": "tasks", "action": "complete", "arguments": {"task_id": int(m.group(1))}}),
             
            (re.compile(r"^delete task (\d+)$", re.IGNORECASE),
             lambda m: {"intent": "tasks", "tool": "tasks", "action": "delete", "arguments": {"task_id": int(m.group(1))}}),

            # =====================================================
            # REMINDERS
            # =====================================================
            (re.compile(r"^(?:show reminders|list reminders)$", re.IGNORECASE),
             lambda m: {"intent": "reminders", "tool": "reminders", "action": "show", "arguments": {}}),
             
            (re.compile(r"^(?:complete reminder|finish reminder) (\d+)$", re.IGNORECASE),
             lambda m: {"intent": "reminders", "tool": "reminders", "action": "complete", "arguments": {"reminder_id": int(m.group(1))}}),
             
            (re.compile(r"^delete reminder (\d+)$", re.IGNORECASE),
             lambda m: {"intent": "reminders", "tool": "reminders", "action": "delete", "arguments": {"reminder_id": int(m.group(1))}}),
             
            (re.compile(r"^clear reminders$", re.IGNORECASE),
             lambda m: {"intent": "reminders", "tool": "reminders", "action": "clear", "arguments": {}}),

            # =====================================================
            # APPS
            # =====================================================
            (re.compile(rf"^(?:open|launch|start|run)\s+({apps_pattern})$", re.IGNORECASE),
             lambda m: {"intent": "apps", "tool": "apps", "action": "open", "arguments": {"app_name": m.group(1).lower().strip()}}),

            # =====================================================
            # FILES
            # =====================================================
            (re.compile(r"^(?:create file|create a file) (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "create_file", "arguments": {"path": m.group(1).strip()}}),
             
            (re.compile(r"^(?:create folder|create a folder) (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "create_folder", "arguments": {"path": m.group(1).strip()}}),
             
            (re.compile(r"^read (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "read_text", "arguments": {"path": m.group(1).strip()}}),
             
            (re.compile(r"^append (.+) to (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "append_text", "arguments": {"content": m.group(1).strip(), "path": m.group(2).strip()}}),
             
            (re.compile(r"^write (.+) to (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "write_text", "arguments": {"content": m.group(1).strip(), "path": m.group(2).strip()}}),
             
            (re.compile(r"^delete file (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "delete_file", "arguments": {"path": m.group(1).strip()}}),
             
            (re.compile(r"^delete folder (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "delete_folder", "arguments": {"path": m.group(1).strip()}}),
             
            (re.compile(r"^rename (.+) (?:to|into) (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "rename", "arguments": {"path": m.group(1).strip(), "new_path": m.group(2).strip()}}),
             
            (re.compile(r"^move (.+) (?:to|into) (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "move", "arguments": {"source": m.group(1).strip(), "destination": m.group(2).strip()}}),
             
            (re.compile(r"^copy (.+) (?:to|into) (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "copy", "arguments": {"source": m.group(1).strip(), "destination": m.group(2).strip()}}),
             
            (re.compile(r"^(?:list files|show files)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "list", "arguments": {"path": ""}}),
             
            (re.compile(r"^search for (.+)$", re.IGNORECASE),
             lambda m: {"intent": "file", "tool": "file", "action": "search", "arguments": {"filename": m.group(1).strip(), "path": ""}}),
        ]

    def parse(self, text: str) -> dict | None:
        text = text.strip()
        for pattern, builder in self.patterns:
            match = pattern.match(text)
            if match:
                return builder(match)
        return None