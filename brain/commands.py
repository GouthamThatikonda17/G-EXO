"""
Project G-EXO
Command Module v0.3
"""

import datetime
from memory import remember, recall, forget, show_memory


def execute(command):

    command = command.lower().strip()

    # ---------------- MEMORY ----------------

    if command.startswith("remember "):

        text = command.replace("remember ", "", 1)

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

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
            print("\nMemory deleted.\n")
        else:
            print("\nI don't remember that.\n")

        return True

    elif command == "memory":

        memory = show_memory()

        if not memory:
            print("\nMemory is empty.\n")
        else:
            print("\nStored Memories\n---------------")
            for key, value in memory.items():
                print(f"{key} : {value}")
            print()

        return True

    # ---------------- NORMAL COMMANDS ----------------

    if command in ["hello", "hi", "hey"]:
        print("\nHello, I am G-EXO.\n")

    elif command == "version":
        print("\nVersion 0.3\n")

    elif command in ["developer", "creator", "who made you"]:
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

remember <key> is <value>
what is <key>
forget <key>
memory

help
exit
""")

    elif command in ["exit", "quit", "bye"]:

        print("\nGoodbye.")
        return False

    else:

        print("\nUnknown command.")

    return True