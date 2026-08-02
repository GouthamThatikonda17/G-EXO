"""
=========================================================
Project G-EXO
AI Executor
Version : 3.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from tools.registry import ToolRegistry


class AIExecutor:

    def __init__(self):

        self.registry = ToolRegistry()

    def execute(self, plan: dict):

        tool = plan.get("tool")
        action = plan.get("action")
        arguments = plan.get("arguments", {})

        # No tool required
        if tool is None:

            return None

        # Execute selected tool
        return self.registry.execute(
            tool,
            action,
            *arguments.values()
        )