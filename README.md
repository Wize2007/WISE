# WISE — Your AI Companion

WISE is a Python desktop companion built with Tkinter. Its current interface combines a glowing Golden Star, text conversation, Windows speech output, memory, and a time/weather-aware environment.

## Requirements

- Windows with Python 3.13 or 3.14
- Tkinter (included with the standard Windows Python installer)
- PowerShell and the Windows System.Speech components for spoken output
- Internet access for live weather and sunrise/sunset data; the interface remains usable if the weather service is unavailable

The core application uses Python's standard library and does not currently require a third-party dependency installation.

## Run WISE

Open PowerShell in the repository folder and run:

```powershell
python main.py
```

The memory module resolves its default data path relative to the project, not the shell's current working directory.

## Configuration

The environment defaults to Nairobi, Kenya. You can override the location using these environment variables before launch:

- `WISE_LOCATION`
- `WISE_LATITUDE`
- `WISE_LONGITUDE`

## Foundation checks

Run the offline test suite:

```powershell
python -m compileall -q main.py interface.py brain tests
python -m unittest discover -s tests -v
```

Tests use temporary files and do not intentionally modify `data/memories.json`. Voice tests cover text preparation without invoking PowerShell or requiring audio hardware. Weather tests do not make network requests.

## Project safeguards

- Keep `data/memories.json` and local backups safe.
- Do not commit secrets, personal tokens, or local environment files.
- Python cache files and virtual environments are ignored by Git.
- Visual appearance changes should preserve the Golden Star, voice, memory, clock/date, weather, and existing scene transitions.
