"""
=========================================================
Project G-EXO
Calculator Tool
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import ast
import operator


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):

        return node.value

    if isinstance(node, ast.BinOp):

        left = _evaluate(node.left)

        right = _evaluate(node.right)

        operation = _ALLOWED_OPERATORS.get(type(node.op))

        if operation is None:

            raise ValueError("Unsupported operator.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = _evaluate(node.operand)

        if isinstance(node.op, ast.USub):

            return -value

        if isinstance(node.op, ast.UAdd):

            return value

    raise ValueError("Invalid expression.")


def calculate(expression: str):

    expression = expression.strip()

    tree = ast.parse(expression, mode="eval")

    return _evaluate(tree.body)