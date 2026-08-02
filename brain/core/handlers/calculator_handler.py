"""
=========================================================
Project G-EXO
Calculator Handler
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from modules.calculator import calculate

from core.response import Response


class CalculatorHandler:

    def __init__(self):

        pass

    def handle(self, request):

        try:

            result = calculate(request.message)

            return Response(
                success=True,
                message=str(result),
                data=result,
            )

        except Exception as e:

            return Response(
                success=False,
                message=f"Calculator Error: {e}",
            )