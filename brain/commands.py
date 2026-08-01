"""
Project G-EXO
Command Module v0.2
"""

import datetime


def execute(command):
    command = command.lower().strip()

    # Greeting
    if (
        command == "hello"
        or "hello" in command
        or "hi" in command
        or "hey" in command
    ):
        print("\nHello, I am G-EXO.\n")

    # Version
    elif (
        command == "version"
        or "version" in command
    ):
        print("\nVersion 0.2\n")

    # Developer
    elif (
        command == "developer"
        or "who made you" in command
        or "creator" in command
        or "your developer" in command
    ):
        print("\nDeveloper: Thatikonda Goutham Teja\n")

    # Time
    elif (
        command == "time"
        or "time" in command
        or "clock" in command
    ):
        now = datetime.datetime.now()
        print("\nCurrent Time:", now.strftime("%I:%M:%S %p"))

    # Date
    elif (
        command == "date"
        or "date" in command
        or "today" in command
    ):
        today = datetime.date.today()
        print("\nToday's Date:", today)

    # Help
    elif (
        command == "help"
        or "commands" in command
    ):
        print("""
Available Commands
------------------
hello
version
developer
time
date
help
exit
""")

    # Exit
    elif command in ["exit", "quit", "bye", "goodbye"]:
        print("\nGoodbye.")
        return False

    # Unknown
    else:
        print("\nUnknown command.")

    return True