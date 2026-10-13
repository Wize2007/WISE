import unittest
from unittest.mock import patch

from brain.star import WiseStar


def bare_star():
    star = object.__new__(WiseStar)
    star.state = "idle"
    star.emotion = "neutral"
    star._closing = False
    star.environment = {"scene": "night"}
    star._last_scene = "night"
    star._target_scene = "night"
    star._transition_start = None
    star._transition_duration = 2.5
    return star


class WiseStarStateTests(unittest.TestCase):
    def test_invalid_state_and_emotion_fall_back_safely(self):
        star = bare_star()
        star.set_state("not-a-state")
        star.set_emotion("not-an-emotion")
        self.assertEqual(star.state, "idle")
        self.assertEqual(star.emotion, "neutral")

    def test_unknown_environment_scene_is_ignored(self):
        star = bare_star()
        star.set_environment({"scene": "underwater", "temperature": 22})
        self.assertEqual(star.environment["scene"], "night")
        self.assertEqual(star._target_scene, "night")
        self.assertEqual(star.environment["temperature"], 22)

    def test_known_environment_scene_starts_transition(self):
        star = bare_star()
        with patch.object(star, "_clock_seconds", return_value=123.0):
            star.set_environment({"scene": "sunset"})
        self.assertEqual(star._target_scene, "sunset")
        self.assertEqual(star._last_scene, "night")
        self.assertEqual(star._transition_start, 123.0)


if __name__ == "__main__":
    unittest.main()
