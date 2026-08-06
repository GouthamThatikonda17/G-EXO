"""
=========================================================
Project G-EXO AI Planner
Version : 4.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
import json
from ai.ai_service import AIService

class AIPlanner:
    def __init__(self):
        # Restored AIService abstraction for automatic provider fallback
        self.ai = AIService()

    def plan(self, message: str) -> dict:
        try:
            response = self.ai.plan(message)
           
            # Clean markdown JSON block formatting if hallucinated
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:]
            
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
                
            clean_response = clean_response.strip()
            
            # Fix missing outer braces hallucination
            if clean_response and not clean_response.startswith("{"):
                clean_response = "{" + clean_response + "}"
                
            plan = json.loads(clean_response)

           

            return plan
        
        except Exception:
            return {
                "intent": "chat",
                "tool": None,
                "action": None,
                "arguments": {},
            }