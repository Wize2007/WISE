import tkinter as tk
from tkinter import messagebox

from brain.brain import WiseBrain
from brain.star import WiseStar
from brain.voice import WiseVoice


class WiseInterface:

    BG = "#050505"
    PANEL = "#0b0b0b"
    PANEL_2 = "#101010"
    GOLD = "#d8a52b"
    GOLD_BRIGHT = "#f0c75e"
    TEXT = "#eeeeee"
    MUTED = "#9c9c9c"

    def __init__(self):
        self.brain = WiseBrain()
        self.voice = WiseVoice()

        self.window = tk.Tk()
        self.window.title("WISE - Your AI Companion")
        self.window.geometry("1000x720")
        self.window.minsize(760, 600)
        self.window.configure(bg=self.BG)
        self.window.protocol("WM_DELETE_WINDOW", self.shutdown)

        self._closing = False
        self.voice_enabled = True

        self._build_header()
        self._build_main_area()
        self._build_chat_panel()
        self._build_message_area()

        self.star.set_emotion(self.brain.get_state()["emotion"])
        self.star.set_state("idle")

        introduction = self.brain.introduce()
        self.add_message("WISE", introduction)
        self.speak(introduction)

        self.message.focus_set()

    # ==================================================
    # WINDOW
    # ==================================================

    def _build_header(self):
        header = tk.Frame(self.window, bg=self.BG)
        header.pack(fill="x", padx=18, pady=(14, 6))

        title = tk.Label(
            header,
            text="W I S E",
            bg=self.BG,
            fg=self.GOLD_BRIGHT,
            font=("Arial", 22, "bold"),
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header,
            text="YOUR AI COMPANION",
            bg=self.BG,
            fg=self.MUTED,
            font=("Arial", 9, "bold"),
        )
        subtitle.pack(side="left", padx=(14, 0), pady=(8, 0))

        self.status = tk.Label(
            header,
            text="IDLE",
            bg=self.BG,
            fg=self.GOLD,
            font=("Arial", 9, "bold"),
        )
        self.status.pack(side="right", pady=(7, 0))

    # ==================================================
    # MAIN AREA
    # ==================================================

    def _build_main_area(self):
        main = tk.Frame(self.window, bg=self.BG)
        main.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        star_frame = tk.Frame(
            main,
            bg=self.BG,
            highlightthickness=1,
            highlightbackground="#17130a",
        )
        star_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8),
        )

        self.star = WiseStar(star_frame)

        self.chat_panel = tk.Frame(
            main,
            bg=self.PANEL,
            width=330,
            highlightthickness=1,
            highlightbackground="#211b0d",
        )
        self.chat_panel.pack(
            side="right",
            fill="y",
            padx=(8, 0),
        )
        self.chat_panel.pack_propagate(False)

    # ==================================================
    # CHAT PANEL
    # ==================================================

    def _build_chat_panel(self):
        panel_header = tk.Frame(self.chat_panel, bg=self.PANEL)
        panel_header.pack(fill="x", padx=12, pady=(12, 7))

        tk.Label(
            panel_header,
            text="CONVERSATION",
            bg=self.PANEL,
            fg=self.GOLD_BRIGHT,
            font=("Arial", 10, "bold"),
        ).pack(side="left")

        self.voice_button = tk.Button(
            panel_header,
            text="VOICE ON",
            command=self.toggle_voice,
            bg="#17130a",
            fg=self.GOLD_BRIGHT,
            activebackground="#211b0d",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            font=("Arial", 8, "bold"),
            padx=8,
            pady=4,
        )
        self.voice_button.pack(side="right")

        chat_container = tk.Frame(self.chat_panel, bg=self.PANEL)
        chat_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10),
        )

        self.chat = tk.Text(
            chat_container,
            bg=self.PANEL_2,
            fg=self.TEXT,
            insertbackground=self.GOLD_BRIGHT,
            selectbackground="#3a2c12",
            selectforeground="#ffffff",
            font=("Arial", 10),
            state="disabled",
            wrap="word",
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
        )
        self.chat.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            chat_container,
            command=self.chat.yview,
            bg="#161616",
            troughcolor=self.PANEL_2,
            activebackground=self.GOLD,
        )
        scrollbar.pack(side="right", fill="y")
        self.chat.config(yscrollcommand=scrollbar.set)

        self.chat.tag_configure(
            "wise",
            foreground=self.GOLD_BRIGHT,
            font=("Arial", 10, "bold"),
        )
        self.chat.tag_configure(
            "you",
            foreground="#d0d0d0",
            font=("Arial", 10, "bold"),
        )
        self.chat.tag_configure(
            "body",
            foreground=self.TEXT,
            font=("Arial", 10),
        )

    # ==================================================
    # MESSAGE AREA
    # ==================================================

    def _build_message_area(self):
        bottom = tk.Frame(
            self.chat_panel,
            bg=self.PANEL,
        )
        bottom.pack(
            fill="x",
            padx=10,
            pady=(0, 12),
        )

        self.message = tk.Entry(
            bottom,
            bg=self.PANEL_2,
            fg=self.TEXT,
            insertbackground=self.GOLD_BRIGHT,
            font=("Arial", 11),
            relief="flat",
            bd=0,
        )
        self.message.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 7),
        )
        self.message.bind("<Return>", self.send_message)
        self.message.bind("<KeyRelease>", self._typing_state)

        self.send_button = tk.Button(
            bottom,
            text="SEND",
            command=self.send_message,
            bg="#8f681b",
            fg="#ffffff",
            activebackground="#b58424",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            font=("Arial", 9, "bold"),
            padx=12,
            pady=7,
        )
        self.send_button.pack(side="right")

    def _typing_state(self, event=None):
        if self._closing:
            return

        if self.message.get().strip():
            self.set_star_state("listening")
        else:
            self.set_star_state("idle")

    # ==================================================
    # STATE CONTROL
    # ==================================================

    def set_status(self, state):
        self.status.config(text=state.upper())

    def set_star_state(self, state):
        if self._closing:
            return

        self.star.set_state(state)
        self.set_status(state)

    def sync_emotion(self):
        try:
            self.star.set_emotion(
                self.brain.get_state()["emotion"]
            )
        except Exception as error:
            print("WISE EMOTION SYNC ERROR:", error)

    # ==================================================
    # CHAT
    # ==================================================

    def add_message(self, speaker, message):
        self.chat.config(state="normal")

        tag = "wise" if speaker == "WISE" else "you"

        self.chat.insert(tk.END, f"{speaker}\n", tag)
        self.chat.insert(tk.END, f"{message}\n\n", "body")

        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    # ==================================================
    # VOICE
    # ==================================================

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        self.voice_button.config(
            text="VOICE ON" if self.voice_enabled else "VOICE OFF"
        )

    def speak(self, text):
        if not self.voice_enabled or self._closing:
            return

        try:
            self.voice.speak(
                text,
                on_start=self._voice_started,
                on_finish=self._voice_finished,
            )
        except TypeError:
            # Backward-compatible fallback for an older WiseVoice implementation.
            self.voice.speak(text)
        except Exception as error:
            print("VOICE ERROR:", error)
            self.set_star_state("error")

    def _voice_started(self):
        if self._closing:
            return
        try:
            self.window.after(0, lambda: self.set_star_state("speaking"))
        except tk.TclError:
            pass

    def _voice_finished(self):
        if self._closing:
            return
        try:
            self.window.after(0, self._finish_speaking)
        except tk.TclError:
            pass

    def _finish_speaking(self):
        if self._closing:
            return
        self.sync_emotion()
        self.set_star_state("idle")

    # ==================================================
    # SEND MESSAGE
    # ==================================================

    def send_message(self, event=None):
        if self._closing:
            return "break"

        text = self.message.get().strip()

        if not text:
            return "break"

        print("USER MESSAGE:", text)

        self.add_message("You", text)
        self.message.delete(0, tk.END)

        self.message.config(state="disabled")
        self.send_button.config(state="disabled")

        self.set_star_state("thinking")

        self.window.after(
            50,
            lambda: self.process_message(text),
        )

        return "break"

    # ==================================================
    # PROCESS MESSAGE
    # ==================================================

    def process_message(self, text):
        try:
            response = self.brain.think(text)
            print("WISE RESPONSE:", response)

            self.sync_emotion()
            self.add_message("WISE", response)

            # The voice callback moves the star to SPEAKING.
            # If voice is disabled, show the response pulse briefly.
            if self.voice_enabled:
                self.speak(response)
            else:
                self.set_star_state("speaking")
                self.window.after(650, self._finish_speaking)

        except Exception as error:
            print("WISE ERROR:", error)

            self.add_message(
                "WISE",
                "I'm sorry, something went wrong.",
            )
            self.set_star_state("error")
            self.window.after(900, self._return_to_idle)

        finally:
            self.message.config(state="normal")
            self.send_button.config(state="normal")
            self.message.focus_set()

    def _return_to_idle(self):
        if not self._closing:
            self.sync_emotion()
            self.set_star_state("idle")

    # ==================================================
    # SHUTDOWN
    # ==================================================

    def shutdown(self):
        if self._closing:
            return

        self._closing = True
        self.set_status("GOODBYE")
        self.star.set_state("goodbye")

        # Give the star a moment to visually fade before closing.
        try:
            self.window.after(650, self._destroy)
        except tk.TclError:
            self._destroy()

    def _destroy(self):
        try:
            self.star.stop()
        except Exception:
            pass

        try:
            self.window.destroy()
        except tk.TclError:
            pass

    # ==================================================
    # RUN
    # ==================================================

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = WiseInterface()
    app.run()
