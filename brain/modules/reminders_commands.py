"""
=========================================================
Project G-EXO
Reminder Commands Module
Version : 1.3
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from reminders import (
    add_reminder,
    get_reminders,
    delete_reminder,
    clear_reminders,
)


def execute(command):

    command = command.strip()

    # =====================================================
    # ADD REMINDER
    # =====================================================

    if command.lower().startswith("reminder add "):

        text = command[13:].strip()

        parts = text.split(" ", 2)

        if len(parts) != 3:

            print(
                "\nUsage:\n"
                "reminder add YYYY-MM-DD HH:MM Your reminder\n"
            )

            return True

        date, time, message = parts

        add_reminder(date, time, message)

        print("\nReminder added successfully.\n")

        log(f"Reminder Added : {date} {time} | {message}")

        return True

    # =====================================================
    # SHOW REMINDERS
    # =====================================================

    elif command.lower() == "show reminders":

        reminders = get_reminders()

        if not reminders:

            print("\nNo reminders found.\n")

        else:

            print("\n=============== REMINDERS ===============\n")

            for reminder in reminders:

                print(
                    f"[{reminder['id']}] "
                    f"{reminder['date']} "
                    f"{reminder['time']}  |  "
                    f"{reminder['message']}"
                )

            print("\n=========================================\n")

        return True

    # =====================================================
    # DELETE REMINDER
    # =====================================================

    elif command.lower().startswith("delete reminder "):

        try:

            reminder_id = int(command[18:].strip())

            if delete_reminder(reminder_id):

                print("\nReminder deleted.\n")

                log(f"Reminder Deleted : {reminder_id}")

            else:

                print("\nReminder not found.\n")

        except ValueError:

            print("\nUsage: delete reminder <number>\n")

        return True

    # =====================================================
    # CLEAR REMINDERS
    # =====================================================

    elif command.lower() == "clear reminders":

        clear_reminders()

        print("\nAll reminders cleared.\n")

        log("All Reminders Cleared")

        return True

    # =====================================================
    # NOT A REMINDER COMMAND
    # =====================================================

    return None