"""
=========================================================
Project G-EXO
Assistant
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from commands import execute
from ai.router import AIRouter


class GEXOBrain:

    def __init__(self):

        self.ai = AIRouter()

    def greet(self):

        print("\n========================================")
        print("         G-EXO AI Assistant")
        print("========================================")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.\n")

    def process_command(self, command):

        result = execute(command)

        # Local command executed
        if result is not None:

            return result

        # Unknown command → Ask Gemini
        print()

        response = self.ai.chat(command)

        print(response)
        print()

        return True