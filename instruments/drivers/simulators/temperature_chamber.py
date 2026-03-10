"""
Temperature chamber driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting


class TemperatureChamber(DriverBase):

    name = "Temperature chamber simulator"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 17000, DriverSetting.CTRL_TEXT),
        DriverSetting("timeout", float, 0.2, DriverSetting.CTRL_TEXT)
    ]

    channels = [
        DriverChannel("get instrument ID"),
        DriverChannel("get actual temperature"),
        DriverChannel("get temperature setpoint"),
        DriverChannel("set temperature setpoint"),
        DriverChannel("get power state"),
        DriverChannel("set power state", False)
    ]

    is_simulator = True


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
