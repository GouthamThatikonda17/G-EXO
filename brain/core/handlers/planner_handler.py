"""
=========================================================
Project G-EXO Planner Handler
Version : 2.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.planner import AIPlanner
from ai.executor import AIExecutor
from ai.exceptions import PlannerError, ProviderError
from core.response import Response
from core.response_builder import ResponseBuilder

class PlannerHandler:
    def __init__(self):
        self.planner = AIPlanner()
        self.executor = AIExecutor()

    def handle(self, request):
        try:
            plan = self.planner.plan(request.message)

            # =====================================================
            # CRITICAL CORRECTION: ABORT CHAT FALLBACKS
            # =====================================================
            # If a command reached the PlannerHandler (via IntentRouter), it is an
            # operational request. We must NEVER substitute a failed operational
            # command with a conversational response.
            if plan.get("intent") == "chat":
                raise PlannerError("Planner attempted to fall back to chat for an operational command.")

            # Deterministic Execution
            result = self.executor.execute(plan)

            return ResponseBuilder.build(
                plan=plan,
                result=result,
            )

        except (PlannerError, ProviderError) as e:
            # Trap structured LLM generation, validation, or network failures.
            # Explicitly drops the silent fallback to conversational generation.
            return Response(
                success=False,
                message=f"Planner Execution Error: I couldn't process that command. {str(e)}",
            )
        except Exception as e:
            # Separate isolation layer for internal execution/python code failures.
            return Response(
                success=False,
                message=f"Internal System Error: {str(e)}",
            )
