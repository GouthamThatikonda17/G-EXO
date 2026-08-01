"""
=========================================================
Project G-EXO
Calculator Module
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log


def calculate(expression):

    try:

        result = eval(expression)

        log(f"Calculated: {expression} = {result}")

        return result

    except Exception:

        return None


def execute(command):

    command = command.lower().strip()

    if not command.startswith("calculate "):
        return None

    expression = command.replace("calculate ", "", 1)

    result = calculate(expression)

    if result is None:

        print("\nInvalid mathematical expression.\n")

    else:

        print(f"\nResult = {result}\n")

    return True