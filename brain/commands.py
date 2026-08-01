"""
=========================================================
Project G-EXO
Command Router
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from modules.calculator import execute as calculator_execute
from modules.memory_commands import execute as memory_execute
from modules.system_commands import execute as system_execute
from modules.app_launcher import execute as app_execute
from modules.web_commands import execute as web_execute
from modules.file_manager import execute as file_execute
from modules.notes_commands import execute as notes_execute


# =====================================================
# MODULE REGISTRY
# =====================================================

MODULES = [
    calculator_execute,
    memory_execute,
    system_execute,
    app_execute,
    web_execute,
    file_execute,
    notes_execute,
]


def execute(command):

    command = command.lower().strip()

    log(f"User Command: {command}")

    # =====================================================
    # SEND COMMAND TO MODULES
    # =====================================================

    for module in MODULES:

        result = module(command)

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

APPLICATIONS
------------
open notepad
open calculator
open paint
open explorer
open vscode
open chrome

WEB
---
open youtube
open github
open gmail
open chatgpt
open google
search <anything>

FILE MANAGER
------------
pwd
list files
create folder <name>
delete folder <name>
change directory <folder>

NOTES
-----
note <text>
show notes
delete note <number>
clear notes

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
    # UNKNOWN COMMAND
    # =====================================================

    log(f"Unknown Command: {command}")

    print("\nUnknown command.\n")

    return True