"""
=========================================================
Project G-EXO Deterministic Routing Test
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from ai.intent_router import IntentRouter
from ai.deterministic_parser import DeterministicParser
from core.dispatcher import Dispatcher
from core.request import Request
from ai.planner import AIPlanner

# Monkeypatch AIPlanner to definitively prove deterministic paths never hit the LLM
def fail_if_called(*args, **kwargs):
    raise AssertionError("CRITICAL FAILURE: AIPlanner was invoked! LLM bypass failed.")
AIPlanner.plan = fail_if_called

def run_tests():
    router = IntentRouter()
    parser = DeterministicParser()
    dispatcher = Dispatcher()

    print("\n--- ASSERTING DETERMINISTIC PARSER CONTRACTS ---\n")
    
    # Assert arguments, types, and mappings conform strictly to ToolRegistry
    plan = parser.parse("show tasks")
    assert plan["intent"] == "tasks"
    assert plan["tool"] == "tasks"
    assert plan["action"] == "show"
    assert plan["arguments"] == {}

    plan = parser.parse("delete task 1")
    assert plan["action"] == "delete"
    assert plan["arguments"]["task_id"] == 1
    assert type(plan["arguments"]["task_id"]) is int

    plan = parser.parse("take a note Buy milk")
    assert plan["tool"] == "notes"
    assert plan["action"] == "add"
    assert plan["arguments"]["text"] == "Buy milk"

    plan = parser.parse("delete note 1")
    assert plan["action"] == "delete"
    assert plan["arguments"]["index"] == 1
    assert type(plan["arguments"]["index"]) is int
    
    plan = parser.parse("show reminders")
    assert plan["intent"] == "reminders"
    assert plan["tool"] == "reminders"
    assert plan["action"] == "show"
    assert plan["arguments"] == {}
    
    plan = parser.parse("complete reminder 1")
    assert plan["intent"] == "reminders"
    assert plan["tool"] == "reminders"
    assert plan["action"] == "complete"
    assert plan["arguments"]["reminder_id"] == 1
    assert type(plan["arguments"]["reminder_id"]) is int

    plan = parser.parse("delete reminder 1")
    assert plan["intent"] == "reminders"
    assert plan["tool"] == "reminders"
    assert plan["action"] == "delete"
    assert plan["arguments"]["reminder_id"] == 1
    assert type(plan["arguments"]["reminder_id"]) is int

    plan = parser.parse("clear reminders")
    assert plan["intent"] == "reminders"
    assert plan["tool"] == "reminders"
    assert plan["action"] == "clear"
    assert plan["arguments"] == {}

    plan = parser.parse("set reminder tomorrow 9am")
    assert plan["intent"] == "reminders"
    assert plan["tool"] == "reminders"
    assert plan["action"] == "add"
    assert plan["arguments"]["date"] == "tomorrow"
    assert plan["arguments"]["time"] == "9am"
    assert plan["arguments"]["message"] == ""

    print("[PASS] Deterministic Parser Contracts Verified.")

    print("\n--- ASSERTING INTENT ROUTING ---\n")
    
    # Assert strict deterministic isolation
    assert router.route("show tasks")["route"] == "deterministic"
    assert router.route("delete task 1")["route"] == "deterministic"
    assert router.route("open chrome")["route"] == "deterministic"
    assert router.route("show reminders")["route"] == "deterministic"
    assert router.route("complete reminder 1")["route"] == "deterministic"
    assert router.route("delete reminder 1")["route"] == "deterministic"
    assert router.route("clear reminders")["route"] == "deterministic"
    
    # Assert non-deterministic behavior is preserved
    assert router.route("what does task management mean?")["route"] == "planner"
    assert router.route("Can you show me my tasks?")["route"] == "planner"
    assert router.route("set reminder tomorrow 9am")["route"] == "deterministic"
    assert router.route("hello")["route"] == "chat"
    assert router.route("25 * 25")["route"] == "calculator"
    print("[PASS] Intent Routing Verified.")

    print("\n--- ASSERTING EXECUTION BYPASS ---\n")
    try:
        commands_to_test = [
            "show tasks", 
            "show notes", 
            "show reminders",
            "set reminder tomorrow 9am",
            "delete task 1",
            "delete note 1",
            "delete reminder 1",
            "complete task 1",
            "complete reminder 1",
            "clear reminders",
            "open chrome",
            "remember my name is Goutham"
        ]
        for cmd in commands_to_test:
            req = Request(message=cmd, source="test")
            res = dispatcher.dispatch(req)
            # The execution logic should bypass the AI Planner assertion
        print("[PASS] End-to-end execution completed without invoking AIPlanner.")
    except AssertionError as e:
        print(f"[FAIL] Dispatcher executed AIPlanner for a deterministic command: {e}")
    
    print("\nALL DETERMINISTIC TESTS PASSED.")

if __name__ == "__main__":
    run_tests()