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


if __name__ == "__main__":
    unittest.main()
