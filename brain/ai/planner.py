"""
=========================================================
Project G-EXO
AI Planner
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""


class AIPlanner:

    def __init__(self):

        pass

    def plan(self, message: str):

        message = message.lower().strip()

        if message.startswith("remember"):

            return {
                "intent": "memory",
                "tool": "memory",
                "action": "remember",
                "arguments": {},
            }

        if message.startswith("note"):

            return {
                "intent": "notes",
                "tool": "notes",
                "action": "add",
                "arguments": {},
            }

        if message.startswith("todo"):

            return {
                "intent": "tasks",
                "tool": "tasks",
                "action": "add",
                "arguments": {},
            }

        return {
            "intent": "chat",
            "tool": None,
            "action": None,
            "arguments": {},
        }