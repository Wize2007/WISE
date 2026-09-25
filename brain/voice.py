import subprocess
import re
import threading


class WiseVoice:

    def __init__(self):

        print("WISE voice system initialized.")

    # =========================
    # REMOVE EMOJIS
    # =========================

    def remove_emojis(self, text):

        # Remove emoji and other Unicode symbols
        # that Windows Speech may try to pronounce.

        text = re.sub(
            r'[\U0001F300-\U0001FAFF]'
            r'|[\U00002700-\U000027BF]'
            r'|[\U00002600-\U000026FF]',
            '',
            text
        )

        return text.strip()

    # =========================
    # SPEAK
    # =========================

    def speak(self, text):

        # Run speech in a background thread
        # so the WISE interface does not freeze.

        speech_thread = threading.Thread(
            target=self._speak,
            args=(text,),
            daemon=True
        )

        speech_thread.start()

    # =========================
    # ACTUAL SPEECH
    # =========================

    def _speak(self, text):

        try:

            print(
                "WISE VOICE:",
                text
            )

            # Remove emojis before speaking

            speech_text = self.remove_emojis(
                text
            )

            # If the message contains only
            # emojis or symbols, don't speak.

            if not speech_text:

                return

            # Escape apostrophes for PowerShell

            safe_text = speech_text.replace(
                "'",
                "''"
            )

            command = (
                "Add-Type -AssemblyName System.Speech; "
                "$speak = New-Object "
                "System.Speech.Synthesis.SpeechSynthesizer; "
                f"$speak.Speak('{safe_text}')"
            )

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    command
                ],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            print(
                "WISE FINISHED SPEAKING"
            )

        except Exception as error:

            print(
                "VOICE ERROR:",
                error
            )