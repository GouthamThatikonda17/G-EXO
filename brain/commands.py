"""
=========================================================
Project G-EXO
Command Router
Version : 0.8
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from modules.calculator import execute as calculator_execute
from modules.memory_commands import execute as memory_execute
from modules.system_commands import execute as system_execute
from modules.app_launcher import execute as app_execute


def execute(command):

    command = command.lower().strip()

    log(f"User Command: {command}")

    result = calculator_execute(command)
    if result is not None:
        return result

    result = memory_execute(command)
    if result is not None:
        return result

    result = system_execute(command)
    if result is not None:
        return result

    result = app_execute(command)
    if result is not None:
        return result

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

APPLICATIONS
------------
open notepad
open calculator
open paint
open cmd
open explorer
open vscode
open chrome

OTHER
-----
help
exit

==================================================
""")

        return True

    if command in ["exit", "quit", "bye"]:

        print("\nGoodbye!\n")

        return False

    log(f"Unknown Command: {command}")

    print("\nUnknown command.\n")

    return True