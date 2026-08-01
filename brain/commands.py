"""
=========================================================
Project G-EXO
Command Module
Version : 0.3
Developer : Thatikonda Goutham Teja
=========================================================
"""

import datetime
from memory import remember, recall


def execute(command):

    command = command.lower().strip()

    # =====================================================
    # MEMORY COMMANDS
    # =====================================================

    if command.startswith("remember "):

        text = command.replace("remember ", "", 1)

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            print("\n✅ Got it! I'll remember that.\n")

        else:

            print("\nUsage:")
            print("remember <something> is <value>\n")

        return True

    elif command.startswith("what is "):

        key = command.replace("what is ", "", 1)

        value = recall(key.strip())

        if value:

            print(f"\n📌 {key.title()} : {value}\n")

        else:

            print("\n❌ I don't know that yet.\n")

        return True

    # =====================================================
    # GREETING
    # =====================================================

    elif (
        command == "hello"
        or "hello" in command
        or "hi" in command
        or "hey" in command
    ):

        print("\nHello! I am G-EXO.")
        print("How can I help you?\n")

    # =====================================================
    # VERSION
    # =====================================================

    elif (
        command == "version"
        or "version" in command
    ):

        print("\nG-EXO Brain Version : 0.3\n")

    # =====================================================
    # DEVELOPER
    # =====================================================

    elif (
        command == "developer"
        or "who made you" in command
        or "creator" in command
        or "your developer" in command
    ):

        print("\nDeveloper : Thatikonda Goutham Teja\n")

    # =====================================================
    # TIME
    # =====================================================

    elif (
        command == "time"
        or "time" in command
        or "clock" in command
    ):

        now = datetime.datetime.now()

        print("\nCurrent Time :", now.strftime("%I:%M:%S %p"))
        print()

    # =====================================================
    # DATE
    # =====================================================

    elif (
        command == "date"
        or "date" in command
        or "today" in command
    ):

        today = datetime.date.today()

        print("\nToday's Date :", today)
        print()

    # =====================================================
    # HELP
    # =====================================================

    elif (
        command == "help"
        or "commands" in command
    ):

        print("""
================ AVAILABLE COMMANDS ================

hello
version
developer
time
date

remember <something> is <value>

what is <something>

help

exit

====================================================
""")

    # =====================================================
    # EXIT
    # =====================================================

    elif command in [
        "exit",
        "quit",
        "bye",
        "goodbye"
    ]:

        print("\nGoodbye!")
        print("Shutting down G-EXO...\n")

        return False

    # =====================================================
    # UNKNOWN COMMAND
    # =====================================================

    else:

        print("\n❌ Unknown Command.")
        print("Type 'help' to see available commands.\n")

    return True