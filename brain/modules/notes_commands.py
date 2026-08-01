"""
=========================================================
Project G-EXO
Notes Commands Module
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from notes import (
    add_note,
    get_notes,
    delete_note,
    clear_notes,
)


def execute(command):

    command = command.strip()

    # =====================================================
    # ADD NOTE
    # =====================================================

    if command.lower().startswith("note "):

        text = command[5:].strip()

        if text:

            add_note(text)

            print("\nNote added successfully.\n")

            log(f"Note Added : {text}")

        else:

            print("\nPlease enter a note.\n")

        return True

    # =====================================================
    # SHOW NOTES
    # =====================================================

    elif command.lower() == "show notes":

        notes = get_notes()

        if not notes:

            print("\nNo notes available.\n")

        else:

            print("\n========== NOTES ==========\n")

            for i, note in enumerate(notes, start=1):

                print(f"{i}. {note}")

            print("\n===========================\n")

        return True

    # =====================================================
    # DELETE NOTE
    # =====================================================

    elif command.lower().startswith("delete note "):

        try:

            index = int(command[12:].strip()) - 1

            if delete_note(index):

                print("\nNote deleted successfully.\n")

                log(f"Note Deleted : {index + 1}")

            else:

                print("\nInvalid note number.\n")

        except ValueError:

            print("\nUsage: delete note <number>\n")

        return True

    # =====================================================
    # CLEAR NOTES
    # =====================================================

    elif command.lower() == "clear notes":

        clear_notes()

        print("\nAll notes cleared.\n")

        log("All Notes Cleared")

        return True

    # =====================================================
    # NOT A NOTES COMMAND
    # =====================================================

    return None