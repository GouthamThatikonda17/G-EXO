"""
Project G-EXO
Assistant Module
"""

from commands import execute
from logger import log


class GEXOBrain:

    def greet(self):
        print("System Ready.")
        print("Hello, I am G-EXO.")
        log("G-EXO Started")

    def process_command(self, command):
        log(f"User Command: {command}")

        running = execute(command)

        if not running:
            log("G-EXO Shutdown")

        return running