# brain/assistant.py
"""
=========================================================
Project G-EXO Brain
Version : 4.4
Developer : Thatikonda Goutham Teja
=========================================================
"""

import uuid
from behavior.behavior_engine import BehaviorEngine
from core.dispatcher import Dispatcher
from core.request import Request
from core.response import Response
from memory.memory_manager import MemoryManager
from memory.models import Memory
from memory.memory_types import MemoryType
from decision.decision_engine import DecisionEngine
from logger import log



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
        self.memory_manager = MemoryManager()
        self.decision_engine = DecisionEngine()
        self.behavior = BehaviorEngine()
    # =====================================================
    # MEMORY HELPERS
    # =====================================================
    def _create_request_memory(self, request: Request) -> Memory:
        """Helper to create a Memory instance from a user Request."""
        return Memory(
            id=str(uuid.uuid4()),
            type=MemoryType.CONVERSATION,
            title=f"User Input ({request.source})",
            content=request.message,
            importance=1,
            source=request.source,
        )

    def _create_response_memory(self, response: Response) -> Memory:
        """Helper to create a Memory instance from an assistant Response."""
        return Memory(
            id=str(uuid.uuid4()),
            type=MemoryType.CONVERSATION,
            title="G-EXO Response",
            content=response.message,
            importance=1,
            source=response.source,
        )

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

        # 1. Record User Request to Memory Engine
        req_memory = self._create_request_memory(request)
        self.memory_manager.working_memory().add(req_memory)

        # 2. Extract Immutable Memory Snapshot
        memory_snapshot = self.memory_manager.get_snapshot()

        # 3. Decision Engine evaluation
        decision = self.decision_engine.decide(
            request=request,
            memory_snapshot=memory_snapshot,
        )

        # Consume the decision result (Logging it since the existing
        # Dispatcher API does not currently accept the DecisionResult)
        log(
            f"[Brain] Decision Evaluated: Skill={decision.skill}, "
            f"Action={decision.action}, Priority={decision.priority.value}"
        )

        # 4. Dispatch Request through existing core Pipeline
        response = self.dispatcher.dispatch(
            request,
            decision,
        )

        # 5. Record Assistant Response to Memory Engine
        res_memory = self._create_response_memory(response)
        self.memory_manager.working_memory().add(res_memory)

        return response