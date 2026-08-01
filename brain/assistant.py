"""
Project G-EXO
Assistant Module
"""

from commands import execute


class GEXOBrain:

    def greet(self):
        print("System Ready.")
        print("Hello, I am G-EXO.")

    def process_command(self, command):
        return execute(command)