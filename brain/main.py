"""
=========================================================
Project G-EXO CLI / Main Entry Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from runtime.application import Application


def main():
    app_root = Application()
    brain = app_root.brain
    print("[G-EXO] Brain Initialized via Application Composition Root.")
    
    while True:
        try:
            command = input("You: ")
            if not command:
                continue
            if command.lower() in ["exit", "quit", "bye"]:
                print("\nGoodbye!\n")
                break
            response = brain.process(command, source="cli")
            print()
            print(response.message)
            print()
        except KeyboardInterrupt:
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()