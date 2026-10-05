import json
import os
import threading
import urllib.parse
import urllib.request
from datetime import datetime, timezone


class WiseEnvironment:
    """Live time, sunrise/sunset, weather and scene data for WISE."""

    DEFAULT_LOCATION = "Nairobi, Kenya"
    DEFAULT_LATITUDE = -1.286389
    DEFAULT_LONGITUDE = 36.817223

    def __init__(self, on_update=None):
        self.on_update = on_update
        self.location_name = os.getenv("WISE_LOCATION", self.DEFAULT_LOCATION)
        self.latitude = self._float_env("WISE_LATITUDE", self.DEFAULT_LATITUDE)
        self.longitude = self._float_env("WISE_LONGITUDE", self.DEFAULT_LONGITUDE)

        self.temperature = None
        self.weather_code = None
        self.weather_text = "Weather unavailable"
        self.sunrise = None
        self.sunset = None
        self.scene = "night"
        self.last_update = None
        self._busy = False
        self._lock = threading.Lock()

    def _float_env(self, name, fallback):
        try:
            return float(os.getenv(name, fallback))
        except (TypeError, ValueError):
            return fallback

    def refresh_async(self):
        with self._lock:
            if self._busy:
                return
            self._busy = True
        threading.Thread(target=self._refresh, daemon=True).start()

    def _refresh(self):
        try:
            params = urllib.parse.urlencode({
                "latitude": self.latitude,
                "longitude": self.longitude,
                "current": "temperature_2m,weather_code",
                "daily": "sunrise,sunset",
                "timezone": "auto",
                "forecast_days": 1,
                "temperature_unit": "celsius",
            })
            url = "https://api.open-meteo.com/v1/forecast?" + params
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "WISE-AI/1.0"},
            )
            with urllib.request.urlopen(request, timeout=8) as response:
                data = json.loads(response.read().decode("utf-8"))

            current = data.get("current", {})
            daily = data.get("daily", {})
            self.temperature = current.get("temperature_2m")
            self.weather_code = current.get("weather_code")
            self.weather_text = self._weather_text(self.weather_code)

            sunrise = (daily.get("sunrise") or [None])[0]
            sunset = (daily.get("sunset") or [None])[0]
            self.sunrise = self._parse_local(sunrise)
            self.sunset = self._parse_local(sunset)
            self.last_update = datetime.now()
        except Exception as error:
            print("WISE ENVIRONMENT ERROR:", error)
        finally:
            self._update_scene()
            with self._lock:
                self._busy = False
            if self.on_update:
                try:
                    self.on_update(self.snapshot())
                except Exception as error:
                    print("WISE ENVIRONMENT CALLBACK ERROR:", error)

    def _parse_local(self, value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def _update_scene(self):
        now = datetime.now()
        if self.sunrise and self.sunset:
            sunrise = self.sunrise.replace(tzinfo=None)
            sunset = self.sunset.replace(tzinfo=None)
            if now < sunrise:
                self.scene = "night"
            elif now < sunrise.replace(hour=min(23, sunrise.hour + 1)):
                self.scene = "sunrise"
            elif now < sunset.replace(hour=max(0, sunset.hour - 1)):
                self.scene = "day"
            elif now < sunset:
                self.scene = "sunset"
            elif now < sunset.replace(hour=min(23, sunset.hour + 2)):
                self.scene = "evening"
            else:
                self.scene = "night"
        else:
            self.scene = "day" if 6 <= now.hour < 18 else "night"

    def tick(self):
        self._update_scene()
        return self.snapshot()

    def snapshot(self):
        self._update_scene()
        return {
            "location": self.location_name,
            "temperature": self.temperature,
            "weather_code": self.weather_code,
            "weather": self.weather_text,
            "sunrise": self.sunrise,
            "sunset": self.sunset,
            "scene": self.scene,
            "time": datetime.now(),
            "last_update": self.last_update,
        }

    @staticmethod
    def _weather_text(code):
        labels = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Drizzle",
            55: "Heavy drizzle",
            61: "Light rain",
            63: "Rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Snow",
            75: "Heavy snow",
            80: "Rain showers",
            81: "Rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm",
            99: "Thunderstorm",
        }
        return labels.get(code, "Weather unavailable")
