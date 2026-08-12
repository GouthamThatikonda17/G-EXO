"""
=========================================================
Project G-EXO Gemini AI Provider
Version : 4.4
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai.prompts import SYSTEM_PROMPT, PLANNER_PROMPT
from ai.provider import AIProvider
from ai.exceptions import (
    ProviderError,
    ProviderAuthenticationError,
    ProviderQuotaExceededError,
    ProviderModelNotFoundError,
    ProviderNetworkError
)

load_dotenv()

class GeminiProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ProviderAuthenticationError("GEMINI_API_KEY not found in environment configuration.")

        self.model = os.getenv("GEMINI_MODEL")
        if not self.model:
            raise ProviderModelNotFoundError("GEMINI_MODEL not found in environment configuration.")

        self.client = genai.Client(api_key=api_key)

    def _translate_error(self, e: Exception):
        error_str = str(e).upper()
        if "404" in error_str or "NOT_FOUND" in error_str:
            raise ProviderModelNotFoundError(f"404 Model Not Found: {e}")
        elif "401" in error_str or "UNAUTHENTICATED" in error_str or "403" in error_str or "PERMISSION_DENIED" in error_str:
            raise ProviderAuthenticationError(f"Authentication/Permission Denied: {e}")
        elif "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "QUOTA" in error_str:
            raise ProviderQuotaExceededError(f"Quota Exceeded: {e}")
        else:
            raise ProviderNetworkError(f"Gemini API Error: {e}")

    # =====================================================
    # CHAT
    # =====================================================
    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
            )
            if not response or not response.text:
                raise ProviderError("Gemini returned an empty text response.")
            return response.text.strip()
        except ProviderError:
            raise
        except Exception as e:
            self._translate_error(e)

    # =====================================================
    # PLANNER
    # =====================================================
    def plan(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{PLANNER_PROMPT}\n\nUser: {prompt}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            if not response or not response.text:
                raise ProviderError("Gemini returned an empty text plan.")
            return response.text.strip()
        except ProviderError:
            raise
        except Exception as e:
            self._translate_error(e)
