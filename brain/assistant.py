"""
=========================================================
Project G-EXO
Assistant
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.dispatcher import Dispatcher
from core.request import Request


class GEXOBrain:

    def __init__(self):

        self.dispatcher = Dispatcher()

    def greet(self):

        print("\n========================================")
        print("         G-EXO AI Assistant")
        print("========================================")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.\n")

    def process_command(self, command):

        request = Request(
            message=command,
            source="desktop",
        )

        response = self.dispatcher.dispatch(request)

        if response.message == "exit":

            return False

        print()

        print(response.message)

        print()

        return True