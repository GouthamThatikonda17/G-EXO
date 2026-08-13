"""
=========================================================
Project G-EXO Memory Pipeline Tests
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys

# --- Fix for import path during direct and module execution ---
_brain_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_brain_dir, ".."))

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _brain_dir not in sys.path:
    sys.path.insert(0, _brain_dir)
# --------------------------------------------------------------

import unittest
import dataclasses
from unittest.mock import patch

from assistant import GEXOBrain
from memory.memory_manager import MemoryManager
from memory.working_memory import WorkingMemory
from memory.models import Memory, MemorySnapshot
from memory.memory_types import MemoryType


class TestMemoryPipeline(unittest.TestCase):

    def test_memory_manager_initialization(self):
        """
        TEST 1 â€” MEMORY MANAGER INITIALIZATION
        Verifies GEXOBrain owns a MemoryManager and WorkingMemory starts empty.
        """
        brain = GEXOBrain()

        self.assertIsNotNone(brain.memory_manager)
        self.assertIsInstance(brain.memory_manager, MemoryManager)

        wm = brain.memory_manager.working_memory()
        self.assertIsNotNone(wm)
        self.assertIsInstance(wm, WorkingMemory)

        self.assertTrue(wm.is_empty())
        self.assertEqual(wm.size(), 0)

    def test_request_response_capture(self):
        """
        TEST 2 â€” REQUEST + RESPONSE CAPTURE
        Verifies processing a command accurately populates WorkingMemory with
        exactly one Request and one Response entry.
        """
        brain = GEXOBrain()
        test_source = "test_framework"

        # Execute deterministic command
        response = brain.process("help", source=test_source)
        self.assertTrue(response.success)

        wm = brain.memory_manager.working_memory()

        # Assert exact memory capture volume
        self.assertEqual(wm.size(), 2)

        memories = wm.get_all()
        req_memory: Memory = memories[0]
        res_memory: Memory = memories[1]

        # Validate Request Memory
        self.assertEqual(req_memory.type, MemoryType.CONVERSATION)
        self.assertIn("User Input", req_memory.title)
        self.assertEqual(req_memory.content, "help")
        self.assertEqual(req_memory.source, test_source)

        # Validate Response Memory
        self.assertEqual(res_memory.type, MemoryType.CONVERSATION)
        self.assertEqual(res_memory.title, "G-EXO Response")
        self.assertEqual(res_memory.content, response.message)
        self.assertEqual(res_memory.source, response.source)

    def test_memory_snapshot(self):
        """
        TEST 3 â€” MEMORY SNAPSHOT
        Verifies the snapshot is generated correctly, contains the captured memory,
        and enforces immutability via frozen tuples.
        """
        brain = GEXOBrain()
        brain.process("version", source="test_env")

        snapshot = brain.memory_manager.get_snapshot()

        self.assertIsInstance(snapshot, MemorySnapshot)
        self.assertIsInstance(snapshot.working, tuple)
        self.assertEqual(len(snapshot.working), 2)

        self.assertEqual(snapshot.working[0].content, "version")

        # Prove immutability (frozen dataclass restriction)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            snapshot.working = tuple()

    def test_decision_engine_receives_snapshot(self):
        """
        TEST 4 â€” DECISION ENGINE RECEIVES SNAPSHOT
        Verifies MemorySnapshot successfully traverses the pipeline into the DecisionEngine.
        Uses `wraps` to inspect arguments without breaking the actual pipeline execution.
        """
        brain = GEXOBrain()

        with patch.object(brain.decision_engine, 'decide', wraps=brain.decision_engine.decide) as mock_decide:
            brain.process("developer", source="integration_test")

            mock_decide.assert_called_once()

            _, kwargs = mock_decide.call_args
            self.assertIn("memory_snapshot", kwargs)
            self.assertIsInstance(kwargs["memory_snapshot"], MemorySnapshot)

            # The snapshot evaluated by the decision engine should capture the just-issued request (length 1)
            # Response hasn't been generated yet during decide()
            self.assertEqual(len(kwargs["memory_snapshot"].working), 1)

    def test_deterministic_routing_regression(self):
        """
        TEST 5 â€” DETERMINISTIC ROUTING REGRESSION
        Verifies that memory capture operations do not break or bypass existing deterministic routing.
        """
        brain = GEXOBrain()

        response = brain.process("version", source="regression_test")

        self.assertTrue(response.success)
        self.assertIn("Version", response.message)

        # Assert memory still captured the interaction cleanly
        self.assertEqual(brain.memory_manager.working_memory().size(), 2)


if __name__ == "__main__":
    unittest.main()
