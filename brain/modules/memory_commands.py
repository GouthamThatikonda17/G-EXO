"""
=========================================================
Project G-EXO
Memory Commands Module
Version : 0.6
Developer : Thatikonda Goutham Teja
=========================================================
"""

from memory import remember, recall, forget, show_memory
from logger import log


def execute(command):

    command = command.lower().strip()

    # =====================================================
    # REMEMBER
    # =====================================================

    if command.startswith("remember "):

        text = command.replace("remember ", "", 1)

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            log(f"Memory Saved: {key.strip()} = {value.strip()}")

            print(f"\n✅ Okay! I'll remember that {key.strip()} is {value.strip()}.\n")

        else:

            print("\nUsage:")
            print("remember <key> is <value>\n")

        return True

    # =====================================================
    # RECALL
    # =====================================================

    elif command.startswith("what is "):

        key = command.replace("what is ", "", 1)

        value = recall(key.strip())

        if value:

            print(f"\n📌 {key.title()} = {value}\n")

        else:

            print("\n❌ I don't know that yet.\n")

        return True

    # =====================================================
    # FORGET
    # =====================================================

    elif command.startswith("forget "):

        key = command.replace("forget ", "", 1)

        if forget(key.strip()):

            log(f"Memory Deleted: {key.strip()}")

            print("\n🗑 Memory deleted.\n")

        else:

            print("\n❌ I don't remember that.\n")

        return True

    # =====================================================
    # SHOW MEMORY
    # =====================================================

    elif command == "memory":

        memory = show_memory()

        if not memory:

            print("\nMemory is empty.\n")

        else:

            print("\n========== MEMORY ==========\n")

            for key, value in memory.items():

                print(f"{key} : {value}")

            print()

        return True

    # =====================================================
    # NOT A MEMORY COMMAND
    # =====================================================

    return None