import unittest

from brain.voice import WiseVoice


class WiseVoiceTextTests(unittest.TestCase):
    def setUp(self):
        self.voice = WiseVoice()

    def test_speech_preprocessing_keeps_words_and_numbers(self):
        text = self.voice._prepare_text("WISE version 2 is ready.")
        self.assertIn("WISE", text)
        self.assertIn("version 2", text)
        self.assertIn("ready", text)

    def test_speech_preprocessing_removes_emoji_without_removing_text(self):
        text = self.voice._prepare_text("Hello 😀, WISE!")
        self.assertNotIn("😀", text)
        self.assertIn("Hello", text)
        self.assertIn("WISE", text)

    def test_empty_text_stays_empty(self):
        self.assertEqual(self.voice._prepare_text("   😀   "), "")


if __name__ == "__main__":
    unittest.main()
