"""
=========================================================
Project G-EXO
Local Handler
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_DEVELOPER,
)

from core.response import Response


HELP_TEXT = """
==================================================
                    G-EXO HELP
==================================================

SYSTEM
------
hello
version
developer
time
date
cpu
ram
disk
battery
system

CALCULATOR
----------
12 + 25
100 / 5
7 * 8

MEMORY
------
Remember my favorite color is black
What is my favorite color?
Forget my favorite color

NOTES
-----
Take a note Buy milk
Show notes

TASKS
-----
Add task Complete G-EXO
Show tasks

OTHER
-----
help
version
developer
exit

==================================================
"""


class LocalHandler:

    def __init__(self):

        pass

    def handle(self, request):

        command = request.message.lower().strip()

        if command == "help":

            return Response(
                success=True,
                message=HELP_TEXT,
            )

        if command == "version":

            return Response(
                success=True,
                message=f"{PROJECT_NAME} Version {PROJECT_VERSION}",
            )

        if command == "developer":

            return Response(
                success=True,
                message=PROJECT_DEVELOPER,
            )

        if command == "exit":

            return Response(
                success=True,
                message="exit",
            )

        return Response(
            success=False,
            message="Unknown local command.",
        )