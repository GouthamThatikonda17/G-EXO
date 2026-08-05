"""
=========================================================
Project G-EXO Chat Handler
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.ai_service import AIService
from core.response import Response


class ChatHandler:
    def __init__(self):
        self.ai = AIService()

    def handle(self, request):
        reply = self.ai.generate(request.message)
        return Response(
            success=True,
            message=reply,
            data=None,
        )