"""
=========================================================
Project G-EXO
AI Tool Registry
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from modules.calculator import calculate
from tasks import add_task
from notes import add_note
from memory import remember


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "calculate": calculate,
            "add_task": add_task,
            "add_note": add_note,
            "remember": remember,
        }

    def has_tool(self, name):

        return name in self.tools

    def execute(self, name, *args):

        if not self.has_tool(name):

            raise ValueError(f"Unknown tool: {name}")

        return self.tools[name](*args)

    def list_tools(self):

        return list(self.tools.keys())