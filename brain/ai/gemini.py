"""
=========================================================
Project G-EXO
Gemini AI Provider
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
from ai.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
from google import genai

from ai.provider import AIProvider

# Load .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiProvider(AIProvider):

    def __init__(self):

        if not API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file."
            )

        self.client = genai.Client(api_key=API_KEY)

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
            )

            return response.text

        except Exception as e:

            return f"Gemini Error: {e}"