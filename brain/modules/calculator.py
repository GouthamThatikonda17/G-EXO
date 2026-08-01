"""
=========================================================
Project G-EXO
Calculator Module
Version : 0.6
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log


def execute(command):

    command = command.lower().strip()

    if not command.startswith("calculate "):
        return None

    expression = command.replace("calculate ", "", 1)

    try:

        result = eval(expression)

        print(f"\nResult = {result}\n")

        log(f"Calculated: {expression} = {result}")

    except Exception:

        print("\nInvalid mathematical expression.\n")

        log(f"Calculation Error: {expression}")

    return True