class WiseEmotion:

    def __init__(self):
        self.current_emotion = "neutral"

    def set_emotion(self, emotion):
        allowed_emotions = [
            "neutral",
            "happy",
            "sad",
            "tired",
            "bored"
        ]

        if emotion in allowed_emotions:
            self.current_emotion = emotion
        else:
            self.current_emotion = "neutral"

    def get_emotion(self):
        return self.current_emotion

    def reset(self):
        self.current_emotion = "neutral"