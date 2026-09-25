import os


class WiseCharacter:

    def __init__(self):
        self.character_folder = "character"

        self.expressions = {
            "neutral": "neutral/neutral.png",
            "happy": "happy/happy.png",
            "sad": "sad/sad.png",
            "tired": "tired/tired.png",
            "bored": "bored/bored.png"
        }

    def get_image_path(self, expression):
        return os.path.join(
            self.character_folder,
            self.expressions.get(
                expression,
                self.expressions["neutral"]
            )
        )

    def get_expression_path(self, expression):
        path = self.get_image_path(expression)

        if os.path.exists(path):
            return path

        return None