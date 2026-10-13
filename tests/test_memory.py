import json
import os
import tempfile
import unittest

from brain.memory import WiseMemory


class WiseMemoryTests(unittest.TestCase):
    def test_round_trip_persists_without_touching_project_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "memories.json")
            memory = WiseMemory(path)
            memory.remember("favorite_game", "chess")

            reloaded = WiseMemory(path)
            self.assertEqual(reloaded.recall("favorite_game"), "chess")
            self.assertEqual(reloaded.get_all_memories(), {"favorite_game": "chess"})

    def test_unreadable_json_is_preserved_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "memories.json")
            original = '{"favorite_game": '
            with open(path, "w", encoding="utf-8") as file:
                file.write(original)

            memory = WiseMemory(path)
            self.assertEqual(memory.get_all_memories(), {})
            with self.assertRaises(OSError):
                memory.remember("favorite_game", "chess")

            with open(path, "r", encoding="utf-8") as file:
                self.assertEqual(file.read(), original)

    def test_non_object_json_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "memories.json")
            original = json.dumps(["not", "a", "memory", "object"])
            with open(path, "w", encoding="utf-8") as file:
                file.write(original)

            memory = WiseMemory(path)
            with self.assertRaises(OSError):
                memory.clear_memory()

            with open(path, "r", encoding="utf-8") as file:
                self.assertEqual(file.read(), original)

    def test_forget_returns_false_for_missing_key(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = WiseMemory(os.path.join(directory, "memories.json"))
            self.assertFalse(memory.forget("missing"))


if __name__ == "__main__":
    unittest.main()
