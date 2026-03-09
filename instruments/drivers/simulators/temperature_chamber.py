"""
Temperature chamber driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_settings import DriverSetting


class TemperatureChamber(DriverBase):

    name = "Temperature chamber simulator"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 17000, DriverSetting.CTRL_TEXT),
        DriverSetting("timeout", float, 0.2, DriverSetting.CTRL_TEXT)
    ]

    is_simulator = True
