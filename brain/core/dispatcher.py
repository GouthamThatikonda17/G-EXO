"""
=========================================================
Project G-EXO Dispatcher
Version : 5.4
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.intent_router import IntentRouter
from core.request import Request
from core.response import Response
from decision.decision_models import DecisionResult
from core.handlers.chat_handler import ChatHandler
from core.handlers.planner_handler import PlannerHandler
from core.handlers.calculator_handler import CalculatorHandler
from core.handlers.local_handler import LocalHandler
from core.handlers.deterministic_handler import DeterministicHandler
from logger import (
    log,
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
            "deterministic": DeterministicHandler(),
        }

    def dispatch(
        self,
        request: Request,
        decision_result: DecisionResult = None,
    ) -> Response:
        try:
            if decision_result:
                log(
                    f"[DECISION] Priority={decision_result.priority.value} | "
                    f"Status={decision_result.status.value} | "
                    f"Confidence={decision_result.confidence} | "
                    f"Reason={decision_result.reason}"
                )
            
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