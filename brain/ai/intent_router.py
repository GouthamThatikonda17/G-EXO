"""
=========================================================
Project G-EXO Intent Router
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import re

class IntentRouter:
    def __init__(self):
        self.local_commands = {
            "help",
            "exit",
            "clear",
            "version",
        }
        self.planner_keywords = {
            "remember",
            "note",
            "notes",
            "task",
            "todo",
            "add",
            "save",
            "forget",
            "my",
        }

    def _is_math_expression(self, text: str) -> bool:
        text = text.strip()
        pattern = r"^\s*\d+(\.\d+)?\s*[\+\-\*/%]\s*\d+(\.\d+)?\s*$"
        return re.match(pattern, text) is not None

    def route(self, message: str) -> dict:
        text = message.lower().strip()

        # =====================================================
        # LOCAL
        # =====================================================
        if text in self.local_commands:
            return {
                "route": "local"
            }

        # =====================================================
        # PLANNER
        # =====================================================
        for keyword in self.planner_keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                return {
                    "route": "planner"
                }

        # =====================================================
        # CALCULATOR
        # =====================================================
        if self._is_math_expression(text):
            return {
                "route": "calculator"
            }

        # =====================================================
        # DEFAULT
        # =====================================================
        return {
            "route": "chat"
        }