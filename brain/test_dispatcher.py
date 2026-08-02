"""
=========================================================
Project G-EXO
Dispatcher Test
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.dispatcher import Dispatcher
from core.request import Request


dispatcher = Dispatcher()

while True:

    message = input("You: ")

    if message.lower() == "exit":
        break

    request = Request(
        message=message,
        source="desktop"
    )

    response = dispatcher.dispatch(request)

    print()
    print("Success :", response.success)
    print("Message :", response.message)
    print("Data    :", response.data)
    print()