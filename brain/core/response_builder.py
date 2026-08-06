# brain/core/response_builder.py
"""
=========================================================
Project G-EXO Response Builder
Version : 1.3
Developer : Thatikonda Goutham Teja
=========================================================
"""
from core.response import Response
from tools.models import ToolResult

class ResponseBuilder:
    @staticmethod
    def build(plan: dict, result=None) -> Response:
        intent = plan.get("intent")
        tool = plan.get("tool")
        action = plan.get("action")
        arguments = plan.get("arguments", {})

        # =====================================================
        # MODERN TOOL RESULT (MIGRATION IN PROGRESS)
        # =====================================================
        # Standardized payload for modern tools (e.g., File Tool, Apps Tool).
        if isinstance(result, ToolResult):
            return Response(
                success=result.success,
                message=result.message,
                data=result.data,
            )

        # =====================================================
        # TEMPORARY COMPATIBILITY: LEGACY MEMORY
        # =====================================================
        if intent == "memory":
            key = arguments.get("key", "")
            value = arguments.get("value", "")
            return Response(
                success=True,
                message=f"  I'll remember that your {key.replace('_', ' ')} is {value}.",
                data=result,
            )

        # =====================================================
        # TEMPORARY COMPATIBILITY: LEGACY NOTES
        # =====================================================
        if intent == "notes":
            return Response(
                success=True,
                message="  Note added successfully.",
                data=result,
            )

        # =====================================================
        # TEMPORARY COMPATIBILITY: LEGACY TASKS
        # =====================================================
        if intent == "tasks":
            return Response(
                success=True,
                message="  Task added successfully.",
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