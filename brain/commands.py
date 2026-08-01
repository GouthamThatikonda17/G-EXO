"""
Project G-EXO
Command Module v0.1
"""

import datetime


def execute(command):
    command = command.lower().strip()

    if command == "hello":
        print("\nHello, I am G-EXO.\n")

    elif command == "version":
        print("\nVersion 0.1\n")

    elif command == "developer":
        print("\nDeveloper: Thatikonda Goutham Teja\n")

    elif command == "time":
        now = datetime.datetime.now()
        print("\nCurrent Time:", now.strftime("%I:%M:%S %p"))

    elif command == "date":
        today = datetime.date.today()
        print("\nToday's Date:", today)

    elif command == "help":
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

    elif command == "exit":
        return False

    else:
        print("\nUnknown command.")

    return True