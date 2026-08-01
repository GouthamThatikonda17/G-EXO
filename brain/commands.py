"""
=========================================================
Project G-EXO
Command Router
Version : 0.6
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from modules.calculator import calculate
from modules.memory_commands import execute as memory_execute
from modules.system_commands import execute as system_execute


def execute(command):

    command = command.lower().strip()

    log(f"User Command: {command}")

    # =====================================================
    # CALCULATOR
    # =====================================================

    if command.startswith("calculate "):
        return calculate(command)

    # =====================================================
    # MEMORY MODULE
    # =====================================================

    result = memory_execute(command)

    if result is not None:
        return result

    # =====================================================
    # SYSTEM MODULE
    # =====================================================

    result = system_execute(command)

    if result is not None:
        return result

    # =====================================================
    # HELP
    # =====================================================

    if command == "help":

        print("""
==================================================
                    G-EXO HELP
==================================================

SYSTEM
------
hello
version
developer
time
date
cpu
ram
disk
battery
system

CALCULATOR
----------
calculate <expression>

MEMORY
------
remember <key> is <value>
what is <key>
forget <key>
memory

OTHER
-----
help
exit

==================================================
""")

        return True

    # =====================================================
    # EXIT
    # =====================================================

    if command in ["exit", "quit", "bye"]:

        print("\nGoodbye!\n")

        return False

    # =====================================================
    # UNKNOWN
    # =====================================================

    log(f"Unknown Command: {command}")

    print("\nUnknown command.\n")

    return True