import unittest
import time
import sys
import io

sys.path.insert(0, "..")
from console_alarm import console_alarm

short_test = False


def output_contains_help(text: str) -> bool:
    return 'Small alarm function for your console.' in text


def get_console_redirect() -> io.StringIO:
    console_redirect = io.StringIO()
    sys.stdout = console_redirect
    return console_redirect


def clean_console_redirect():
    sys.stdout = sys.__stdout__


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
                start_time: float = time.time()
                console_alarm.start_pomodoro(minutes[minute_index])
                duration: float = time.time() - start_time
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
        start_time: float = time.time()
        alarm_time = time.localtime(start_time+60)
        console_alarm.start_alarm_clock(alarm_time.tm_hour, alarm_time.tm_min, alarm_time.tm_sec)
        duration = time.time() - start_time
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
        console_redirect: io.StringIO = get_console_redirect()
        start_time: float = time.time()
        console_alarm.ring(1)
        duration: float = time.time() - start_time
        clean_console_redirect()
        self.assertTrue("Wake up!!! <3" in console_redirect.getvalue())
        self.assertGreaterEqual(duration, 1)
        self.assertLessEqual(duration, 1.5)


class TestConsoleScriptEntryPoint(unittest.TestCase):

    def test_without_parameters(self):
        with self.assertRaises(TypeError):
            console_alarm.console_script_entry_point()

    def test_with_one_parameter(self):
        console_redirect: io.StringIO = get_console_redirect()
        console_alarm.console_script_entry_point([""])
        clean_console_redirect()
        self.assertTrue(output_contains_help(console_redirect.getvalue()))

    def test_with_wrong_parameter_types(self):
        wrong_types = [1, 1.1, [], [1, 2], {}, True]
        for type_index in range(len(wrong_types)):
            for arg_count in range(2):
                with self.subTest(type_index=type_index, arg_count=arg_count):
                    with self.assertRaises(TypeError):
                        args: list = [""]
                        if arg_count == 0:
                            args.append(wrong_types[type_index])
                        else:
                            args.append("2")
                        if arg_count == 1:
                            args.append(wrong_types[type_index])

                        console_alarm.console_script_entry_point(args)

    def test_with_wrong_string_parameters(self):
        wrong_strings = ["a", "1.1", "-1", ""]
        for string_index in range(len(wrong_strings)):
            for arg_count in range(2):
                with self.subTest(string_index=string_index, arg_count=arg_count):
                    args: list = [""]
                    if arg_count == 0:
                        args.append(wrong_strings[string_index])
                    else:
                        args.append("2")
                    if arg_count == 1:
                        args.append(wrong_strings[string_index])

                    console_redirect: io.StringIO = get_console_redirect()
                    console_alarm.console_script_entry_point(["", wrong_strings[string_index]])
                    clean_console_redirect()
                    self.assertTrue(output_contains_help(console_redirect.getvalue()))

    def test_with_to_much_parameters(self):
        some_parameters = ["a", "1.1", "-1", "", "45"]
        for parameter_index in range(len(some_parameters)):
            with self.subTest(parameter_index=parameter_index):
                console_redirect = get_console_redirect()
                console_alarm.console_script_entry_point(['', '10', '10', some_parameters[parameter_index]])
                clean_console_redirect()
                self.assertTrue(output_contains_help(console_redirect.getvalue()))

        some_parameters = [1, 1.1, [], [1, 2], {}, True]
        for parameter_index in range(len(some_parameters)):
            with self.subTest(parameter_index=parameter_index):
                with self.assertRaises(TypeError):
                    console_alarm.console_script_entry_point(["", "10", "10", some_parameters[parameter_index]])

        some_parameters = [1, 1.1, [], [1, 2], {}, True, "45"]
        for parameter_index in range(len(some_parameters)):
            with self.subTest(parameter_index=parameter_index):
                with self.assertRaises(TypeError):
                    console_alarm.console_script_entry_point(["", "10", "10"], some_parameters[parameter_index])

    @unittest.skipIf(short_test, "Skipped long tests.")
    def test_with_correct_parameter_one_second_index(self):
        console_redirect: io.StringIO = get_console_redirect()
        start_time: float = time.time()
        console_alarm.console_script_entry_point(["", "1"])
        duration: float = time.time() - start_time
        clean_console_redirect()
        self.assertTrue("Wake up!!! <3" in console_redirect.getvalue())
        self.assertLessEqual(duration, 66)
        self.assertGreaterEqual(duration, 60)

    @unittest.skipIf(short_test, "Skipped long tests.")
    def test_with_correct_parameter_one_third_index(self):
        console_redirect: io.StringIO = get_console_redirect()
        start_time: float = time.time()
        alarm_time = time.localtime(start_time+60)
        console_alarm.console_script_entry_point(["", "{}".format(alarm_time.tm_hour), "{}".format(alarm_time.tm_min)])
        duration: float = time.time() - start_time
        clean_console_redirect()
        self.assertTrue("Wake up!!! <3" in console_redirect.getvalue())
        self.assertLessEqual(duration, 66)
        self.assertGreaterEqual(duration, 1)
        self.assertLessEqual(time.localtime().tm_sec, 6)
        self.assertGreaterEqual(time.localtime().tm_sec, 0)


if __name__ == '__main__':
    unittest.main()
