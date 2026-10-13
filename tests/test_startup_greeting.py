import unittest
from datetime import datetime

from interface import WiseInterface


class StartupGreetingTests(unittest.TestCase):
    def test_greeting_uses_expected_local_time_period(self):
        cases = (
            (datetime(2026, 10, 13, 5, 0), "this fine morning"),
            (datetime(2026, 10, 13, 7, 59), "this fine morning"),
            (datetime(2026, 10, 13, 8, 0), "this morning"),
            (datetime(2026, 10, 13, 11, 59), "this morning"),
            (datetime(2026, 10, 13, 12, 0), "this afternoon"),
            (datetime(2026, 10, 13, 16, 59), "this afternoon"),
            (datetime(2026, 10, 13, 17, 0), "this evening"),
            (datetime(2026, 10, 13, 20, 59), "this evening"),
            (datetime(2026, 10, 13, 21, 0), "tonight"),
            (datetime(2026, 10, 13, 0, 0), "tonight"),
        )

        for now, period in cases:
            with self.subTest(hour=now.hour, minute=now.minute):
                greeting = WiseInterface._opening_greeting(now)
                self.assertEqual(
                    greeting,
                    f"Hello, Master Wisdom! What can I do for you {period}?",
                )


if __name__ == "__main__":
    unittest.main()
