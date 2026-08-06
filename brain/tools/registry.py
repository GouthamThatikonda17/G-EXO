"""
=========================================================
Project G-EXO AI Capability Registry
Version : 4.3
Developer : Thatikonda Goutham Teja
=========================================================
"""
import inspect
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
from tools.file_tool import (
    create_file, create_folder, delete_file, delete_folder,
    rename, move, copy, read_text, write_text, append_text,
    list_directory, search_by_filename
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

    def execute(self, category, action, *args, **kwargs):
        if not self.has_tool(category, action):
            raise ValueError(
                f"Unknown tool: {category}.{action}"
            )
            
        func = self.tools[category][action]
        sig = inspect.signature(func)
        
        valid_kwargs = {}
        unused_values = list(args)
        
        # 1. Match explicit kwargs by parameter name safely ignoring AI hallucinations
        for key, value in kwargs.items():
            if key in sig.parameters:
                valid_kwargs[key] = value
            else:
                unused_values.append(value)
                
        # 2. Fill missing required parameters positionally if the AI utilized wrong parameter names
        for name, param in sig.parameters.items():
            if name not in valid_kwargs and param.default == inspect.Parameter.empty:
                if unused_values:
                    valid_kwargs[name] = unused_values.pop(0)
                    
        return func(**valid_kwargs)

    def list_categories(self):
        return list(self.tools.keys())

    def list_tools(self, category):
        if not self.has_category(category):
            return []
        return list(self.tools[category].keys())