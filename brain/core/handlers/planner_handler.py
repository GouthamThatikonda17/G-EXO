"""
=========================================================
Project G-EXO
Planner Handler
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.planner import AIPlanner
from ai.executor import AIExecutor

from core.response import Response
from core.response_builder import ResponseBuilder


class PlannerHandler:

    def __init__(self):

        self.planner = AIPlanner()
        self.executor = AIExecutor()

    def handle(self, request):

        try:

            plan = self.planner.plan(request.message)

            result = self.executor.execute(plan)

            return ResponseBuilder.build(
                plan=plan,
                result=result,
            )

        except Exception as e:

            return Response(
                success=False,
                message=str(e),
            )