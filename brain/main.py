from assistant import GEXOBrain


def main():

    assistant = GEXOBrain()

    assistant.greet()

    while True:

        command = input("You: ")

        if not assistant.process_command(command):
            break


if __name__ == "__main__":
    main()