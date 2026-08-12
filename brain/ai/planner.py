# brain/ai/planner.py
"""
=========================================================
Project G-EXO AI Planner
Version : 4.5
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
from ai.ai_service import AIService
from ai.exceptions import ProviderError, PlannerError
from logger import log

class AIPlanner:
    def __init__(self):
        self.ai = AIService()

    def _extract_json(self, text: str) -> str:
        """Robustly extracts exactly one JSON object using brace counting."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        start_idx = text.find('{')
        if start_idx == -1:
            raise PlannerError("No JSON object found in the response.")

        depth = 0
        end_idx = -1
        in_string = False
        escape_next = False

        for i in range(start_idx, len(text)):
            char = text[i]

            if escape_next:
                escape_next = False
                continue

            if char == '\\':
                escape_next = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        end_idx = i
                        break

        if end_idx == -1:
            raise PlannerError("Incomplete JSON object (missing closing brace).")

        return text[start_idx:end_idx+1]

    def plan(self, message: str) -> dict:
        prompt = message

        for attempt in range(2):
            raw_response = ""
            try:
                raw_response = self.ai.plan(prompt)
                log(f"[AIPlanner] Raw response: {raw_response}", "DEBUG")

                extracted_json = self._extract_json(raw_response)
                plan = json.loads(extracted_json)

                if not isinstance(plan, dict):
                    raise PlannerError("Parsed JSON is not a dictionary.")

                required_keys = ["intent", "tool", "action", "arguments"]
                for key in required_keys:
                    if key not in plan:
                        raise PlannerError(f"Missing required JSON routing keys: '{key}'.")

                return plan

            except ProviderError as e:
                # Propagate native network/auth/quota errors immediately without retry
                raise e

            except Exception as e:
                # Trap JSON extraction/validation and runtime errors for exactly one retry
                log(f"[AIPlanner] Plan parsing error on attempt {attempt + 1}: {e}", "ERROR")

                if attempt == 0:
                    prompt = (
                        f"Original request: {message}\n\n"
                        f"Your previous response was invalid: {str(e)}\n"
                        "Return EXACTLY ONE valid JSON object. No explanation. No markdown."
                    )
                else:
                    raise PlannerError(f"Planner failed to generate a valid plan: {str(e)}")

        raise PlannerError("Planner exhausted retry attempts.")
