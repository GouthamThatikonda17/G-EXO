"""
=========================================================
Project G-EXO
Application Launcher Module
Version : 0.8
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
import subprocess

from logger import log


def execute(command):

    command = command.lower().strip()

    if not command.startswith("open "):
        return None

    app = command.replace("open ", "", 1)

    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe",
        "vscode": "code",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    }

    if app not in apps:
        return None

    try:

        print(f"\nOpening {app.title()}...\n")

        log(f"Opening Application : {app}")

        if app == "chrome":

            if os.path.exists(apps[app]):
                subprocess.Popen(apps[app])
            else:
                print("Chrome not found.")
                log("Chrome executable not found.")

        else:

            subprocess.Popen(apps[app])

    except Exception as e:

        print(f"\nUnable to open {app}.\n")

        log(f"Application Error : {e}")

    return True