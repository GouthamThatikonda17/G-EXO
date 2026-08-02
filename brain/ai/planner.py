"""
=========================================================
Project G-EXO
AI Planner
Version : 4.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json

from ai.gemini import GeminiProvider


class AIPlanner:

    def __init__(self):

        self.ai = GeminiProvider()

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