"""
Module with time converter functions.
"""

import time

from datetime import datetime


class TimeConverter:

    TIME_UNIT_TO_FACTOR = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
    TIME_UNITS = list(TIME_UNIT_TO_FACTOR.keys())
    _TIMESTAMP_FORMAT = "%Y%m%d %H%M%S"

    @staticmethod
    def create_duration_time_string(seconds):
        d, h = divmod(seconds, 86400)
        m, s = divmod(h, 60)
        h, m = divmod(m, 60)
        output = ""
        if d > 0:
            output = f"{d} days, "
        output += f"{h:02}:{m:02}:{s:02}"
        return output

    @classmethod
    def convert_seconds_to_time_with_unit(cls, seconds):
        factor = 1
        if seconds > 0:
            for factor in sorted(cls.TIME_UNIT_TO_FACTOR.values(), reverse=True):
                if seconds > 0 and seconds % factor == 0:
                    break
        unit = list(cls.TIME_UNIT_TO_FACTOR.keys())[list(
            cls.TIME_UNIT_TO_FACTOR.values()).index(factor)]
        return int(seconds / factor), unit

    @classmethod
    def convert_time_with_unit_to_seconds(cls, value, unit):
        if value > 0:
            matches = list(filter(lambda x: x == unit, cls.TIME_UNIT_TO_FACTOR.keys()))
            if len(matches) == 1:
                value *= cls.TIME_UNIT_TO_FACTOR[matches[0]]
        return value

    @classmethod
    def get_timestamp(cls, timestamp=time.time()):
        return datetime.fromtimestamp(timestamp).strftime(cls._TIMESTAMP_FORMAT)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.time_converter_test import TimeConverterTest

    TimeConverterTest().run(True)
