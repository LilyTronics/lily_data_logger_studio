"""
Driver for the TDS2000 series oscilloscope.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.tektronix.oscilloscope_tds_base import TektronixOscilloscopeTdsBase


class TektronixOscilloscopeTds200(TektronixOscilloscopeTdsBase, DriverBase):

    id = "477b7c01-9f41-4b27-baf4-b441296cfca8"
    model = "TDS2000 (RS232)"
    description = "Tektronix oscilloscope TDS2000 series using RS232"


if __name__ == "__main__":

    driver_test_settings = {
        "port": "COM4"
    }

    driver = TektronixOscilloscopeTds200(driver_test_settings, "DPT")
    driver.test_driver()
