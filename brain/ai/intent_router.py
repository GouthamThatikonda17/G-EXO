"""
=========================================================
Project G-EXO Intent Router
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import re
from tools.app_metadata import SUPPORTED_APPS

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
        
        # Build dynamic regex using the shared application identities.
        # This keeps routing strict and dynamic without duplicate app lists.
        supported_apps = "|".join(re.escape(app) for app in SUPPORTED_APPS.keys())
        self.app_pattern = re.compile(
            rf"^(open|launch|start|run)\s+({supported_apps})$", 
            re.IGNORECASE
        )

    def _is_math_expression(self, text: str) -> bool:
        text = text.strip()
        pattern = r"^\s*\d+(\.\d+)?\s*[\+\-\*/%]\s*\d+(\.\d+)?\s*$"
        return re.match(pattern, text) is not None

    def _is_app_command(self, text: str) -> bool:
        return self.app_pattern.match(text.strip()) is not None

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
        # COMMAND PATTERN (STRICT ROUTING)
        # =====================================================
        if self._is_app_command(text):
            return {
                "route": "planner"
            }

        # =====================================================
        # PLANNER (WHOLE WORD MATCHING)
        # =====================================================
        # Uses explicit word boundaries to prevent substring false positives
        if any(re.search(rf"\b{keyword}\b", text) for keyword in self.planner_keywords):
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