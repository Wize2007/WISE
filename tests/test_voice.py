import threading
import time
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

    def test_speech_requests_are_serialized(self):
        active = 0
        maximum_active = 0
        state_lock = threading.Lock()

        def fake_speech(text, on_start=None, on_finish=None):
            nonlocal active, maximum_active
            with state_lock:
                active += 1
                maximum_active = max(maximum_active, active)
            time.sleep(0.03)
            with state_lock:
                active -= 1

        self.voice._speak_unlocked = fake_speech
        threads = [
            threading.Thread(target=self.voice._speak, args=(text,))
            for text in ("first", "second")
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=2)

        self.assertTrue(all(not thread.is_alive() for thread in threads))
        self.assertEqual(maximum_active, 1)


if __name__ == "__main__":
    unittest.main()
