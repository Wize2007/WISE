class WiseExpression:

    def __init__(self):
        self.current_expression = "neutral"

    def set_expression(self, expression):
        self.current_expression = expression

    def get_expression(self):
        return self.current_expression

    def emotion_to_expression(self, emotion):
        expression_map = {
            "happy": "happy",
            "sad": "sad",
            "tired": "tired",
            "bored": "bored",
            "neutral": "neutral"
        }

        return expression_map.get(emotion, "neutral")