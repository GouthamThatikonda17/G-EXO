# brain/decision/decision_engine.py
"""
=========================================================
Project G-EXO Decision Engine
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.request import Request
from ai.intent_router import IntentRouter
from memory.models import MemorySnapshot
from decision.decision_context import DecisionContext
from decision.decision_models import (
    DecisionPriority,
    DecisionRequest,
    DecisionResult,
    DecisionStatus,
)

class DecisionEngine:
    """
    The central reasoning component of G-EXO.
    Responsibilities
    ----------------
    - Analyze requests
    - Estimate priority
    - Choose a skill
    - Explain the decision

    Future versions will integrate:
        - Memory
        - Emotion
        - Personality
        - Knowledge
        - Vision
        - Voice
    """
    def __init__(self):
        self.router = IntentRouter()

    def decide(
        self,
        request: Request,
        memory_snapshot: MemorySnapshot,
    ) -> DecisionResult:
        # =====================================================
        # INTENT EVALUATION
        # =====================================================
        # Preserving existing behavior by utilizing the intent router
        route_data = self.router.route(request.message)
        intent = route_data.get("route", "unknown")

        # =====================================================
        # CONSTRUCT INTERNAL REQUEST
        # =====================================================
        decision_request = DecisionRequest(
            user_input=request.message,
            intent=intent,
            source=request.source,
        )

        # =====================================================
        # CONSTRUCT CONTEXT
        # =====================================================
        # NOTE: DecisionContext construction securely packages the memory state.
        # This serves as intentional preparation work for future reasoning.
        # In upcoming sprints, this context will be evaluated directly against
        # system rules to adjust execution paths and LLM prompts.
        context = DecisionContext(
            user_input=decision_request.user_input,
            source=decision_request.source,
            working_memory=list(memory_snapshot.working),
            short_memory=list(memory_snapshot.short),
            long_memory=list(memory_snapshot.long),
        )

        # =====================================================
        # EVALUATE
        # =====================================================
        priority = self._estimate_priority(decision_request)
        skill = self._select_skill(decision_request.intent)
        action = "evaluate"  # Action is kept strictly independent from intent
        reason = (
            f"Selected '{skill}' "
            f"for intent '{decision_request.intent}'."
        )

        # TODO: Adjust confidence based on `context` memory states in future sprints
        confidence = 1.0

        return DecisionResult(
            success=True,
            skill=skill,
            action=action,
            reason=reason,
            confidence=confidence,
            priority=priority,
            status=DecisionStatus.COMPLETED,
        )

    # =====================================================
    # PRIORITY
    # =====================================================
    def _estimate_priority(
        self,
        request: DecisionRequest,
    ) -> DecisionPriority:
        text = request.user_input.lower()
        emergency_keywords = (
            "help",
            "emergency",
            "accident",
            "hospital",
            "heart",
            "ambulance",
        )
        if any(
            keyword in text
            for keyword in emergency_keywords
        ):
            return DecisionPriority.CRITICAL

        return DecisionPriority.NORMAL

    # =====================================================
    # SKILL
    # =====================================================
    def _select_skill(
        self,
        intent: str,
    ) -> str:
        return intent