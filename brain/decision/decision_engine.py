"""
=========================================================
Project G-EXO
Decision Engine
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

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

    def decide(
        self,
        request: DecisionRequest,
        context: DecisionContext,
    ) -> DecisionResult:

        priority = self._estimate_priority(request)

        skill = self._select_skill(request.intent)

        action = request.intent

        reason = (
            f"Selected '{skill}' "
            f"for intent '{request.intent}'."
        )

        return DecisionResult(

            success=True,

            skill=skill,

            action=action,

            reason=reason,

            confidence=1.0,

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