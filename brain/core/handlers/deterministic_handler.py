"""
=========================================================
Project G-EXO Deterministic Handler
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.deterministic_parser import DeterministicParser
from ai.executor import AIExecutor
from core.response import Response
from core.response_builder import ResponseBuilder

class DeterministicHandler:
    """
    Executes unambiguous commands entirely bypassing the LLM layer.
    """
    def __init__(self):
        self.parser = DeterministicParser()
        self.executor = AIExecutor()

    def handle(self, request) -> Response:
        try:
            # 1. Parse structured plan natively
            plan = self.parser.parse(request.message)
            if not plan:
                return Response(
                    success=False,
                    message="Failed to parse deterministic command natively."
                )
            
            # 2. Execute directly via the standard execution boundary
            result = self.executor.execute(plan)
            
            # 3. Build response exactly as the PlannerHandler would
            return ResponseBuilder.build(
                plan=plan,
                result=result,
            )
        except Exception as e:
            return Response(
                success=False,
                message=f"Deterministic Execution Error: {str(e)}",
            )