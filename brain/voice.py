import re
import subprocess
import threading


class WiseVoice:
    """Non-blocking Windows System.Speech voice with natural pacing."""

    PREFERRED_VOICES = (
        "Microsoft David Desktop",
        "Microsoft Mark Desktop",
        "Microsoft Zira Desktop",
        "Microsoft David",
        "Microsoft Mark",
        "Microsoft Zira",
    )

    def __init__(self):
        print("WISE voice system initialized.")

    def remove_emojis(self, text):
        text = re.sub(
            r'[\U0001F300-\U0001FAFF]'
            r'|[\U00002700-\U000027BF]'
            r'|[\U00002600-\U000026FF]',
            '',
            text,
        )
        return re.sub(r'[ \t]+', ' ', text).strip()

    def _prepare_text(self, text):
        text = self.remove_emojis(text)

        # Make common symbols speak naturally instead of spelling punctuation.
        text = text.replace("—", ", ").replace("–", ", ")
        text = text.replace("•", ", ")
        text = re.sub(r'\s*:\s*', ': ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Give short responses a gentle conversational rhythm.
        text = re.sub(r'([.!?])\s+', r'\1  ', text)
        return text

    def speak(self, text, on_start=None, on_finish=None):
        thread = threading.Thread(
            target=self._speak,
            args=(text, on_start, on_finish),
            daemon=True,
        )
        thread.start()

    def _speak(self, text, on_start=None, on_finish=None):
        try:
            speech_text = self._prepare_text(text)

            if not speech_text:
                if on_finish:
                    on_finish()
                return

            print("WISE VOICE:", speech_text)

            if on_start:
                on_start()

            encoded = speech_text.encode("utf-8").hex()

            # IMPORTANT: use normal SpeechSynthesizer.Speak, not SSML.
            # This prevents WISE from reading XML/SSML tags or individual markup
            # characters when a Windows voice does not support SSML correctly.
            ps = r'''
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$text = [System.Text.Encoding]::UTF8.GetString(
    [Convert]::FromHexString('''' + '''''' + '''ENCODED''' + '''''')
)

$preferred = @(
    'Microsoft David Desktop',
    'Microsoft Mark Desktop',
    'Microsoft Zira Desktop',
    'Microsoft David',
    'Microsoft Mark',
    'Microsoft Zira'
)

$voices = $s.GetInstalledVoices() |
    Where-Object { $_.Enabled } |
    ForEach-Object { $_.VoiceInfo.Name }

$selected = $null
foreach ($wanted in $preferred) {
    $selected = $voices | Where-Object { $_ -eq $wanted } | Select-Object -First 1
    if ($selected) { break }
}

if ($selected) {
    $s.SelectVoice($selected)
}

$s.Rate = -1
$s.Volume = 100
$s.Speak($text)
$s.Dispose()
'''
            ps = ps.replace("'''ENCODED'''", encoded)

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
