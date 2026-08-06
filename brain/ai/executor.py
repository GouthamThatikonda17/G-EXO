"""
=========================================================
Project G-EXO AI Executor
Version : 3.3
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
        arguments = plan.get("arguments")

        if not isinstance(arguments, dict):
            arguments = {}

        # Fallback for flattened LLM JSON outputs where the model 
        # hallucinates arguments at the root level.
        if not arguments:
            reserved_keys = {"intent", "tool", "action", "arguments"}
            arguments = {k: v for k, v in plan.items() if k not in reserved_keys}
        else:
            # Prevent reserved keys (like 'action') from duplicating in kwargs
            arguments = {
                k: v for k, v in arguments.items() 
                if k not in {"intent", "tool", "action", "arguments"}
            }

        # No tool required
        if tool is None:
            return None

        # Execute selected tool via robust keyword mapping
        return self.registry.execute(
            tool,
            action,
            **arguments
        )