import base64
import re
import subprocess
import threading


class WiseVoice:
    """Non-blocking Windows speech with PowerShell 5.1-compatible diagnostics."""

    PREFERRED_VOICES = (
        "Microsoft David Desktop",
        "Microsoft Mark Desktop",
        "Microsoft Zira Desktop",
        "Microsoft David",
        "Microsoft Mark",
        "Microsoft Zira",
    )

    def __init__(self):
        self._speech_lock = threading.Lock()
        print("WISE voice system initialized.")

    def remove_emojis(self, text):
        text = re.sub(
            r"[\U0001F300-\U0001FAFF]"
            r"|[\U00002700-\U000027BF]"
            r"|[\U00002600-\U000026FF]",
            "",
            str(text),
        )
        return re.sub(r"[ \t]+", " ", text).strip()

    def _prepare_text(self, text):
        text = self.remove_emojis(text)
        text = text.replace("—", ", ").replace("–", ", ")
        text = text.replace("•", ", ")
        return re.sub(r"\s+", " ", text).strip()

    def speak(self, text, on_start=None, on_finish=None):
        threading.Thread(
            target=self._speak,
            args=(text, on_start, on_finish),
            daemon=True,
        ).start()

    def _speak(self, text, on_start=None, on_finish=None):
        # Serialize speech requests so overlapping replies cannot speak at once.
        with self._speech_lock:
            self._speak_unlocked(text, on_start, on_finish)

    def _speak_unlocked(self, text, on_start=None, on_finish=None):
        try:
            speech_text = self._prepare_text(text)
            if not speech_text:
                return

            print("WISE VOICE:", speech_text)
            if on_start:
                on_start()

            # Base64 avoids PowerShell quoting problems and works in Windows
            # PowerShell 5.1 (unlike Convert.FromHexString, which is newer).
            encoded_text = base64.b64encode(
                speech_text.encode("utf-8")
            ).decode("ascii")

            preferred = list(self.PREFERRED_VOICES)
            preferred_ps = ", ".join(
                "'" + voice.replace("'", "''") + "'" for voice in preferred
            )

            ps_script = f"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {{
    $text = [System.Text.Encoding]::UTF8.GetString(
        [System.Convert]::FromBase64String('{encoded_text}')
    )
    $preferred = @({preferred_ps})
    $voices = $s.GetInstalledVoices() |
        Where-Object {{ $_.Enabled }} |
        ForEach-Object {{ $_.VoiceInfo.Name }}

    $selected = $null
    foreach ($wanted in $preferred) {{
        if ($voices -contains $wanted) {{
            $selected = $wanted
            break
        }}
    }}

    if ($selected) {{
        $s.SelectVoice($selected)
        Write-Output "WISE selected voice: $selected"
    }} else {{
        Write-Output "WISE warning: no preferred voice found; using system default."
    }}

    $s.Rate = -1
    $s.Volume = 100
    $s.Speak($text)
}} finally {{
    $s.Dispose()
}}
"""

            encoded_script = base64.b64encode(
                ps_script.encode("utf-16le")
            ).decode("ascii")

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-EncodedCommand",
                    encoded_script,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            if result.stdout.strip():
                print(result.stdout.strip())

            if result.returncode != 0:
                print("WISE POWERSHELL ERROR:", result.stderr.strip())
            else:
                print("WISE FINISHED SPEAKING")

        except subprocess.TimeoutExpired:
            print("VOICE ERROR: speech timed out after 120 seconds.")
        except Exception as error:
            print("VOICE ERROR:", repr(error))
        finally:
            if on_finish:
                try:
                    on_finish()
                except Exception as callback_error:
                    print("VOICE CALLBACK ERROR:", repr(callback_error))
