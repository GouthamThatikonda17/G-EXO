"""
=========================================================
Project G-EXO AI Capability Registry
Version : 5.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import inspect
from legacy_memory import remember, recall, forget
from legacy_notes import add_note, get_notes, delete_note, clear_notes
from legacy_tasks import add_task, get_tasks, complete_task, delete_task, clear_tasks
from tools.apps_tool import open_app
from tools.file_tool import (
    create_file, create_folder, delete_file, delete_folder,
    rename, move, copy, read_text, write_text, append_text,
    list_directory, search_by_filename
)
from tools.reminders_tool import (
    add_reminder, show_reminders, complete_reminder, delete_reminder, clear_reminders
)

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
                "clear": clear_notes,
            },
            "tasks": {
                "add": add_task,
                "show": get_tasks,
                "complete": complete_task,
                "delete": delete_task,
                "clear": clear_tasks,
            },
            "reminders": {
                "add": add_reminder,
                "show": show_reminders,
                "complete": complete_reminder,
                "delete": delete_reminder,
                "clear": clear_reminders,
            },
            "apps": {
                "open": open_app,
            },
            "file": {
                "create_file": create_file,
                "create_folder": create_folder,
                "delete_file": delete_file,
                "delete_folder": delete_folder,
                "rename": rename,
                "move": move,
                "copy": copy,
                "read_text": read_text,
                "write_text": write_text,
                "append_text": append_text,
                "list": list_directory,
                "search": search_by_filename,
            },
        }

    def has_category(self, category):
        return category in self.tools

    def has_tool(self, category, action):
        return (
            self.has_category(category)
            and action in self.tools[category]
        )

    def execute(self, category, action, **kwargs):
        if not self.has_tool(category, action):
            raise ValueError(f"Unknown tool: {category}.{action}")

        func = self.tools[category][action]
        sig = inspect.signature(func)

        # 1. Reject Unknown Arguments
        # If the LLM generates an argument name that does not exist in the actual
        # function signature (e.g. "id" instead of "task_id"), immediately reject it.
        # We do not guess or map positional arguments.
        for key in kwargs.keys():
            if key not in sig.parameters:
                raise ValueError(f"Unknown argument '{key}' provided for {category}.{action}.")

        # 2. LEVEL 2: TOOL ARGUMENT CONTRACT VALIDATION
        # Validate that all required parameters are present, non-null, and non-empty.
        for name, param in sig.parameters.items():
            # A parameter is 'required' only if it lacks a default value
            if param.default == inspect.Parameter.empty:
                if name not in kwargs:
                    raise ValueError(f"Missing required argument '{name}' for {category}.{action}.")

                val = kwargs[name]
                if val is None:
                    raise ValueError(f"Argument '{name}' for {category}.{action} cannot be null.")

                if isinstance(val, str) and not val.strip():
                    raise ValueError(f"Argument '{name}' for {category}.{action} cannot be empty.")

        return func(**kwargs)

    def list_categories(self):
        return list(self.tools.keys())

    def list_tools(self, category):
        if not self.has_category(category):
            return []
        return list(self.tools[category].keys())
