"""
Unit test for the time converter.
"""

from datetime import datetime

from src.models.time_converter import TimeConverter
from tests.lib.test_suite import TestSuite


class TimeConverterTest(TestSuite):

    _TEST_VALUES = [
        (    0,     0, "seconds", "00:00:00"),
        (   59,    59, "seconds", "00:00:59"),
        (   60,     1, "minutes", "00:01:00"),
        (   90,    90, "seconds", "00:01:30"),
        ( 3540,    59, "minutes", "00:59:00"),
        ( 3600,     1, "hours",   "01:00:00"),
        ( 3630,  3630, "seconds", "01:00:30"),
        ( 5400,    90, "minutes", "01:30:00"),
        (82800,    23, "hours",   "23:00:00"),
        (86400,     1, "days",    "1 days, 00:00:00"),
        (86430, 86430, "seconds", "1 days, 00:00:30"),
        (86460,  1441, "minutes", "1 days, 00:01:00"),
        (90000,    25, "hours",   "1 days, 01:00:00")
    ]

    def test_convert_seconds_to_time_with_unit(self):
        for test_value in self._TEST_VALUES:
            self.log.debug(f"Test value: {test_value[0]} seconds")
            value, unit = TimeConverter.convert_seconds_to_time_with_unit(test_value[0])
            self.log.debug(f"Result: {value}, {unit}")
            self.fail_if(value != test_value[1],
                         f"Invalid value. Expected: {test_value[1]}")
            self.fail_if(unit != test_value[2],
                         f"Invalid value. Expected: {test_value[2]}")

    def test_convert_time_with_unit_to_seconds(self):
        for test_value in self._TEST_VALUES:
            self.log.debug(f"Test values: {test_value[1]}, {test_value[2]}")
            value = TimeConverter.convert_time_with_unit_to_seconds(test_value[1], test_value[2])
            self.log.debug(f"Result: {value} seconds")
            self.fail_if(value != test_value[0],
                         f"Invalid value. Expected: {test_value[0]}")

    def test_create_duration_time_string(self):
        for test_value in self._TEST_VALUES:
            self.log.debug(f"Test value: {test_value[0]} seconds")
            value = TimeConverter.create_duration_time_string(test_value[0])
            self.log.debug(f"Result: {value}")
            self.fail_if(value != test_value[3],
                         f"Invalid value. Expected: {test_value[3]}")

    def test_get_timestamp(self):
        expected = datetime.now().strftime("%Y%m%d %H%M%S")
        value = TimeConverter.get_timestamp()
        self.log.debug(f"Result: {value}")
        self.fail_if(value != expected, f"Invalid timestamp. Expected: {expected}")


if __name__ == "__main__":

    TimeConverterTest().run(True)
