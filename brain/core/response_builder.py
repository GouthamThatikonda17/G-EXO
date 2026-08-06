"""
=========================================================
Project G-EXO Response Builder
Version : 1.4
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
            
            if action == "remember":
                return Response(
                    success=True,
                    message=f"  I'll remember that your {key.replace('_', ' ')} is {value}.",
                    data=result,
                )
            elif action == "recall":
                if result:
                    return Response(
                        success=True,
                        message=f"  {result}",
                        data=result,
                    )
                return Response(
                    success=False,
                    message=f"  I don't remember anything about {key.replace('_', ' ')}.",
                    data=result,
                )
            elif action == "forget":
                if result:
                    return Response(
                        success=True,
                        message=f"  I have forgotten about {key.replace('_', ' ')}.",
                        data=result,
                    )
                return Response(
                    success=False,
                    message=f"  I don't have any memory of {key.replace('_', ' ')}.",
                    data=result,
                )
            
            return Response(
                success=True,
                message="  Memory action completed.",
                data=result,
            )

        # =====================================================
        # TEMPORARY COMPATIBILITY: LEGACY NOTES
        # =====================================================
        if intent == "notes":
            if action == "add":
                return Response(
                    success=True,
                    message="  Note added successfully.",
                    data=result,
                )
            elif action == "show":
                if isinstance(result, list) and result:
                    formatted = "\n".join(f"  {i+1}. {note}" for i, note in enumerate(result))
                    return Response(
                        success=True,
                        message=f"  Here are your notes:\n{formatted}",
                        data=result,
                    )
                return Response(
                    success=True,
                    message="  You have no notes.",
                    data=result,
                )
            elif action == "delete":
                if result:
                    return Response(
                        success=True,
                        message="  Note deleted successfully.",
                        data=result,
                    )
                return Response(
                    success=False,
                    message="  Failed to delete note. Invalid index.",
                    data=result,
                )

            return Response(
                success=True,
                message="  Notes action completed.",
                data=result,
            )

        # =====================================================
        # TEMPORARY COMPATIBILITY: LEGACY TASKS
        # =====================================================
        if intent == "tasks":
            if action == "add":
                return Response(
                    success=True,
                    message="  Task added successfully.",
                    data=result,
                )
            elif action == "show":
                if isinstance(result, list) and result:
                    formatted = "\n".join(
                        f"  {t.get('id', '?')}. [{t.get('status', 'Pending')}] {t.get('task', '')}" 
                        for t in result
                    )
                    return Response(
                        success=True,
                        message=f"  Here are your tasks:\n{formatted}",
                        data=result,
                    )
                return Response(
                    success=True,
                    message="  You have no tasks.",
                    data=result,
                )
            elif action == "complete":
                if result:
                    return Response(
                        success=True,
                        message="  Task marked as completed.",
                        data=result,
                    )
                return Response(
                    success=False,
                    message="  Failed to complete task.",
                    data=result,
                )
            elif action == "delete":
                if result:
                    return Response(
                        success=True,
                        message="  Task deleted successfully.",
                        data=result,
                    )
                return Response(
                    success=False,
                    message="  Failed to delete task.",
                    data=result,
                )

            return Response(
                success=True,
                message="  Task action completed.",
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