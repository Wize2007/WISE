import tkinter as tk
import os
import random

from PIL import Image, ImageTk

from brain.brain import WiseBrain
from brain.voice import WiseVoice


class WiseInterface:

    def __init__(self):

        # =========================
        # WISE BRAIN
        # =========================

        self.brain = WiseBrain()

        # =========================
        # WISE VOICE
        # =========================

        self.voice = WiseVoice()

        # =========================
        # MAIN WINDOW
        # =========================

        self.window = tk.Tk()

        self.window.title(
            "WISE - Your AI Companion"
        )

        self.window.geometry(
            "900x800"
        )

        self.window.minsize(
            700,
            600
        )

        # =========================
        # TITLE
        # =========================

        self.title = tk.Label(
            self.window,
            text="W I S E",
            font=("Arial", 24, "bold")
        )

        self.title.pack(
            pady=(5, 0)
        )

        # =========================
        # STATUS
        # =========================

        self.status = tk.Label(
            self.window,
            text="WISE is ready.",
            font=("Arial", 11)
        )

        self.status.pack(
            pady=(0, 3)
        )

        # ==================================================
        # CHARACTER FRAME
        # ==================================================

        self.character_frame = tk.Frame(
            self.window,
            height=240
        )

        self.character_frame.pack(
            fill="x",
            pady=2
        )

        # Keep the frame at exactly 240 pixels.

        self.character_frame.pack_propagate(
            False
        )

        # =========================
        # CHARACTER DISPLAY
        # =========================

        self.expression_display = tk.Label(
            self.character_frame
        )

        self.expression_display.pack(
            expand=True
        )

        self.current_image = None

        # =========================
        # INITIAL IMAGE
        # =========================

        self.update_character_image()

        # ==================================================
        # CHAT FRAME
        # ==================================================

        self.chat_frame = tk.Frame(
            self.window,
            height=250
        )

        self.chat_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # Keep chat area at exactly 250 pixels.

        self.chat_frame.pack_propagate(
            False
        )

        # ==================================================
        # CHAT CONTAINER
        # ==================================================

        self.chat_container = tk.Frame(
            self.chat_frame
        )

        self.chat_container.pack(
            fill="both",
            expand=True
        )

        # =========================
        # CHAT BOX
        # =========================

        self.chat = tk.Text(
            self.chat_container,
            font=("Arial", 11),
            state="disabled",
            wrap="word",
            padx=10,
            pady=8
        )

        self.chat.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =========================
        # CHAT SCROLLBAR
        # =========================

        self.chat_scrollbar = tk.Scrollbar(
            self.chat_container,
            command=self.chat.yview
        )

        self.chat_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat.config(
            yscrollcommand=self.chat_scrollbar.set
        )

        # ==================================================
        # MESSAGE FRAME
        # ==================================================

        self.message_frame = tk.Frame(
            self.window
        )

        self.message_frame.pack(
            fill="x",
            padx=15,
            pady=(2, 10)
        )

        # =========================
        # MESSAGE BOX
        # =========================

        self.message = tk.Entry(
            self.message_frame,
            font=("Arial", 13)
        )

        self.message.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7,
            padx=(0, 8)
        )

        # Press ENTER to send.

        self.message.bind(
            "<Return>",
            self.send_message
        )

        # =========================
        # SEND BUTTON
        # =========================

        self.send_button = tk.Button(
            self.message_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            width=10,
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            ipady=4
        )

        # =========================
        # INTRODUCTION
        # =========================

        introduction = (
            self.brain.introduce()
        )

        self.add_message(
            "WISE",
            introduction
        )

        self.speak(
            introduction
        )

        # =========================
        # START BLINKING
        # =========================

        self.schedule_blink()

    # ==================================================
    # DISPLAY IMAGE
    # ==================================================

    def display_image(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        ).convert("RGBA")

        # ==========================================
        # WISE IMAGE SIZE
        # ==========================================
        #
        # Maximum width  = 130 pixels
        # Maximum height = 220 pixels
        #
        # Original aspect ratio is preserved.

        image.thumbnail(
            (130, 220),
            Image.Resampling.LANCZOS
        )

        self.current_image = ImageTk.PhotoImage(
            image
        )

        self.expression_display.config(
            image=self.current_image,
            text=""
        )

    # ==================================================
    # UPDATE CHARACTER IMAGE
    # ==================================================

    def update_character_image(self):

        state = self.brain.get_state()

        outfit = state["outfit"]
        expression = state["expression"]

        image_path = os.path.join(
            "character",
            outfit,
            f"{expression}.png"
        )

        print(
            "WISE IMAGE:",
            image_path
        )

        try:

            self.display_image(
                image_path
            )

            return

        except FileNotFoundError:

            pass

        # =========================
        # FALLBACK
        # =========================

        fallback_path = os.path.join(
            "character",
            expression,
            f"{expression}.png"
        )

        print(
            "WISE FALLBACK:",
            fallback_path
        )

        try:

            self.display_image(
                fallback_path
            )

            return

        except FileNotFoundError:

            pass

        self.expression_display.config(
            image="",
            text=(
                f"{outfit.upper()} / "
                f"{expression.upper()} "
                "IMAGE NOT FOUND"
            ),
            font=("Arial", 14, "bold")
        )

    # ==================================================
    # BLINK TIMER
    # ==================================================

    def schedule_blink(self):

        delay = random.randint(
            4000,
            8000
        )

        self.window.after(
            delay,
            self.blink
        )

    # ==================================================
    # BLINK
    # ==================================================

    def blink(self):

        blink_path = os.path.join(
            "character",
            "neutral",
            "animation",
            "blink.png"
        )

        print(
            "WISE BLINK:",
            blink_path
        )

        try:

            self.display_image(
                blink_path
            )

            # Keep eyes closed briefly.

            self.window.after(
                160,
                self.restore_after_blink
            )

        except FileNotFoundError:

            print(
                "WISE BLINK IMAGE NOT FOUND"
            )

            self.schedule_blink()

    # ==================================================
    # RESTORE AFTER BLINK
    # ==================================================

    def restore_after_blink(self):

        self.update_character_image()

        self.schedule_blink()

    # ==================================================
    # ADD CHAT MESSAGE
    # ==================================================

    def add_message(
        self,
        speaker,
        message
    ):

        self.chat.config(
            state="normal"
        )

        self.chat.insert(
            tk.END,
            f"{speaker}: {message}\n\n"
        )

        self.chat.config(
            state="disabled"
        )

        # Always scroll to newest message.

        self.chat.see(
            tk.END
        )

    # ==================================================
    # WISE VOICE
    # ==================================================

    def speak(
        self,
        text
    ):

        try:

            print(
                "WISE VOICE:",
                text
            )

            self.voice.speak(
                text
            )

            print(
                "WISE FINISHED SPEAKING"
            )

        except Exception as error:

            print(
                "VOICE ERROR:",
                error
            )

    # ==================================================
    # SEND MESSAGE
    # ==================================================

    def send_message(
        self,
        event=None
    ):

        text = (
            self.message
            .get()
            .strip()
        )

        if not text:

            return

        print(
            "USER MESSAGE:",
            text
        )

        # =========================
        # SHOW USER MESSAGE
        # =========================

        self.add_message(
            "You",
            text
        )

        # =========================
        # CLEAR INPUT
        # =========================

        self.message.delete(
            0,
            tk.END
        )

        # =========================
        # TEMPORARILY DISABLE INPUT
        # =========================

        self.message.config(
            state="disabled"
        )

        self.send_button.config(
            state="disabled"
        )

        # =========================
        # THINKING STATUS
        # =========================

        self.status.config(
            text="WISE is thinking..."
        )

        # =========================
        # PROCESS MESSAGE
        # =========================

        self.window.after(
            50,
            lambda: self.process_message(text)
        )

    # ==================================================
    # PROCESS MESSAGE
    # ==================================================

    def process_message(
        self,
        text
    ):

        try:

            # =========================
            # WISE THINKS
            # =========================

            response = self.brain.think(
                text
            )

            print(
                "WISE RESPONSE:",
                response
            )

            # =========================
            # SHOW RESPONSE
            # =========================

            self.add_message(
                "WISE",
                response
            )

            # =========================
            # SPEAK RESPONSE
            # =========================

            self.speak(
                response
            )

            # =========================
            # CURRENT STATE
            # =========================

            state = self.brain.get_state()

            outfit = state["outfit"]
            expression = state["expression"]

            self.status.config(
                text=(
                    f"Outfit: {outfit}   |   "
                    f"Expression: {expression}"
                )
            )

            # =========================
            # UPDATE IMAGE
            # =========================

            self.update_character_image()

        except Exception as error:

            print(
                "WISE ERROR:",
                error
            )

            self.add_message(
                "WISE",
                "I'm sorry, something went wrong."
            )

            self.status.config(
                text="WISE encountered an error."
            )

        finally:

            # =========================
            # RESTORE INPUT
            # =========================

            self.message.config(
                state="normal"
            )

            self.send_button.config(
                state="normal"
            )

            self.message.focus_set()

    # ==================================================
    # RUN WISE
    # ==================================================

    def run(self):

        self.window.mainloop()


# ======================================================
# START WISE
# ======================================================

if __name__ == "__main__":

    app = WiseInterface()

    app.run()