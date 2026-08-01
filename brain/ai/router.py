"""
=========================================================
Project G-EXO
AI Router
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.gemini import GeminiProvider
from ai.planner import AIPlanner


class AIRouter:

    def __init__(self):

        self.ai = GeminiProvider()
        self.planner = AIPlanner()

    def chat(self, prompt):

        plan = self.planner.plan(prompt)

        print(f"PLAN: {plan}")

        return self.ai.generate(prompt)