"""
=========================================================
Project G-EXO AI Executor
Version : 3.5
Developer : Thatikonda Goutham Teja
=========================================================
"""

from tools.registry import ToolRegistry
from ai.exceptions import PlannerError

class AIExecutor:
    def __init__(self):
        self.registry = ToolRegistry()

    def execute(self, plan: dict):
        tool = plan.get("tool")
        action = plan.get("action")

        # No tool required
        if tool is None:
            return None

        # Strict validation: Rejects flattened plans and missing keys entirely.
        # No silent creation of empty {} dictionaries.
        if "arguments" not in plan:
            raise PlannerError("Planner output is missing 'arguments'.")

        arguments = plan.get("arguments")
        if not isinstance(arguments, dict):
            raise PlannerError("Planner output field 'arguments' must be an object.")

        try:
            # Execute selected tool via strict keyword mapping.
            # No positional overrides or fallback injections are permitted.
            return self.registry.execute(
                tool,
                action,
                **arguments
            )
        except ValueError as e:
            # Safely trap Level 2 contract validation failures
            # (e.g., missing, unknown, or empty required arguments)
            # and surface them cleanly as deterministic PlannerErrors.
            raise PlannerError(str(e))
