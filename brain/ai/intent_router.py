"""
=========================================================
Project G-EXO Intent Router
Version : 2.3
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
            "tasks",
            "todo",
            "todos",
            "add",
            "save",
            "forget",
            "my",
            "file",
            "folder",
            "directory",
            "read",
            "write",
            "append",
            "rename",
            "move",
            "copy",
            "delete",
            "search",
            "list",
            "create",
            "show",
            "display",
            "complete",
            "finish",
            "open",
            "launch",
            "start",
            "run",
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
        # PLANNER (WHOLE WORD MATCHING)
        # =====================================================
        # Uses explicit word boundaries (\b) to prevent substring false positives
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