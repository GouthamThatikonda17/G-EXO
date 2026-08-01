"""
Calculator Module
Project G-EXO
"""

from logger import log


def calculate(command):

    expression = command.replace("calculate ", "", 1)

    try:

        result = eval(expression)

        print(f"\nResult = {result}\n")

        log(f"Calculated: {expression} = {result}")

    except Exception:

        print("\nInvalid mathematical expression.\n")

        log(f"Calculation Error: {expression}")

    return True