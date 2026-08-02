"""
=========================================================
Project G-EXO
AI Router
Version : 3.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.gemini import GeminiProvider
from ai.planner import AIPlanner
from ai.executor import AIExecutor


class AIRouter:

    def __init__(self):

        self.ai = GeminiProvider()
        self.planner = AIPlanner()
        self.executor = AIExecutor()

    def chat(self, prompt):

        # Step 1: Create a plan
        plan = self.planner.plan(prompt)

        print(f"PLAN: {plan}")

        # Step 2: Execute the plan
        result = self.executor.execute(plan)

        # Step 3: If a tool executed successfully,
        # return its result directly.
        if result is not None:

            return result

        # Step 4: Otherwise continue normal AI chat.
        return self.ai.generate(prompt)