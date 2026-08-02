"""
=========================================================
Project G-EXO
Planner Test
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.planner import AIPlanner


planner = AIPlanner()

while True:

    message = input("You: ")

    if message.lower() == "exit":
        break

    plan = planner.plan(message)

    print()
    print(plan)
    print()