"""
Driver for the TDS200 series oscilloscope.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.tektronix.oscilloscope_tds_base import TektronixOscilloscopeTdsBase


class TektronixOscilloscopeTds200(TektronixOscilloscopeTdsBase, DriverBase):

    id = "aa4795f6-0911-4dd8-bdef-7fc2e2dd9678"
    model = "TDS200(RS232)"
    description = "Tektronix oscilloscope TDS200 series using RS232"


if __name__ == "__main__":

    driver_test_settings = {
        "port": "COM4"
    }

    driver = TektronixOscilloscopeTds200(driver_test_settings, "DPT")
    driver.test_driver()
