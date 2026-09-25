import random

from brain.memory import WiseMemory
from brain.personality import WisePersonality
from brain.emotion import WiseEmotion
from brain.expression import WiseExpression
from brain.outfit import WiseOutfit
from brain.commands import WiseCommands


class WiseBrain:

    def __init__(self):

        print(
            "I am WISE, your personal AI companion and friend."
        )

        # =========================
        # SHORT-TERM CONVERSATION
        # =========================

        self.conversation_history = []

        # Number of recent messages WISE
        # keeps in short-term memory.

        self.max_conversation_history = 10

        # =========================
        # WISE SYSTEMS
        # =========================

        self.memory = WiseMemory()
        self.personality = WisePersonality()
        self.emotion = WiseEmotion()
        self.expression = WiseExpression()
        self.outfit = WiseOutfit()
        self.commands = WiseCommands()

    # =========================
    # INTRODUCTION
    # =========================

    def introduce(self):

        return self.personality.introduction()

    # =========================
    # EMOTION
    # =========================

    def set_emotion(self, emotion):

        self.emotion.set_emotion(
            emotion
        )

        expression = (
            self.expression.emotion_to_expression(
                emotion
            )
        )

        self.expression.set_expression(
            expression
        )

    # =========================
    # OUTFIT
    # =========================

    def set_outfit(self, outfit):

        self.outfit.set_outfit(
            outfit
        )

    # =========================
    # CURRENT STATE
    # =========================

    def get_state(self):

        return {
            "emotion": self.emotion.get_emotion(),
            "expression": self.expression.get_expression(),
            "outfit": self.outfit.get_outfit()
        }

    # =========================
    # SHORT-TERM MEMORY
    # =========================

    def remember_conversation(
        self,
        speaker,
        message
    ):

        self.conversation_history.append({
            "speaker": speaker,
            "message": message
        })

        # Keep only the most recent
        # conversations.

        if len(
            self.conversation_history
        ) > self.max_conversation_history:

            self.conversation_history.pop(
                0
            )

    # =========================
    # GET RECENT CONVERSATION
    # =========================

    def get_recent_conversation(self):

        return self.conversation_history[-10:]

        # =========================
    # GET PREVIOUS MESSAGE
    # =========================

    def get_previous_message(self):

        if len(
            self.conversation_history
        ) < 2:

            return None

        return self.conversation_history[-2]["message"]

    # =========================
    # THINK
    # =========================

    def think(self, message):

        message = message.lower().strip()

        # =========================
        # REMEMBER USER MESSAGE
        # =========================

        self.remember_conversation(
            "You",
            message
        )

        # =========================
        # RECORDING MODE
        # =========================

        recording_words = [
            "recording",
            "record",
            "recording a video",
            "record a video",
            "recording a presentation",
            "record a presentation",
            "making a video",
            "making a presentation"
        ]

        if any(
            word in message
            for word in recording_words
        ):

            self.set_outfit(
                "recording"
            )

            self.set_emotion(
                "neutral"
            )

            return (
                "Recording mode activated. "
                "I'm ready when you are."
            )

        
                # =========================
        # CONVERSATION CONTEXT
        # =========================

        previous_message = (
            self.get_previous_message()
        )

        print(
            "WISE PREVIOUS MESSAGE:",
            previous_message
        )
        # =========================
        # STUDYING MODE
        # =========================

        studying_words = [
            "studying",
            "study",
            "study for my exam",
            "studying for my exam",
            "doing my homework",
            "doing homework",
            "reading",
            "learning"
        ]

        if any(
            word in message
            for word in studying_words
        ):

            self.set_outfit(
                "studying"
            )

            self.set_emotion(
                "neutral"
            )

            return (
                "Study mode activated. "
                "Let's get to work."
            )

        # =========================
        # GAMING MODE
        # =========================

        gaming_words = [
            "gaming",
            "game",
            "playing games",
            "play games",
            "play a game",
            "playing a game"
        ]

        if any(
            word in message
            for word in gaming_words
        ):

            self.set_outfit(
                "gaming"
            )

            self.set_emotion(
                "happy"
            )

            return (
                "Gaming mode activated. "
                "Let's have some fun."
            )

        # =========================
        # NIGHT MODE
        # =========================

        sleep_words = [
            "going to sleep",
            "go to sleep",
            "time to sleep",
            "bedtime",
            "going to bed"
        ]

        if any(
            word in message
            for word in sleep_words
        ):

            self.set_outfit(
                "night"
            )

            self.set_emotion(
                "tired"
            )

            return (
                "Night mode activated. "
                "Time to relax."
            )

        # =========================
        # RETURN TO NORMAL
        # =========================

        normal_words = [
            "normal outfit",
            "normal mode",
            "casual outfit",
            "change back",
            "go back to normal"
        ]

        if any(
            word in message
            for word in normal_words
        ):

            self.set_outfit(
                "normal"
            )

            self.set_emotion(
                "neutral"
            )

            return (
                "Back to my normal outfit."
            )

        # =========================
        # STATUS
        # =========================

        if (
            "what is your status" in message
            or "show your status" in message
            or "your status" in message
            or message == "status"
        ):

            return self.commands.status(
                self.emotion.get_emotion(),
                self.expression.get_expression(),
                self.outfit.get_outfit()
            )

        # =========================
        # MEMORY
        # =========================

        if (
            "what do you remember" in message
            or "show your memory" in message
            or "what do you know about me" in message
            or "your memory" in message
        ):

            return self.commands.memory_status(
                self.memory.memories
            )

        # =========================
        # TIME
        # =========================

        if (
            "what time is it" in message
            or "what's the time" in message
            or "what is the time" in message
            or "tell me the time" in message
            or "current time" in message
            or message == "time"
        ):

            return self.commands.get_time()

        # =========================
        # DATE
        # =========================

        if (
            "what is today's date" in message
            or "what is the date" in message
            or "what's today's date" in message
            or "tell me today's date" in message
            or "tell me the date" in message
            or "current date" in message
            or message == "date"
        ):

            return self.commands.get_date()

        # =========================
        # HELP
        # =========================

        if (
            message == "help"
            or "what can you do" in message
            or "what can you help me with" in message
            or "show me what you can do" in message
            or "commands" in message
        ):

            return self.commands.help()

        # =========================
        # EMOTION STATUS
        # =========================

        if (
            "what are you feeling" in message
            or "what is your emotion" in message
        ):

            return (
                f"My current state is "
                f"{self.emotion.get_emotion()}."
            )

        # =========================
        # EXPRESSION STATUS
        # =========================

        if (
            "what expression" in message
            or "what are you showing" in message
        ):

            return (
                f"My current expression is "
                f"{self.expression.get_expression()}."
            )

        # =========================
        # OUTFIT STATUS
        # =========================

        if (
            "what are you wearing" in message
            or "what is your outfit" in message
        ):

            return (
                f"My current outfit is "
                f"{self.outfit.get_outfit()}."
            )

        # =========================
        # REMEMBER NAME
        # =========================

        if message.startswith(
            "my name is "
        ):

            name = message.replace(
                "my name is ",
                "",
                1
            ).strip()

            self.memory.remember(
                "name",
                name
            )

            self.set_emotion(
                "happy"
            )

            return (
                f"Nice to meet you, {name}. "
                "I'll remember your name."
            )

        # =========================
        # REMEMBER FAVORITE GAME
        # =========================

        if message.startswith(
            "my favorite game is "
        ):

            game = message.replace(
                "my favorite game is ",
                "",
                1
            ).strip()

            self.memory.remember(
                "favorite_game",
                game
            )

            self.set_emotion(
                "happy"
            )

            return (
                f"Got it. I'll remember that "
                f"your favorite game is {game}."
            )

        # =========================
        # RECALL NAME
        # =========================

        if (
            "what is my name" in message
            or "do you know my name" in message
        ):

            name = self.memory.recall(
                "name"
            )

            if name:

                return (
                    f"Your name is {name}."
                )

            return (
                "You haven't told me your name yet."
            )

        # =========================
        # RECALL FAVORITE GAME
        # =========================

        if (
            "what is my favorite game"
            in message
        ):

            game = self.memory.recall(
                "favorite_game"
            )

            if game:

                return (
                    f"Your favorite game is "
                    f"{game}."
                )

            return (
                "You haven't told me "
                "your favorite game yet."
            )

        # =========================
        # NATURAL GREETINGS
        # =========================

        greeting_words = [
            "hello",
            "hi",
            "hey",
            "hey wise",
            "hello wise",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if any(
            word in message
            for word in greeting_words
        ):

            self.set_emotion(
                "happy"
            )

            greetings = [
                "Hey! It's good to hear from you.",
                "Hello! I'm glad you're here.",
                "Hey there! WISE is ready.",
                "Hello! How are you doing?",
                "Hey! What are we working on today?"
            ]

            return random.choice(
                greetings
            )

        # =========================
        # HOW ARE YOU
        # =========================

        if "how are you" in message:

            self.set_emotion(
                "happy"
            )

            responses = [
                "I'm doing great! My brain is getting stronger every step of the way.",
                "I'm doing well! I'm happy to be here with you.",
                "I'm great and ready to help with whatever you're working on.",
                "I'm doing good! WISE is online and ready."
            ]

            return random.choice(
                responses
            )

        # =========================
        # USER FEELS GOOD
        # =========================

        positive_words = [
            "i'm good",
            "im good",
            "i am good",
            "i'm great",
            "im great",
            "i am great",
            "i'm fine",
            "im fine",
            "i am fine",
            "i'm okay",
            "im okay",
            "i am okay",
            "i'm alright",
            "im alright",
            "i am alright"
        ]

        if any(
            phrase in message
            for phrase in positive_words
        ):

            self.set_emotion(
                "happy"
            )

            responses = [
                "That's great to hear! I'm glad you're doing well.",
                "Awesome! I'm happy you're feeling good.",
                "That's good to hear. What shall we work on today?",
                "Nice! I'm glad things are going well."
            ]

            return random.choice(
                responses
            )

        # =========================
        # USER FEELS NOT GOOD
        # =========================

        negative_words = [
            "i'm not good",
            "im not good",
            "i am not good",
            "i'm not okay",
            "im not okay",
            "i am not okay",
            "i'm not fine",
            "im not fine",
            "i am not fine"
        ]

        if any(
            phrase in message
            for phrase in negative_words
        ):

            self.set_emotion(
                "sad"
            )

            responses = [
                "I'm sorry you're having a rough time. I'm here to listen.",
                "I'm sorry to hear that. We can take things one step at a time.",
                "That doesn't sound easy. I'm here if you'd like to talk about it.",
                "I'm sorry you're not feeling okay. Let's take things slowly."
            ]

            return random.choice(
                responses
            )

        # =========================
        # HAPPY
        # =========================

        if (
            "happy" in message
            or "excited" in message
        ):

            self.set_emotion(
                "happy"
            )

            responses = [
                "That's awesome! I love the positive energy.",
                "Nice! I'm happy you're feeling excited.",
                "That's great! Let's make the most of it."
            ]

            return random.choice(
                responses
            )

        # =========================
        # TIRED
        # =========================

        if (
            "tired" in message
            or "sleepy" in message
        ):

            self.set_emotion(
                "tired"
            )

            return (
                self.personality.tired_response()
            )

        # =========================
        # SAD
        # =========================

        if (
            "sad" in message
            or "upset" in message
        ):

            self.set_emotion(
                "sad"
            )

            return (
                self.personality.sad_response()
            )

        # =========================
        # BORED
        # =========================

        if "bored" in message:

            self.set_emotion(
                "bored"
            )

            return (
                "Hmm... sounds like you're bored. "
                "Maybe we should do something fun."
            )

        # =========================
        # IDENTITY
        # =========================

        if (
            "your name" in message
            or "who are you" in message
        ):

            self.set_emotion(
                "neutral"
            )

            return (
                self.personality.introduction()
            )

        # =========================
        # GOODBYE
        # =========================

        if (
            "bye" in message
            or "goodbye" in message
        ):

            self.set_emotion(
                "neutral"
            )

            return (
                self.personality.goodbye()
            )

                # =========================
        # CONTEXTUAL CONVERSATION
        # =========================

        if previous_message:

            # =========================
            # DIFFICULT / HARD
            # =========================

            difficult_words = [
                "difficult",
                "hard",
                "challenging",
                "confusing",
                "complicated"
            ]

            if any(
                word in message
                for word in difficult_words
            ):

                if (
                    "study" in previous_message
                    or "studying" in previous_message
                    or "exam" in previous_message
                    or "learning" in previous_message
                    or "physics" in previous_message
                    or "math" in previous_message
                    or "mathematics" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. "
                        "That can be challenging. "
                        "Let's break it down into smaller "
                        "parts and work through it together."
                    )

            # =========================
            # FUN / AMAZING
            # =========================

            positive_context_words = [
                "fun",
                "amazing",
                "awesome",
                "great",
                "cool",
                "enjoying",
                "enjoy"
            ]

            if any(
                word in message
                for word in positive_context_words
            ):

                if (
                    "game" in previous_message
                    or "gaming" in previous_message
                    or "playing" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "That's awesome! "
                        "Sounds like you're having fun. "
                        "Enjoy yourself!"
                    )

            # =========================
            # USER AGREEMENT
            # =========================

            agreement_words = [
                "yes",
                "yeah",
                "yep",
                "exactly",
                "true",
                "correct",
                "that's right"
            ]

            if message in agreement_words:

                self.set_emotion(
                    "happy"
                )

                return (
                    "Exactly! I'm with you. "
                    "What should we tackle next?"
                )

            # =========================
            # USER DISAGREEMENT
            # =========================

            disagreement_words = [
                "no",
                "nope",
                "not really",
                "that's wrong",
                "not exactly"
            ]

            if message in disagreement_words:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "Got it. Thanks for correcting me. "
                    "Let's try another approach."
                )

            # =========================
            # REQUEST FOR HELP
            # =========================

            help_phrases = [
                "help me",
                "can you help",
                "help please",
                "i need help",
                "could you help me",
                "please help"
            ]

            if any(
                phrase in message
                for phrase in help_phrases
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # =========================
            # SHORT FOLLOW-UP
            # =========================

            if len(message.split()) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )

                # =========================
        # CONTEXTUAL CONVERSATION
        # =========================

        if previous_message:

            # =========================
            # DIFFICULT / HARD
            # =========================

            difficult_words = [
                "difficult",
                "hard",
                "challenging",
                "confusing",
                "complicated"
            ]

            if any(
                word in message
                for word in difficult_words
            ):

                if (
                    "study" in previous_message
                    or "studying" in previous_message
                    or "exam" in previous_message
                    or "learning" in previous_message
                    or "physics" in previous_message
                    or "math" in previous_message
                    or "mathematics" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. "
                        "That can be challenging. "
                        "Let's break it down into smaller "
                        "parts and work through it together."
                    )

            # =========================
            # FUN / AMAZING
            # =========================

            positive_context_words = [
                "fun",
                "amazing",
                "awesome",
                "great",
                "cool",
                "enjoying",
                "enjoy"
            ]

            if any(
                word in message
                for word in positive_context_words
            ):

                if (
                    "game" in previous_message
                    or "gaming" in previous_message
                    or "playing" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "That's awesome! "
                        "Sounds like you're having fun. "
                        "Enjoy yourself!"
                    )

            # =========================
            # USER AGREEMENT
            # =========================

            agreement_words = [
                "yes",
                "yeah",
                "yep",
                "exactly",
                "true",
                "correct",
                "that's right"
            ]

            if message in agreement_words:

                self.set_emotion(
                    "happy"
                )

                return (
                    "Exactly! I'm with you. "
                    "What should we tackle next?"
                )

            # =========================
            # USER DISAGREEMENT
            # =========================

            disagreement_words = [
                "no",
                "nope",
                "not really",
                "that's wrong",
                "not exactly"
            ]

            if message in disagreement_words:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "Got it. Thanks for correcting me. "
                    "Let's try another approach."
                )

            # =========================
            # REQUEST FOR HELP
            # =========================

            help_phrases = [
                "help me",
                "can you help",
                "help please",
                "i need help",
                "could you help me",
                "please help"
            ]

            if any(
                phrase in message
                for phrase in help_phrases
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # =========================
            # SHORT FOLLOW-UP
            # =========================

            if len(message.split()) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )
        # =========================
        # CONTEXTUAL CONVERSATION
        # =========================

        if previous_message:

            # =========================
            # DIFFICULT / HARD
            # =========================

            difficult_words = [
                "difficult",
                "hard",
                "challenging",
                "confusing",
                "complicated"
            ]

            if any(
                word in message
                for word in difficult_words
            ):

                if (
                    "study" in previous_message
                    or "studying" in previous_message
                    or "exam" in previous_message
                    or "learning" in previous_message
                    or "physics" in previous_message
                    or "math" in previous_message
                    or "mathematics" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. "
                        "That can be challenging. "
                        "Let's break it down into smaller "
                        "parts and work through it together."
                    )

            # =========================
            # FUN / AMAZING
            # =========================

            positive_context_words = [
                "fun",
                "amazing",
                "awesome",
                "great",
                "cool",
                "enjoying",
                "enjoy"
            ]

            if any(
                word in message
                for word in positive_context_words
            ):

                if (
                    "game" in previous_message
                    or "gaming" in previous_message
                    or "playing" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "That's awesome! "
                        "Sounds like you're having fun. "
                        "Enjoy yourself!"
                    )

            # =========================
            # USER AGREEMENT
            # =========================

            agreement_words = [
                "yes",
                "yeah",
                "yep",
                "exactly",
                "true",
                "correct",
                "that's right"
            ]

            if message in agreement_words:

                self.set_emotion(
                    "happy"
                )

                return (
                    "Exactly! I'm with you. "
                    "What should we tackle next?"
                )

            # =========================
            # USER DISAGREEMENT
            # =========================

            disagreement_words = [
                "no",
                "nope",
                "not really",
                "that's wrong",
                "not exactly"
            ]

            if message in disagreement_words:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "Got it. Thanks for correcting me. "
                    "Let's try another approach."
                )

            # =========================
            # REQUEST FOR HELP
            # =========================

            help_phrases = [
                "help me",
                "can you help",
                "help please",
                "i need help",
                "could you help me",
                "please help"
            ]

            if any(
                phrase in message
                for phrase in help_phrases
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # =========================
            # SHORT FOLLOW-UP
            # =========================

            if len(message.split()) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )

        # =========================
        # CONTEXTUAL CONVERSATION
        # =========================

        if previous_message:

            # =========================
            # DIFFICULT / HARD
            # =========================

            difficult_words = [
                "difficult",
                "hard",
                "challenging",
                "confusing",
                "complicated"
            ]

            if any(
                word in message
                for word in difficult_words
            ):

                if (
                    "study" in previous_message
                    or "studying" in previous_message
                    or "exam" in previous_message
                    or "learning" in previous_message
                    or "physics" in previous_message
                    or "math" in previous_message
                    or "mathematics" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. "
                        "That can be challenging. "
                        "Let's break it down into smaller "
                        "parts and work through it together."
                    )

            # =========================
            # FUN / AMAZING
            # =========================

            positive_context_words = [
                "fun",
                "amazing",
                "awesome",
                "great",
                "cool",
                "enjoying",
                "enjoy"
            ]

            if any(
                word in message
                for word in positive_context_words
            ):

                if (
                    "game" in previous_message
                    or "gaming" in previous_message
                    or "playing" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "That's awesome! "
                        "Sounds like you're having fun. "
                        "Enjoy yourself!"
                    )

            # =========================
            # USER AGREEMENT
            # =========================

            agreement_words = [
                "yes",
                "yeah",
                "yep",
                "exactly",
                "true",
                "correct",
                "that's right"
            ]

            if message in agreement_words:

                self.set_emotion(
                    "happy"
                )

                return (
                    "Exactly! I'm with you. "
                    "What should we tackle next?"
                )

            # =========================
            # USER DISAGREEMENT
            # =========================

            disagreement_words = [
                "no",
                "nope",
                "not really",
                "that's wrong",
                "not exactly"
            ]

            if message in disagreement_words:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "Got it. Thanks for correcting me. "
                    "Let's try another approach."
                )

            # =========================
            # REQUEST FOR HELP
            # =========================

            help_phrases = [
                "help me",
                "can you help",
                "help please",
                "i need help",
                "could you help me",
                "please help"
            ]

            if any(
                phrase in message
                for phrase in help_phrases
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # =========================
            # SHORT FOLLOW-UP
            # =========================

            if len(message.split()) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )

         # =========================
        # CONTEXTUAL CONVERSATION
        # =========================

        if previous_message:

            # =========================
            # DIFFICULT / HARD
            # =========================

            difficult_words = [
                "difficult",
                "hard",
                "challenging",
                "confusing",
                "complicated"
            ]

            if any(
                word in message
                for word in difficult_words
            ):

                if (
                    "study" in previous_message
                    or "studying" in previous_message
                    or "exam" in previous_message
                    or "learning" in previous_message
                    or "physics" in previous_message
                    or "math" in previous_message
                    or "mathematics" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. "
                        "That can be challenging. "
                        "Let's break it down into smaller "
                        "parts and work through it together."
                    )

            # =========================
            # FUN / AMAZING
            # =========================

            positive_context_words = [
                "fun",
                "amazing",
                "awesome",
                "great",
                "cool",
                "enjoying",
                "enjoy"
            ]

            if any(
                word in message
                for word in positive_context_words
            ):

                if (
                    "game" in previous_message
                    or "gaming" in previous_message
                    or "playing" in previous_message
                ):

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "That's awesome! "
                        "Sounds like you're having fun. "
                        "Enjoy yourself!"
                    )

            # =========================
            # USER AGREEMENT
            # =========================

            agreement_words = [
                "yes",
                "yeah",
                "yep",
                "exactly",
                "true",
                "correct",
                "that's right"
            ]

            if message in agreement_words:

                self.set_emotion(
                    "happy"
                )

                return (
                    "Exactly! I'm with you. "
                    "What should we tackle next?"
                )

            # =========================
            # USER DISAGREEMENT
            # =========================

            disagreement_words = [
                "no",
                "nope",
                "not really",
                "that's wrong",
                "not exactly"
            ]

            if message in disagreement_words:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "Got it. Thanks for correcting me. "
                    "Let's try another approach."
                )

            # =========================
            # REQUEST FOR HELP
            # =========================

            help_phrases = [
                "help me",
                "can you help",
                "help please",
                "i need help",
                "could you help me",
                "please help"
            ]

            if any(
                phrase in message
                for phrase in help_phrases
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # =========================
            # SHORT FOLLOW-UP
            # =========================

            if len(message.split()) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )

        # =========================
        # UNKNOWN MESSAGE
        # =========================

        self.set_emotion(
            "neutral"
        )

        return (
            self.personality.unknown_response()
        )