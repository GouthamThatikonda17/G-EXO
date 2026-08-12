"""
=========================================================
Project G-EXO OpenRouter AI Provider
Version : 1.3
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
import json
import urllib.request
import urllib.error
import socket
from dotenv import load_dotenv

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

class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ProviderAuthenticationError("OPENROUTER_API_KEY not found in environment configuration.")

        self.model = os.getenv("OPENROUTER_MODEL")
        if not self.model:
            raise ProviderModelNotFoundError("OPENROUTER_MODEL not found in environment configuration.")

        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def _call_api(self, messages: list, expect_json: bool = False) -> str:
        payload = {
            "model": self.model,
            "messages": messages
        }

        if expect_json:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/G-EXO",
            "X-Title": "G-EXO"
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "choices" not in res_data or not res_data["choices"]:
                    raise ProviderError(f"OpenRouter returned invalid response structure: {res_data}")
                return res_data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ProviderModelNotFoundError(f"404 Model Not Found: {e}")
            elif e.code in (401, 403):
                raise ProviderAuthenticationError(f"Authentication/Permission Denied: {e}")
            elif e.code == 429:
                raise ProviderQuotaExceededError(f"Quota Exceeded: {e}")
            else:
                raise ProviderNetworkError(f"HTTP Error {e.code}: {e}")
        except urllib.error.URLError as e:
            if isinstance(e.reason, (socket.timeout, TimeoutError)):
                raise ProviderNetworkError(f"Timeout Error: {e}")
            raise ProviderNetworkError(f"Network Error: {e}")
        except (socket.timeout, TimeoutError) as e:
            raise ProviderNetworkError(f"Timeout Error: {e}")
        except Exception as e:
            raise ProviderError(f"Unknown Error: {e}")

    # =====================================================
    # CHAT
    # =====================================================
    def generate(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        return self._call_api(messages)

    # =====================================================
    # PLANNER
    # =====================================================
    def plan(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": prompt}
        ]
        return self._call_api(messages, expect_json=True)
