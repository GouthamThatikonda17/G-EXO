"""
=========================================================
Project G-EXO
File Manager Module
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os

from logger import log

# Current working directory for G-EXO
current_directory = os.getcwd()


def execute(command):

    global current_directory

    command = command.lower().strip()

    # =====================================================
    # PWD
    # =====================================================

    if command == "pwd":

        print(f"\nCurrent Directory:\n{current_directory}\n")

        log(f"PWD : {current_directory}")

        return True

    # =====================================================
    # LIST FILES
    # =====================================================

    elif command == "list files":

        try:

            items = os.listdir(current_directory)

            print("\n========== FILES ==========\n")

            if not items:
                print("Folder is empty.")

            for item in items:
                print(item)

            print()

            log("Listed Files")

        except Exception as e:

            print(f"\nError : {e}\n")

            log(f"List Files Error : {e}")

        return True

    # =====================================================
    # CREATE FOLDER
    # =====================================================

    elif command.startswith("create folder "):

        folder = command.replace("create folder ", "", 1)

        path = os.path.join(current_directory, folder)

        try:

            os.makedirs(path)

            print(f"\nFolder '{folder}' created.\n")

            log(f"Folder Created : {path}")

        except FileExistsError:

            print("\nFolder already exists.\n")

        except Exception as e:

            print(f"\nError : {e}\n")

        return True

    # =====================================================
    # DELETE FOLDER
    # =====================================================

    elif command.startswith("delete folder "):

        folder = command.replace("delete folder ", "", 1)

        path = os.path.join(current_directory, folder)

        try:

            os.rmdir(path)

            print(f"\nFolder '{folder}' deleted.\n")

            log(f"Folder Deleted : {path}")

        except FileNotFoundError:

            print("\nFolder not found.\n")

        except OSError:

            print("\nFolder is not empty.\n")

        except Exception as e:

            print(f"\nError : {e}\n")

        return True

    # =====================================================
    # CHANGE DIRECTORY
    # =====================================================

    elif command.startswith("change directory "):

        folder = command.replace("change directory ", "", 1)

        new_path = os.path.join(current_directory, folder)

        if os.path.isdir(new_path):

            current_directory = new_path

            print(f"\nDirectory changed to:\n{current_directory}\n")

            log(f"Directory Changed : {current_directory}")

        else:

            print("\nDirectory not found.\n")

        return True

    # =====================================================
    # NOT A FILE COMMAND
    # =====================================================

    return None