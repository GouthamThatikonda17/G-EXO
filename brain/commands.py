"""
=========================================================
Project G-EXO
Command Module
Version : 0.5
Developer : Thatikonda Goutham Teja
=========================================================
"""

import datetime

from memory import remember, recall, forget, show_memory
from logger import log


def execute(command):

    command = command.lower().strip()

    log(f"User Command: {command}")

    # =====================================================
    # CALCULATOR
    # =====================================================

    if command.startswith("calculate "):

        expression = command.replace("calculate ", "", 1)

        try:

            result = eval(expression)

            print(f"\nResult = {result}\n")

            log(f"Calculated: {expression} = {result}")

        except Exception:

            print("\nInvalid mathematical expression.\n")

            log(f"Calculation Error: {expression}")

        return True

    # =====================================================
    # MEMORY
    # =====================================================

    elif command.startswith("remember "):

        text = command.replace("remember ", "", 1)

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            log(f"Memory Saved: {key.strip()} = {value.strip()}")

            print(f"\nOkay! I'll remember that {key.strip()} is {value.strip()}.\n")

        else:

            print("\nUsage:\nremember <key> is <value>\n")

        return True

    elif command.startswith("what is "):

        key = command.replace("what is ", "", 1)

        value = recall(key.strip())

        if value:

            print(f"\n{key.title()} = {value}\n")

        else:

            print("\nI don't know that yet.\n")

        return True

    elif command.startswith("forget "):

        key = command.replace("forget ", "", 1)

        if forget(key.strip()):

            log(f"Memory Deleted: {key.strip()}")

            print("\nMemory deleted.\n")

        else:

            print("\nI don't remember that.\n")

        return True

    elif command == "memory":

        memory = show_memory()

        if not memory:

            print("\nMemory is empty.\n")

        else:

            print("\nStored Memories")
            print("----------------")

            for key, value in memory.items():

                print(f"{key} : {value}")

            print()

        return True

    # =====================================================
    # GREETING
    # =====================================================

    elif command in ["hello", "hi", "hey"]:

        print("\nHello, I am G-EXO.\n")

    # =====================================================
    # VERSION
    # =====================================================

    elif command == "version":

        print("\nG-EXO Version 0.5\n")

    # =====================================================
    # DEVELOPER
    # =====================================================

    elif command in ["developer", "creator", "who made you"]:

        print("\nDeveloper: Thatikonda Goutham Teja\n")

    # =====================================================
    # TIME
    # =====================================================

    elif command == "time":

        now = datetime.datetime.now()

        print("\nCurrent Time:", now.strftime("%I:%M:%S %p"))

    # =====================================================
    # DATE
    # =====================================================

    elif command == "date":

        today = datetime.date.today()

        print("\nToday's Date:", today)

    # =====================================================
    # HELP
    # =====================================================

    elif command == "help":

        print("""
==================== COMMANDS ====================

hello
version
developer
time
date

calculate <expression>

remember <key> is <value>
what is <key>
forget <key>
memory

help
exit

==================================================
""")

    # =====================================================
    # EXIT
    # =====================================================

    elif command in ["exit", "quit", "bye"]:

        print("\nGoodbye!\n")

        return False

    # =====================================================
    # UNKNOWN
    # =====================================================

    else:

        log(f"Unknown Command: {command}")

        print("\nUnknown command.\n")

    return True