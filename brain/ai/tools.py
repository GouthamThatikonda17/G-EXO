"""
=========================================================
Project G-EXO
AI Tools
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from tools.registry import ToolRegistry

registry = ToolRegistry()


def list_categories():

    return registry.list_categories()


def list_tools(category):

    return registry.list_tools(category)


def execute_tool(category, action, *args):

    return registry.execute(category, action, *args)