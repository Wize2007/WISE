from datetime import datetime


class WiseCommands:

    def get_time(self):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    def get_date(self):
        current_date = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {current_date}."

    def help(self):
        return (
            "Here are some things you can ask me:\n"
            "- What is my name?\n"
            "- What is my favorite game?\n"
            "- What time is it?\n"
            "- What is today's date?\n"
            "- What are you feeling?\n"
            "- What expression are you showing?\n"
            "- What do you remember?"
        )

    def status(self, emotion, expression, outfit=None):
        result = (
            f"WISE status:\n"
            f"Emotion: {emotion}\n"
            f"Expression: {expression}"
        )

        if outfit is not None:
            result += f"\nOutfit: {outfit}"

        return result

    def memory_status(self, memories):
        if not memories:
            return "My memory is currently empty."

        result = "Here is what I remember:\n"

        for key, value in memories.items():
            result += f"- {key}: {value}\n"

        return result
