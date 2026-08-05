"""
=========================================================
Project G-EXO AI Planner
Version : 4.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
from ai.ai_service import AIService


class AIPlanner:
    def __init__(self):
        self.ai = AIService()

    def plan(self, message: str) -> dict:
        try:
            response = self.ai.plan(message)
            return json.loads(response)
        except Exception:
            return {
                "intent": "chat",
                "tool": None,
                "action": None,
                "arguments": {},
            }