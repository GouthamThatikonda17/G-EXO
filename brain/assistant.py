"""
=========================================================
Project G-EXO Brain
Version : 4.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.dispatcher import Dispatcher
from core.request import Request
from core.response import Response
from behavior.behavior_engine import BehaviorEngine
from decision.decision_engine import DecisionEngine


class GEXOBrain:
    """
    Main entry point of G-EXO Brain.
    Every interface communicates with this class.
    Examples:
        - Desktop
        - Mobile
        - Robot
        - Voice
        - API
    """

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.behavior = BehaviorEngine()
        self.decision_engine = DecisionEngine()

    # =====================================================
    # PROCESS
    # =====================================================
    def process(
        self,
        message: str,
        source: str = "desktop",
    ) -> Response:
        request = Request(
            message=message,
            source=source,
        )
        decision_result = self.decision_engine.decide(request)
        return self.dispatcher.dispatch(request, decision_result)