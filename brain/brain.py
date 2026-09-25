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
    # CONVERSATION STATUS
    # =========================

    def conversation_status(self):

        if not self.conversation_history:

            return (
                "I don't have any conversation "
                "history yet."
            )

        lines = [
            "Here is our recent conversation:"
        ]

        for item in self.conversation_history:

            speaker = item["speaker"]
            message = item["message"]

            lines.append(
                f"{speaker}: {message}"
            )

        return "\n".join(lines)

    # =========================
    # GET PREVIOUS USER MESSAGE
    # =========================

    def get_previous_message(self):

        if len(
            self.conversation_history
        ) < 2:

            return None

        return self.conversation_history[-2]["message"]

    # =========================
    # DETECT CONVERSATION TOPIC
    # =========================

    def get_conversation_topic(self):

        if not self.conversation_history:

            return None

        recent_messages = [
            item["message"]
            for item in reversed(
                self.conversation_history[-6:]
            )
        ]

        for message in recent_messages:

            # -------------------------
            # GAMING
            # -------------------------

            if any(
                word in message
                for word in [
                    "game",
                    "gaming",
                    "playing",
                    "play",
                    "little nightmares",
                    "e football"
                ]
            ):

                return "gaming"

            # -------------------------
            # STUDYING
            # -------------------------

            if any(
                word in message
                for word in [
                    "study",
                    "studying",
                    "exam",
                    "homework",
                    "learning",
                    "physics",
                    "math",
                    "mathematics"
                ]
            ):

                return "studying"

            # -------------------------
            # PROGRAMMING
            # -------------------------

            if any(
                word in message
                for word in [
                    "python",
                    "programming",
                    "coding",
                    "code",
                    "program",
                    "software"
                ]
            ):

                return "programming"

            # -------------------------
            # RECORDING
            # -------------------------

            if any(
                word in message
                for word in [
                    "recording",
                    "record",
                    "video",
                    "presentation"
                ]
            ):

                return "recording"

            # -------------------------
            # SLEEP
            # -------------------------

            if any(
                word in message
                for word in [
                    "sleep",
                    "sleeping",
                    "bedtime",
                    "tired",
                    "sleepy"
                ]
            ):

                return "sleep"

        return None

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
        # PREVIOUS MESSAGE
        # =========================

        previous_message = (
            self.get_previous_message()
        )

        print(
            "WISE PREVIOUS MESSAGE:",
            previous_message
        )

        # =========================
        # CONVERSATION TOPIC
        # =========================

        conversation_topic = (
            self.get_conversation_topic()
        )

        print(
            "WISE CONVERSATION TOPIC:",
            conversation_topic
        )

        # =========================
        # CURRENT LONG-TERM MEMORIES
        # =========================

        memories = self.memory.get_all_memories()

        favorite_game = memories.get(
            "favorite_game"
        )

        favorite_subject = memories.get(
            "favorite_subject"
        )

        favorite_color = memories.get(
            "favorite color"
        )

        current_game = memories.get(
            "current_game"
        )

        # ==================================================
        # RECORDING MODE
        # ==================================================

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

            return random.choice([
                "Recording mode activated. Let's make something great.",
                "Alright, recording mode is ready.",
                "Recording mode activated. I'm ready when you are."
            ])

        # ==================================================
        # MEMORY-AWARE GAMING CONVERSATION
        # ==================================================

        if favorite_game:

            game_words = [
                "play something",
                "play a game",
                "want to play",
                "feel like playing",
                "gaming",
                "play games"
            ]

            if any(
                word in message
                for word in game_words
            ):

                self.set_outfit(
                    "gaming"
                )

                self.set_emotion(
                    "happy"
                )

                return (
                    f"Sounds good! Since I remember "
                    f"that you like {favorite_game}, "
                    f"we could play that."
                )

        # ==================================================
        # MEMORY-AWARE STUDY CONVERSATION
        # ==================================================

        if favorite_subject:

            study_words = [
                "let's study",
                "lets study",
                "i want to study",
                "what should i study",
                "study something",
                "time to study"
            ]

            if any(
                word in message
                for word in study_words
            ):

                self.set_outfit(
                    "studying"
                )

                self.set_emotion(
                    "happy"
                )

                return (
                    f"Sure! Since I remember that "
                    f"{favorite_subject} is your favorite "
                    f"subject, we can work on {favorite_subject}."
                )

        # ==================================================
        # MEMORY-AWARE FAVORITE COLOR
        # ==================================================

        if favorite_color:

            if (
                "favorite color" in message
                or "favourite color" in message
                or "favorite colour" in message
                or "favourite colour" in message
            ):

                self.set_emotion(
                    "happy"
                )

                return (
                    f"I remember your favorite "
                    f"color is {favorite_color}."
                )

        # ==================================================
        # STUDYING MODE
        # ==================================================

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

            return random.choice([
                "Study mode activated. Let's get to work.",
                "Study mode is ready. What are we learning today?",
                "Alright, study mode activated. Let's tackle it together."
            ])

        # ==================================================
        # GAMING MODE
        # ==================================================

        gaming_words = [
            "gaming",
            "game",
            "playing games",
            "play games",
            "play a game",
            "playing a game",
            "playing"
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

            return random.choice([
                "Gaming mode activated! What are we playing?",
                "Gaming mode activated! I'm ready. What game are you playing?",
                "Let's go! Gaming mode is ready. What are we playing?"
            ])

        # ==================================================
        # NIGHT MODE
        # ==================================================

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
                "Night mode activated. Time to relax."
            )

        # ==================================================
        # RETURN TO NORMAL
        # ==================================================

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

        # ==================================================
        # STATUS
        # ==================================================

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

        # ==================================================
        # CONVERSATION HISTORY
        # ==================================================

        if (
            "show conversation" in message
            or "show our conversation" in message
            or "conversation history" in message
            or "what did we talk about" in message
            or message == "conversation"
        ):

            return self.conversation_status()

        # ==================================================
        # MEMORY
        # ==================================================

        if (
            "what do you remember" in message
            or "show your memory" in message
            or "what do you know about me" in message
            or "your memory" in message
        ):

            return self.commands.memory_status(
                self.memory.memories
            )

        # ==================================================
        # TIME
        # ==================================================

        if (
            "what time is it" in message
            or "what's the time" in message
            or "what is the time" in message
            or "tell me the time" in message
            or "current time" in message
            or message == "time"
        ):

            return self.commands.get_time()

        # ==================================================
        # DATE
        # ==================================================

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

        # ==================================================
        # HELP
        # ==================================================

        if (
            message == "help"
            or "what can you do" in message
            or "what can you help me with" in message
            or "show me what you can do" in message
            or message == "commands"
        ):

            return self.commands.help()

        # =========================
        # FLEXIBLE MEMORY
        # =========================

        remember_patterns = [
            "remember that ",
            "remember ",
            "please remember that ",
            "please remember "
        ]

        memory_request = None

        for pattern in remember_patterns:

            if message.startswith(pattern):

                memory_request = message[
                    len(pattern):
                ].strip()

                break

        if memory_request:

            if " is " in memory_request:

                parts = memory_request.split(
                    " is ",
                    1
                )

                memory_key = (
                    parts[0]
                    .strip()
                    .lower()
                )

                memory_value = (
                    parts[1]
                    .strip()
                )

                prefixes = [
                    "my ",
                    "our ",
                    "the "
                ]

                for prefix in prefixes:

                    if memory_key.startswith(
                        prefix
                    ):

                        memory_key = (
                            memory_key[
                                len(prefix):
                            ]
                        )

                        break

                if memory_key and memory_value:

                    self.memory.remember(
                        memory_key,
                        memory_value
                    )

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        f"Got it! I'll remember "
                        f"that your {memory_key} "
                        f"is {memory_value}."
                    )

            self.memory.remember(
                "note",
                memory_request
            )

            self.set_emotion(
                "happy"
            )

            return (
                "Got it! I'll remember that."
            )

        # =========================
        # FORGET MEMORY
        # =========================

        forget_patterns = [
            "forget my ",
            "forget the ",
            "forget ",
            "please forget my ",
            "please forget the ",
            "please forget "
        ]

        forget_key = None

        for pattern in forget_patterns:

            if message.startswith(pattern):

                forget_key = message[
                    len(pattern):
                ].strip()

                break

        if forget_key:

            prefixes = [
                "favorite ",
                "my "
            ]

            for prefix in prefixes:

                if forget_key.startswith(
                    prefix
                ):

                    forget_key = (
                        forget_key[
                            len(prefix):
                        ]
                    )

                    break

            if self.memory.forget(
                forget_key
            ):

                self.set_emotion(
                    "neutral"
                )

                return (
                    f"Okay. I've forgotten "
                    f"your {forget_key}."
                )

            return (
                f"I don't currently have "
                f"{forget_key} in my memory."
            )

        # ==================================================
        # REMEMBER NAME
        # ==================================================

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

        # ==================================================
        # REMEMBER FAVORITE GAME
        # ==================================================

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

        # ==================================================
        # REMEMBER FAVORITE SUBJECT
        # ==================================================

        favorite_subject_prefixes = [
            "my favorite subject is ",
            "my fav subject is "
        ]

        for prefix in favorite_subject_prefixes:

            if message.startswith(prefix):

                subject = message.replace(
                    prefix,
                    "",
                    1
                ).strip()

                self.memory.remember(
                    "favorite_subject",
                    subject
                )

                self.set_emotion(
                    "happy"
                )

                return (
                    f"Got it. I'll remember that "
                    f"your favorite subject is {subject}."
                )

        # ==================================================
        # RECALL NAME
        # ==================================================

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

        # ==================================================
        # RECALL FAVORITE GAME
        # ==================================================

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

        # ==================================================
        # RECALL FAVORITE SUBJECT
        # ==================================================

        if (
            "what is my favorite subject"
            in message
            or "what's my favorite subject"
            in message
        ):

            subject = self.memory.recall(
                "favorite_subject"
            )

            if subject:

                return (
                    f"Your favorite subject is "
                    f"{subject}."
                )

            return (
                "You haven't told me "
                "your favorite subject yet."
            )

        # ==================================================
        # EMOTION STATUS
        # ==================================================

        if (
            "what are you feeling" in message
            or "what is your emotion" in message
        ):

            return (
                f"My current state is "
                f"{self.emotion.get_emotion()}."
            )

        # ==================================================
        # EXPRESSION STATUS
        # ==================================================

        if (
            "what expression" in message
            or "what are you showing" in message
        ):

            return (
                f"My current expression is "
                f"{self.expression.get_expression()}."
            )

        # ==================================================
        # OUTFIT STATUS
        # ==================================================

        if (
            "what are you wearing" in message
            or "what is your outfit" in message
        ):

            return (
                f"My current outfit is "
                f"{self.outfit.get_outfit()}."
            )

        # ==================================================
        # HOW ARE YOU
        # ==================================================

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

        # ==================================================
        # NATURAL GREETINGS
        # ==================================================

        greeting_words = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if (
            message in greeting_words
            or any(
                greeting in message.split()
                for greeting in [
                    "hello",
                    "hi",
                    "hey"
                ]
            )
            or message.startswith("good morning")
            or message.startswith("good afternoon")
            or message.startswith("good evening")
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

        # ==================================================
        # POSITIVE CONTEXT
        # ==================================================

        positive_context_words = [
            "amazing",
            "awesome",
            "fun",
            "great",
            "cool",
            "enjoying",
            "enjoy",
            "fantastic",
            "wonderful",
            "incredible"
        ]

        if any(
            word in message.split()
            for word in positive_context_words
        ):

            # ------------------------------------------
            # GAMING CONTEXT
            # ------------------------------------------

            if conversation_topic == "gaming":

                self.set_emotion(
                    "happy"
                )

                responses = [
                    "That's awesome! Sounds like you're having fun with the game.",
                    "Nice! I'm glad you're enjoying the game.",
                    "That's great! Sounds like gaming is going well.",
                    "Awesome! Keep enjoying yourself!"
                ]

                return random.choice(
                    responses
                )

            # ------------------------------------------
            # STUDY CONTEXT
            # ------------------------------------------

            if conversation_topic == "studying":

                self.set_emotion(
                    "happy"
                )

                responses = [
                    "That's great! I'm glad you're enjoying your study session.",
                    "Nice! Sounds like you're getting into it.",
                    "Awesome! Keep going — you're making progress.",
                    "That's good to hear! What are you studying?"
                ]

                return random.choice(
                    responses
                )

            # ------------------------------------------
            # GENERAL POSITIVE MESSAGE
            # ------------------------------------------

            self.set_emotion(
                "happy"
            )

            responses = [
                "That's awesome to hear!",
                "Nice! I love the positive energy.",
                "That's great! I'm glad you're enjoying yourself.",
                "Awesome! Tell me more about it."
            ]

            return random.choice(
                responses
            )

        # ==================================================
        # USER FEELS GOOD
        # ==================================================

        positive_phrases = [
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
            for phrase in positive_phrases
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

        # ==================================================
        # USER FEELS NOT GOOD
        # ==================================================

        negative_phrases = [
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
            for phrase in negative_phrases
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

        # ==================================================
        # HAPPY
        # ==================================================

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

        # ==================================================
        # TIRED
        # ==================================================

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

        # ==================================================
        # SAD
        # ==================================================

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

        # ==================================================
        # BORED
        # ==================================================

        if "bored" in message:

            self.set_emotion(
                "bored"
            )

            return (
                "Hmm... sounds like you're bored. "
                "Maybe we should do something fun."
            )

        # ==================================================
        # IDENTITY
        # ==================================================

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

        # ==================================================
        # GOODBYE
        # ==================================================

        if (
            message == "bye"
            or message == "goodbye"
            or message.startswith("bye ")
        ):

            self.set_emotion(
                "neutral"
            )

            return (
                self.personality.goodbye()
            )

        # ==================================================
        # DEEP CONTEXTUAL CONVERSATION
        # ==================================================

        if previous_message:

            # ------------------------------------------
            # DIFFICULT / HARD
            # ------------------------------------------

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

                if conversation_topic == "gaming":

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "Yeah, that sounds challenging. "
                        "What part of the game are you "
                        "finding difficult?"
                    )

                if conversation_topic == "studying":

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "I understand. That can be "
                        "challenging. Let's break it down "
                        "into smaller parts and work "
                        "through it together."
                    )

                if conversation_topic == "programming":

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        "Programming can definitely get "
                        "complicated. Let's break the "
                        "problem into smaller pieces."
                    )

                self.set_emotion(
                    "happy"
                )

                return (
                    "I understand. That sounds "
                    "challenging. Let's work through "
                    "it together."
                )

            # ------------------------------------------
            # USER DOESN'T KNOW
            # ------------------------------------------

            if message in [
                "i don't know",
                "i dont know",
                "idk",
                "not sure",
                "i'm not sure",
                "im not sure"
            ]:

                self.set_emotion(
                    "neutral"
                )

                if conversation_topic == "gaming":

                    return (
                        "That's okay! We can figure it "
                        "out. What part of the game are "
                        "you thinking about?"
                    )

                if conversation_topic == "studying":

                    return (
                        "That's okay. We can figure it "
                        "out together. What part are you "
                        "unsure about?"
                    )

                if conversation_topic == "programming":

                    return (
                        "No problem. We can work through "
                        "the code together. What part is "
                        "confusing you?"
                    )

                return (
                    "That's okay. We don't have to "
                    "figure everything out immediately. "
                    "What are you thinking about?"
                )

            # ------------------------------------------
            # TELL ME MORE
            # ------------------------------------------

            if message in [
                "tell me more",
                "go on",
                "continue"
            ]:

                self.set_emotion(
                    "happy"
                )

                if conversation_topic == "gaming":

                    return (
                        "Sure! I'm listening. Tell me "
                        "what's happening in the game."
                    )

                if conversation_topic == "studying":

                    return (
                        "Sure! Let's keep going. "
                        "What part are you studying?"
                    )

                if conversation_topic == "programming":

                    return (
                        "Sure! Let's continue. "
                        "Show me what you're working on."
                    )

                return (
                    "Sure! I'm listening. "
                    "Tell me more about it."
                )

            # ------------------------------------------
            # AGREEMENT
            # ------------------------------------------

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

            # ------------------------------------------
            # DISAGREEMENT
            # ------------------------------------------

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

            # ------------------------------------------
            # REQUEST FOR HELP
            # ------------------------------------------

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

                if conversation_topic == "gaming":

                    return (
                        "Of course! Tell me what you're "
                        "stuck on in the game."
                    )

                if conversation_topic == "studying":

                    return (
                        "Of course! Tell me what you're "
                        "working on and we'll tackle it."
                    )

                if conversation_topic == "programming":

                    return (
                        "Absolutely! Tell me what's "
                        "happening with your code."
                    )

                return (
                    "Of course! I'm here to help. "
                    "Tell me what you're working on."
                )

            # ------------------------------------------
            # GAME FOLLOW-UP
            # ------------------------------------------

            if conversation_topic == "gaming":

                if len(message.split()) <= 4:

                    if message not in [
                        "yes",
                        "yeah",
                        "yep",
                        "no",
                        "nope"
                    ]:

                        self.set_emotion(
                            "happy"
                        )

                        self.memory.remember(
                            "current_game",
                            message
                        )

                        return (
                            f"Ohh, {message}! 😄 "
                            f"How are you finding it so far?"
                        )

            # ------------------------------------------
            # STUDY FOLLOW-UP
            # ------------------------------------------

            if conversation_topic == "studying":

                if len(message.split()) <= 4:

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        f"{message.title()}! Nice. 😄 "
                        f"What are you working on?"
                    )

            # ------------------------------------------
            # PROGRAMMING FOLLOW-UP
            # ------------------------------------------

            if conversation_topic == "programming":

                if len(message.split()) <= 4:

                    self.set_emotion(
                        "happy"
                    )

                    return (
                        f"{message.title()}! Nice. "
                        f"What are you building or "
                        f"working on?"
                    )

            # ------------------------------------------
            # SHORT FOLLOW-UP
            # ------------------------------------------

            if len(
                message.split()
            ) <= 3:

                self.set_emotion(
                    "neutral"
                )

                return (
                    "I understand. "
                    "Tell me a little more."
                )

        # ==================================================
        # UNKNOWN MESSAGE
        # ==================================================

        self.set_emotion(
            "neutral"
        )

        return (
            self.personality.unknown_response()
        )