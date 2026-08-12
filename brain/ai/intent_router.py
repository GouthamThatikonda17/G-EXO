# brain/ai/intent_router.py
"""
=========================================================
Project G-EXO Intent Router
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import re
from ai.deterministic_parser import DeterministicParser

class IntentRouter:
    def __init__(self):
        self.local_commands = {
            "help",
            "exit",
            "clear",
            "version",
        }
        
        self.deterministic_parser = DeterministicParser()
        
        # Kept intact for genuinely ambiguous requests
        self.planner_keywords = {
            "remember",
            "note",
            "notes",
            "task",
            "todo",
            "add",
            "save",
            "forget",
            "remind",
            "reminder",
            "reminders",
            "my",
            "file",
            "folder",
            "directory",
            "read",
            "write",
            "rename",
            "move",
            "copy",
            "delete",
            "search",
            "list",
            "create",
        }

    def _is_math_expression(self, text: str) -> bool:
        text = text.strip()
        pattern = r"^\s*\d+(\.\d+)?\s*[\+\-\*/%]\s*\d+(\.\d+)?\s*$"
        return re.match(pattern, text) is not None

    def route(self, message: str) -> dict:
        text = message.lower().strip()
        
        # =====================================================
        # 1. LOCAL
        # =====================================================
        if text in self.local_commands:
            return {
                "route": "local"
            }
            
        # =====================================================
        # 2. DETERMINISTIC
        # =====================================================
        if self.deterministic_parser.parse(text) is not None:
            return {
                "route": "deterministic"
            }

        # =====================================================
        # 3. CALCULATOR
        # =====================================================
        if self._is_math_expression(text):
            return {
                "route": "calculator"
            }
            
        # =====================================================
        # 4. PLANNER (NATURAL LANGUAGE FALLTHROUGH)
        # =====================================================
        # Uses explicit word boundaries (\b) to prevent substring false positives
        if any(re.search(rf"\b{keyword}\b", text) for keyword in self.planner_keywords):
            return {
                "route": "planner"
            }
            
        # =====================================================
        # 5. DEFAULT
        # =====================================================
        return {
            "route": "chat"
        }