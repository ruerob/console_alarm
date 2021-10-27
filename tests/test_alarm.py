import unittest
import time
import sys
sys.path.insert(0, "..")
import console_alarm


class PomodoroTestCase(unittest.TestCase):

    def test_start_pomodoro_with_to_few_seconds(self):
        with self.assertRaises(ValueError):
            console_alarm.start_pomodoro(0)

    def test_start_pomodoro_with_too_much_seconds(self):
        with self.assertRaises(ValueError):
            console_alarm.start_pomodoro(1440)

    def test_start_pomodoro_with_floating_values(self):
        with self.assertRaises(TypeError):
            console_alarm.start_pomodoro(1.5)

    def test_start_pomodoro_with_not_numeric_values(self):
        with self.assertRaises(TypeError):
            console_alarm.start_pomodoro("2")

    def test_start_pomodoro_without_values(self):
        with self.assertRaises(TypeError):
            console_alarm.start_pomodoro()

    def test_start_pomodoro_for_one_minute(self):
        timestamp: float = time.time()
        console_alarm.start_pomodoro(1)
        with self.subTest():
            self.assertLess(timestamp+60, time.time(), "Pomodoro started to fast.")
        with self.subTest():
            self.assertGreater(timestamp+66, time.time(), "Pomodoro ended to late.")

    def test_start_pomodoro_for_two_minutes(self):
        timestamp: float = time.time()
        console_alarm.start_pomodoro(2)
        with self.subTest():
            self.assertLess(timestamp+120, time.time(), "Pomodoro started to fast.")
        with self.subTest():
            self.assertGreater(timestamp+126, time.time(), "Pomodoro ended to late.")


class TestAlarmClock(unittest.TestCase):

    def start_alarm_clock_without_parameters(self):
        with self.assertRaises(ValueError):
            console_alarm.start_alarm_clock()


if __name__ == '__main__':
    unittest.main()
