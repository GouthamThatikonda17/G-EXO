"""
=========================================================
Project G-EXO Ollama AI Provider
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

class OllamaProvider(AIProvider):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST")
        if not self.host:
            raise ProviderNetworkError("OLLAMA_HOST not found in environment configuration.")

        self.model = os.getenv("OLLAMA_MODEL")
        if not self.model:
            raise ProviderModelNotFoundError("OLLAMA_MODEL not found in environment configuration.")

        # Fast fail connectivity check during lazy initialization
        url = f"{self.host}/api/tags"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status != 200:
                    raise ProviderNetworkError(f"Ollama server returned non-200 status: {resp.status}")
        except urllib.error.URLError as e:
            if isinstance(e.reason, (socket.timeout, TimeoutError)):
                raise ProviderNetworkError(f"Ollama server timeout at {self.host}: {e}")
            raise ProviderNetworkError(f"Ollama server is unavailable at {self.host}: {e}")
        except (socket.timeout, TimeoutError) as e:
            raise ProviderNetworkError(f"Ollama server timeout at {self.host}: {e}")
        except Exception as e:
            raise ProviderError(f"Ollama initialization failed: {e}")

    def _translate_error(self, e: Exception):
        if isinstance(e, urllib.error.HTTPError):
            if e.code == 404:
                raise ProviderModelNotFoundError(f"404 Model Not Found: {e}")
            elif e.code in (401, 403):
                raise ProviderAuthenticationError(f"Authentication/Permission Denied: {e}")
            elif e.code == 429:
                raise ProviderQuotaExceededError(f"Quota Exceeded: {e}")
            else:
                raise ProviderNetworkError(f"HTTP Error {e.code}: {e}")
        elif isinstance(e, urllib.error.URLError):
            if isinstance(e.reason, (socket.timeout, TimeoutError)):
                raise ProviderNetworkError(f"Timeout Error: {e}")
            raise ProviderNetworkError(f"Network Error: {e}")
        elif isinstance(e, (socket.timeout, TimeoutError)):
            raise ProviderNetworkError(f"Timeout Error: {e}")
        else:
            raise ProviderError(f"Unknown Error: {e}")

    # =====================================================
    # CHAT
    # =====================================================
    def generate(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "response" not in res_data:
                    raise ProviderError(f"Ollama returned invalid payload: {res_data}")
                return res_data["response"].strip()
        except Exception as e:
            self._translate_error(e)

    # =====================================================
    # PLANNER
    # =====================================================
    def plan(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{PLANNER_PROMPT}\n\nUser: {prompt}",
            "stream": False,
            "format": "json"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "response" not in res_data:
                    raise ProviderError(f"Ollama returned invalid payload: {res_data}")
                return res_data["response"].strip()
        except Exception as e:
            self._translate_error(e)
