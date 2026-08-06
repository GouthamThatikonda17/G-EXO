"""
=========================================================
Project G-EXO AI Capability Registry
Version : 4.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from legacy_memory import remember, recall, forget
from legacy_notes import (
    add_note,
    get_notes,
    delete_note,
)
from legacy_tasks import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
)
from tools.apps_tool import open_app

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "memory": {
                "remember": remember,
                "recall": recall,
                "forget": forget,
            },
            "notes": {
                "add": add_note,
                "show": get_notes,
                "delete": delete_note,
            },
            "tasks": {
                "add": add_task,
                "show": get_tasks,
                "complete": complete_task,
                "delete": delete_task,
            },
            "apps": {
                "open": open_app,
            },
        }

    def has_category(self, category):
        return category in self.tools

    def has_tool(self, category, action):
        return (
            self.has_category(category)
            and action in self.tools[category]
        )

    def execute(self, category, action, *args):
        if not self.has_tool(category, action):
            raise ValueError(
                f"Unknown tool: {category}.{action}"
            )
        return self.tools[category][action](*args)

    def list_categories(self):
        return list(self.tools.keys())

    def list_tools(self, category):
        if not self.has_category(category):
            return []
        return list(self.tools[category].keys())