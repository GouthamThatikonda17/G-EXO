"""
====================================================
Project G-EXO
Brain Module v0.1
====================================================
"""

VERSION = "0.1"


class GEXOBrain:

    def __init__(self):
        self.modules = {
            "Brain": True,
            "Voice": False,
            "Vision": False,
            "Memory": False,
            "Hardware": False,
        }

    def boot(self):

        print("=" * 55)
        print("              PROJECT G-EXO")
        print(f"              Brain Version {VERSION}")
        print("=" * 55)

        print("\nBooting System...\n")

        for module, status in self.modules.items():

            state = "ONLINE" if status else "OFFLINE"

            print(f"{module:<12} : {state}")

        print("\nSystem Ready.")
        print("Welcome to G-EXO.\n")


def main():

    brain = GEXOBrain()

    brain.boot()


if __name__ == "__main__":
    main()