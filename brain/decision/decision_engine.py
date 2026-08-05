"""
=========================================================
Project G-EXO Decision Engine
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.request import Request
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
    - Construct DecisionContext
    - Produce DecisionResult without fake skill selection
    """
     
    def decide(
        self,
        request: Request,
    ) -> DecisionResult:
        decision_request = DecisionRequest(
            user_input=request.message,
            intent="unknown",
            source=request.source,
            timestamp=request.timestamp,
        )
        context = DecisionContext(
            user_input=request.message,
            source=request.source,
            user_id=request.user,
            conversation_id=request.session_id,
            timestamp=request.timestamp,
        )
        priority = self._estimate_priority(decision_request)
        reason = "Evaluated request priority and metadata context."
        return DecisionResult(
            success=True,
            skill=None,
            action=None,
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