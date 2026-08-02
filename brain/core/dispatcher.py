"""
=========================================================
Project G-EXO
Dispatcher
Version : 5.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.intent_router import IntentRouter

from core.request import Request
from core.response import Response

from core.handlers.chat_handler import ChatHandler
from core.handlers.planner_handler import PlannerHandler
from core.handlers.calculator_handler import CalculatorHandler
from core.handlers.local_handler import LocalHandler

from logger import (
    log_request,
    log_response,
    log_exception,
)


class Dispatcher:

    def __init__(self):

        self.router = IntentRouter()

        self.handlers = {

            "chat": ChatHandler(),

            "planner": PlannerHandler(),

            "calculator": CalculatorHandler(),

            "local": LocalHandler(),

        }

    def dispatch(self, request: Request) -> Response:

        try:

            route = self.router.route(request.message)["route"]

            log_request(route, request.message)

            handler = self.handlers.get(route)

            if handler is None:

                response = Response(
                    success=False,
                    message=f"No handler available for route '{route}'."
                )

                log_response(
                    response.success,
                    response.message,
                )

                return response

            response = handler.handle(request)

            log_response(
                response.success,
                response.message,
            )

            return response

        except Exception as e:

            log_exception(e)

            return Response(
                success=False,
                message="Internal Dispatcher Error."
            )