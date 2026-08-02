"""
=========================================================
Project G-EXO
Chat Handler
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.gemini import GeminiProvider
from core.response import Response


class ChatHandler:

    def __init__(self):

        self.ai = GeminiProvider()

    def handle(self, request):

        reply = self.ai.generate(request.message)

        return Response(
            success=True,
            message=reply,
            data=None,
        )