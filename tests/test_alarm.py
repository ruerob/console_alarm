import unittest
import time
import sys

sys.path.insert(0, "..")
from console_alarm import console_alarm

short_test = False


class PomodoroTestCase(unittest.TestCase):

    def test_start_pomodoro_with_to_few_seconds(self):
        with self.assertRaises(ValueError):
            console_alarm.start_pomodoro(0)

    def test_start_pomodoro_with_too_much_seconds(self):
        with self.assertRaises(ValueError):
            console_alarm.start_pomodoro(1440)

    def test_start_pomodoro_with_wrong_value_types(self):
        wrong_types = ["a", "1", 1.1, [], [1, 2], {}, True]
        for type_index in range(len(wrong_types)):
            with self.subTest(type_index=type_index):
                with self.assertRaises(TypeError):
                    console_alarm.start_pomodoro(wrong_types[type_index])

    def test_start_pomodoro_without_values(self):
        with self.assertRaises(TypeError):
            console_alarm.start_pomodoro()

    def test_start_pomodoro_with_to_much_values(self):
        some_types = ["a", "1", 1.1, [], [1, 2], {}, True, 2]
        for type_index in range(len(some_types)):
            with self.subTest(type_index=type_index):
                with self.assertRaises(TypeError):
                    console_alarm.start_pomodoro(1, some_types[type_index])

    @unittest.skipIf(short_test, "Skipped long test")
    def test_start_pomodoro_for_some_minute(self):
        minutes = [1, 2]
        for minute_index in range(len(minutes)):
            with self.subTest(minute_index=minute_index):
                timestamp: float = time.time()
                console_alarm.start_pomodoro(minutes[minute_index])
                duration: float = time.time() - timestamp
                with self.subTest():
                    self.assertGreater(duration, 60*(minute_index+1), "Pomodoro started to fast.")
                with self.subTest():
                    self.assertLess(duration, 60*(minute_index+1)+6, "Pomodoro ended to late.")


class TestAlarmClock(unittest.TestCase):

    def test_start_alarm_clock_without_parameters(self):
        with self.assertRaises(TypeError):
            console_alarm.start_alarm_clock()

    def test_start_alarm_clock_with_to_much_parameters(self):
        some_types = ["a", "1", 1.1, [], [1, 2], {}, True, 2]
        for type_index in range(len(some_types)):
            with self.subTest(type_index=type_index):
                with self.assertRaises(TypeError):
                    console_alarm.start_alarm_clock(1, 1, 1, some_types[type_index])

    def test_start_alarm_clock_with_wrong_parameter_types(self):
        wrong_types = ["a", "1", 1.1, [], [1, 2], {}, True]

        for type_index in range(len(wrong_types)):
            for wrong_parameter in range(3):
                with self.subTest(typeIndex=type_index, wrong_parameter=wrong_parameter):
                    with self.assertRaises(TypeError):
                        console_alarm.start_alarm_clock(
                            wrong_types[type_index] if wrong_parameter == 0 else 2,
                            wrong_types[type_index] if wrong_parameter == 1 else 2,
                            wrong_types[type_index] if wrong_parameter == 2 else 2
                        )

    def test_start_alarm_clock_with_out_of_range_values(self):
        wrong_values = [[-1, -1], [24, 60]]
        for value_index in range(len(wrong_values)):
            for wrong_parameter in range(3):
                with self.subTest(value_index=value_index, wrong_parameter=wrong_parameter):
                    with self.assertRaises(ValueError):
                        console_alarm.start_alarm_clock(
                            wrong_values[value_index][0] if wrong_parameter == 0 else 2,
                            wrong_values[value_index][1] if wrong_parameter == 1 else 2,
                            wrong_values[value_index][1] if wrong_parameter == 2 else 2,
                        )

    @unittest.skipIf(short_test, "Skipped long test")
    def test_start_alarm_clock_for_one_minute(self):
        timestamp: float = time.time()
        alarm_time = time.localtime(timestamp+60)
        console_alarm.start_alarm_clock(alarm_time.tm_hour, alarm_time.tm_min, alarm_time.tm_sec)
        duration = time.time() - timestamp
        self.assertGreater(duration, 60)
        self.assertLess(duration, 66)


class TestRing(unittest.TestCase):

    def test_ring_without_parameter(self):
        with self.assertRaises(TypeError):
            console_alarm.ring()

    def test_ring_with_wrong_parameter_types(self):
        wrong_types = ["a", "1", 1.1, [], [1, 2], {}, True]
        for type_index in range(len(wrong_types)):
            with self.subTest(type_index=type_index):
                with self.assertRaises(TypeError):
                    console_alarm.ring(wrong_types[type_index])

    def test_ring_with_to_much_parameter(self):
        some_types = ["a", "1", 1.1, [], [1, 2], {}, True, 2]
        for type_index in range(len(some_types)):
            with self.subTest(type_index=type_index):
                with self.assertRaises(TypeError):
                    console_alarm.ring(1, some_types[type_index])

    def test_ring_with_out_of_range_values(self):
        out_of_range_values = [0, 61, -20]
        for value_index in range(len(out_of_range_values)):
            with self.subTest(value_index=value_index):
                with self.assertRaises(ValueError):
                    console_alarm.ring(out_of_range_values[value_index])

    def test_ring_with_correct_values(self):
        timestamp: float = time.time()
        console_alarm.ring(1)
        duration: float = time.time() - timestamp
        self.assertGreaterEqual(duration, 1)
        self.assertLessEqual(duration, 1.5)


if __name__ == '__main__':
    unittest.main()
