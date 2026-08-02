"""
=========================================================
Project G-EXO
Response Builder
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.response import Response


class ResponseBuilder:

    @staticmethod
    def build(plan: dict, result=None) -> Response:

        intent = plan.get("intent")
        tool = plan.get("tool")
        action = plan.get("action")
        arguments = plan.get("arguments", {})

        # =====================================================
        # MEMORY
        # =====================================================

        if intent == "memory":

            key = arguments.get("key", "")
            value = arguments.get("value", "")

            return Response(
                success=True,
                message=f"✅ I'll remember that your {key.replace('_', ' ')} is {value}.",
                data=result,
            )

        # =====================================================
        # NOTES
        # =====================================================

        if intent == "notes":

            return Response(
                success=True,
                message="📝 Note added successfully.",
                data=result,
            )

        # =====================================================
        # TASKS
        # =====================================================

        if intent == "tasks":

            return Response(
                success=True,
                message="✅ Task added successfully.",
                data=result,
            )

        # =====================================================
        # CHAT
        # =====================================================

        if intent == "chat":

            return Response(
                success=True,
                message=str(result),
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        return Response(
            success=True,
            message="Done.",
            data=result,
        )