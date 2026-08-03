"""
=========================================================
Project G-EXO
Calculator Handler
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from tools.calculator_tool import calculate

from core.response import Response


class CalculatorHandler:

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