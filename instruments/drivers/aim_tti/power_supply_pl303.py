"""
Driver for Aim-TTi PL303 power supply.
"""

from instruments.drivers.aim_tti.power_supply_base import AimTtiPowerSupplyBase
from instruments.drivers.driver_base import DriverBase


class AimTtiPowerSupplyPl303(AimTtiPowerSupplyBase, DriverBase):

    id = "f5e081d8-74dc-484a-847c-0a3b17cdc754"
    model = "PL303"
    description = "Aim-TTi power supply PL303, dual channel 15V/3A"


if __name__ == "__main__":

    # Add some test code here to test your driver

    # Override the default settings with some test settings if needed
    driver_test_settings = {
        "port": "COM5",
    }

    # Initialize the driver with debug enabled to see the debug output
    # "DPT": 'D': driver debug, 'P': protocol debug, 'T': transport debug
    driver = AimTtiPowerSupplyPl303(driver_test_settings, "DPT")
    driver.test_driver()
