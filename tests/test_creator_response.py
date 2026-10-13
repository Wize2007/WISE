import os
import tempfile
import unittest
from unittest.mock import patch

from brain.brain import WiseBrain
from brain.memory import WiseMemory


class CreatorResponseTests(unittest.TestCase):
    def test_creator_question_gets_personalized_answer(self):
        with tempfile.TemporaryDirectory() as directory:
            memory_path = os.path.join(directory, "memories.json")
            with patch("brain.brain.WiseMemory", lambda: WiseMemory(memory_path)):
                brain = WiseBrain()

            response = brain.think("Who created you?")
            self.assertIn("Wisdom Nzioka", response)
            self.assertIn("Master Wisdom", response)
            self.assertIn("AI companion", response)


if __name__ == "__main__":
    unittest.main()
