"""
=========================================================
Project G-EXO
Tasks Commands Module
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from logger import log

from tasks import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    clear_tasks,
)


def execute(command):

    command = command.strip()

    # =====================================================
    # ADD TODO
    # =====================================================

    if command.lower().startswith("todo "):

        text = command[5:].strip()

        if text:

            add_task(text)

            print("\nTodo added successfully.\n")

            log(f"Todo Added : {text}")

        else:

            print("\nPlease enter a todo.\n")

        return True

    # =====================================================
    # SHOW TODOS
    # =====================================================

    elif command.lower() == "show todos":

        tasks = get_tasks()

        if not tasks:

            print("\nNo todos available.\n")

        else:

            print("\n==================== TODOS ====================\n")

            for task in tasks:

                print(
                    f"[{task['id']}] "
                    f"{task['task']} | "
                    f"{task['status']} | "
                    f"{task['created']}"
                )

            print("\n===============================================\n")

        return True

    # =====================================================
    # COMPLETE TODO
    # =====================================================

    elif command.lower().startswith("complete todo "):

        try:

            task_id = int(command[14:].strip())

            if complete_task(task_id):

                print("\nTodo marked as completed.\n")

                log(f"Todo Completed : {task_id}")

            else:

                print("\nTodo not found.\n")

        except ValueError:

            print("\nUsage: complete todo <number>\n")

        return True

    # =====================================================
    # DELETE TODO
    # =====================================================

    elif command.lower().startswith("delete todo "):

        try:

            task_id = int(command[12:].strip())

            if delete_task(task_id):

                print("\nTodo deleted.\n")

                log(f"Todo Deleted : {task_id}")

            else:

                print("\nTodo not found.\n")

        except ValueError:

            print("\nUsage: delete todo <number>\n")

        return True

    # =====================================================
    # CLEAR TODOS
    # =====================================================

    elif command.lower() == "clear todos":

        clear_tasks()

        print("\nAll todos cleared.\n")

        log("All Todos Cleared")

        return True

    # =====================================================
    # NOT A TASK COMMAND
    # =====================================================

    return None