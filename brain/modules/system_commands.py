"""
Project G-EXO
System Commands Module
"""

import datetime
import platform
import psutil


def execute(command):

    command = command.lower().strip()

    # ---------------- HELLO ----------------

    if command in ["hello", "hi", "hey"]:
        print("\nHello, I am G-EXO.\n")
        return True

    # ---------------- VERSION ----------------

    elif command == "version":
        print("\nVersion 0.2\n")
        return True

    # ---------------- DEVELOPER ----------------

    elif command in [
        "developer",
        "creator",
        "who made you",
        "your developer",
    ]:
        print("\nDeveloper : Thatikonda Goutham Teja\n")
        return True

    # ---------------- TIME ----------------

    elif command == "time":
        now = datetime.datetime.now()
        print(f"\nCurrent Time : {now.strftime('%I:%M:%S %p')}\n")
        return True

    # ---------------- DATE ----------------

    elif command == "date":
        today = datetime.date.today()
        print(f"\nToday's Date : {today}\n")
        return True

    # ---------------- CPU ----------------

    elif command == "cpu":
        print(f"\nCPU Usage : {psutil.cpu_percent(interval=1)} %\n")
        return True

    # ---------------- RAM ----------------

    elif command == "ram":
        ram = psutil.virtual_memory()
        print(f"\nRAM Usage : {ram.percent} %")
        print(f"Available : {round(ram.available / (1024**3), 2)} GB\n")
        return True

    # ---------------- DISK ----------------

    elif command == "disk":
        disk = psutil.disk_usage("/")
        print(f"\nDisk Usage : {disk.percent} %")
        print(f"Free Space : {round(disk.free / (1024**3), 2)} GB\n")
        return True

    # ---------------- BATTERY ----------------

    elif command == "battery":

        battery = psutil.sensors_battery()

        if battery:
            print(f"\nBattery : {battery.percent}%")
            print(f"Charging : {battery.power_plugged}\n")
        else:
            print("\nBattery information unavailable.\n")

        return True

    # ---------------- SYSTEM ----------------

    elif command == "system":

        print("\n========== SYSTEM INFO ==========")
        print(f"OS         : {platform.system()} {platform.release()}")
        print(f"Machine    : {platform.machine()}")
        print(f"Processor  : {platform.processor()}")
        print(f"Python     : {platform.python_version()}")
        print("=================================\n")

        return True

    return None