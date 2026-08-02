"""
=========================================================
Project G-EXO
Gemini AI Provider
Version : 4.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os

from dotenv import load_dotenv
from google import genai

from ai.prompts import SYSTEM_PROMPT, PLANNER_PROMPT
from ai.provider import AIProvider

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded API Key:", API_KEY[:12] if API_KEY else "None")

class GeminiProvider(AIProvider):

    def __init__(self):

        if not API_KEY:

            raise ValueError(
                "GEMINI_API_KEY not found in .env file."
            )

        self.client = genai.Client(
            api_key=API_KEY
        )

    # =====================================================
    # CHAT
    # =====================================================

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
            )

            return response.text.strip()

        except Exception as e:

            return f"Gemini Error: {str(e)}"

    # =====================================================
    # PLANNER
    # =====================================================

    def plan(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"{PLANNER_PROMPT}\n\nUser: {prompt}",
            )

            return response.text.strip()

        except Exception:

            return (
                '{"intent":"chat",'
                '"tool":null,'
                '"action":null,'
                '"arguments":{}}'
            )