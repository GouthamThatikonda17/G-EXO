"""
=========================================================
Project G-EXO
AI Router
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.gemini import GeminiProvider


class AIRouter:

    def __init__(self):

        self.ai = GeminiProvider()

    def chat(self, prompt):

        return self.ai.generate(prompt)