import unittest
from datetime import datetime
from unittest.mock import patch

from brain.environment import WiseEnvironment


class WiseEnvironmentTests(unittest.TestCase):
    def test_weather_codes_have_safe_fallback(self):
        self.assertEqual(WiseEnvironment._weather_text(0), "Clear sky")
        self.assertEqual(
            WiseEnvironment._weather_text(999),
            "Weather unavailable",
        )
        self.assertEqual(
            WiseEnvironment._weather_text(None),
            "Weather unavailable",
        )

    def test_tick_uses_local_time_fallback_when_sun_data_is_missing(self):
        environment = WiseEnvironment()
        with patch("brain.environment.datetime") as clock:
            clock.now.return_value = datetime(2026, 5, 1, 12, 0)
            snapshot = environment.tick()

        self.assertEqual(snapshot["scene"], "day")
        self.assertIsNone(snapshot["temperature"])
        self.assertEqual(snapshot["weather"], "Weather unavailable")
        self.assertEqual(snapshot["location"], environment.location_name)

    def test_sunrise_and_sunset_data_selects_expected_scenes(self):
        environment = WiseEnvironment()
        environment.sunrise = datetime(2026, 5, 1, 6, 0)
        environment.sunset = datetime(2026, 5, 1, 18, 0)
        cases = (
            (datetime(2026, 5, 1, 5, 0), "night"),
            (datetime(2026, 5, 1, 6, 30), "sunrise"),
            (datetime(2026, 5, 1, 12, 0), "day"),
            (datetime(2026, 5, 1, 17, 30), "sunset"),
            (datetime(2026, 5, 1, 19, 0), "evening"),
            (datetime(2026, 5, 1, 21, 0), "night"),
        )

        for current_time, expected_scene in cases:
            with self.subTest(time=current_time, scene=expected_scene):
                with patch("brain.environment.datetime") as clock:
                    clock.now.return_value = current_time
                    self.assertEqual(environment.tick()["scene"], expected_scene)

    def test_network_failure_keeps_weather_unavailable_and_releases_refresh_lock(self):
        environment = WiseEnvironment()
        with patch("brain.environment.urllib.request.urlopen", side_effect=OSError("offline")):
            environment._refresh()

        self.assertIsNone(environment.temperature)
        self.assertEqual(environment.weather, "Weather unavailable")
        self.assertFalse(environment._busy)


if __name__ == "__main__":
    unittest.main()
