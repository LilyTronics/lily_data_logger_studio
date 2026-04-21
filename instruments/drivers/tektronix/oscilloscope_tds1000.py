"""
Driver for the TDS1000 series oscilloscope.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.tektronix.oscilloscope_tds_base import TektronixOscilloscopeTdsBase


class TektronixOscilloscopeTds200(TektronixOscilloscopeTdsBase, DriverBase):

    id = "f1c1b4e1-5f27-4b46-baa8-99b6d90fa40b"
    model = "TDS1000 (RS232)"
    description = "Tektronix oscilloscope TDS1000 series using RS232"


if __name__ == "__main__":

    driver_test_settings = {
        "port": "COM4"
    }

    driver = TektronixOscilloscopeTds200(driver_test_settings, "DPT")
    driver.test_driver()
