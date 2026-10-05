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

    def speak(self, text, on_start=None, on_finish=None):
        """Speak in the background and optionally report lifecycle events."""
        speech_thread = threading.Thread(
            target=self._speak,
            args=(text, on_start, on_finish),
            daemon=True,
        )
        speech_thread.start()

    # =========================
    # ACTUAL SPEECH
    # =========================

    def _speak(self, text, on_start=None, on_finish=None):
        try:
            print("WISE VOICE:", text)

            speech_text = self.remove_emojis(text)

            if not speech_text:
                if on_finish:
                    on_finish()
                return

            if on_start:
                on_start()

            safe_text = speech_text.replace("'", "''")

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
                    command,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            print("WISE FINISHED SPEAKING")

        except Exception as error:
            print("VOICE ERROR:", error)

        finally:
            if on_finish:
                try:
                    on_finish()
                except Exception as callback_error:
                    print("VOICE CALLBACK ERROR:", callback_error)
