import unittest

from brain.emotion import WiseEmotion
from brain.expression import WiseExpression
from brain.outfit import WiseOutfit


class WiseStateModuleTests(unittest.TestCase):
    def test_emotion_rejects_unknown_values(self):
        emotion = WiseEmotion()
        emotion.set_emotion("happy")
        self.assertEqual(emotion.get_emotion(), "happy")
        emotion.set_emotion("unknown")
        self.assertEqual(emotion.get_emotion(), "neutral")

    def test_expression_maps_known_and_unknown_emotions(self):
        expression = WiseExpression()
        self.assertEqual(expression.emotion_to_expression("sad"), "sad")
        self.assertEqual(expression.emotion_to_expression("unknown"), "neutral")

    def test_outfit_can_be_changed_and_read(self):
        outfit = WiseOutfit()
        self.assertEqual(outfit.get_outfit(), "normal")
        outfit.set_outfit("studying")
        self.assertEqual(outfit.get_outfit(), "studying")


if __name__ == "__main__":
    unittest.main()
