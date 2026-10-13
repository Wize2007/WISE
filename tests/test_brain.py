import os
import tempfile
import unittest
from unittest.mock import patch

from brain.brain import WiseBrain
from brain.memory import WiseMemory


class WiseBrainTests(unittest.TestCase):
    def make_brain(self, directory):
        memory_path = os.path.join(directory, "memories.json")
        with patch("brain.brain.WiseMemory", lambda: WiseMemory(memory_path)):
            return WiseBrain()

    def test_brain_initializes_and_introduces_itself(self):
        with tempfile.TemporaryDirectory() as directory:
            brain = self.make_brain(directory)
            self.assertTrue(brain.introduce().strip())
            self.assertIn("emotion", brain.get_state())

    def test_status_command_returns_state_without_external_services(self):
        with tempfile.TemporaryDirectory() as directory:
            brain = self.make_brain(directory)
            response = brain.think("status")
            self.assertIn("WISE status", response)
            self.assertIn("Emotion:", response)


if __name__ == "__main__":
    unittest.main()
