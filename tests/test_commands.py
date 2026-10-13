import unittest

from brain.commands import WiseCommands


class WiseCommandsTests(unittest.TestCase):
    def test_help_lists_supported_basics(self):
        help_text = WiseCommands().help()
        self.assertIn("What time is it?", help_text)
        self.assertIn("What do you remember?", help_text)

    def test_memory_status_handles_empty_and_existing_memories(self):
        commands = WiseCommands()
        self.assertIn("empty", commands.memory_status({}).lower())
        self.assertIn("favorite_game: chess", commands.memory_status({
            "favorite_game": "chess",
        }))


if __name__ == "__main__":
    unittest.main()
