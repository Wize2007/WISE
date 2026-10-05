import base64
import re
import subprocess
import threading


class WiseVoice:
    """Non-blocking Windows voice with smoother pacing and a calm delivery."""

    PREFERRED_VOICES = (
        "Microsoft David",
        "Microsoft Guy Online (Natural) - English (United States)",
        "Microsoft Mark",
    )

    def __init__(self):
        print("WISE voice system initialized.")

    def remove_emojis(self, text):
        text = re.sub(
            r'[U0001F300-U0001FAFF]'
            r'|[U00002700-U000027BF]'
            r'|[U00002600-U000026FF]',
            '',
            text
        )
        return re.sub(r'[ 	]+', ' ', text).strip()

    def _build_ssml(self, text):
        safe = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        # Give punctuation room to breathe so speech does not become a
        # continuous machine-like stream.
        safe = re.sub(r'([.!?])\s+', r'\1<break time="240ms"/> ', safe)
        safe = re.sub(r'[,;:]\s+', r'\g<0><break time="110ms"/>', safe)
        return (
            '<?xml version="1.0"?>'
            '<speak version="1.0" '
            'xmlns="http://www.w3.org/2001/10/synthesis" '
            'xml:lang="en-US">'
            '<prosody rate="-7%" pitch="-2st">'
            + safe +
            '</prosody></speak>'
        )

    def speak(self, text, on_start=None, on_finish=None):
        thread = threading.Thread(
            target=self._speak,
            args=(text, on_start, on_finish),
            daemon=True,
        )
        thread.start()

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

            ssml = self._build_ssml(speech_text)
            encoded = base64.b64encode(ssml.encode("utf-8")).decode("ascii")
            voices = "|".join(self.PREFERRED_VOICES)

            # Pass the SSML as base64 so punctuation or user text cannot
            # accidentally break the PowerShell command.
            ps = (
                "Add-Type -AssemblyName System.Speech; "
                "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                "$preferred='" + voices.replace("'", "''") + "'.Split('|'); "
                "$chosen=$null; "
                "foreach($v in $preferred){"
                "try{$s.SelectVoice($v);$chosen=$v;break}catch{}}; "
                "$xml=[Text.Encoding]::UTF8.GetString("
                "[Convert]::FromBase64String('" + encoded + "')); "
                "try{$s.SpeakSsml($xml)}catch{$s.Speak("
                "[System.Text.RegularExpressions.Regex]::Replace("
                "$xml,'<[^>]+>',''))}; "
                "$s.Dispose();"
            )

            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120,
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
