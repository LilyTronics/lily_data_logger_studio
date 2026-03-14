"""
Unit test for serial port model.
"""

from src.models.serial_ports import get_available_serial_ports
from tests.lib.test_suite import TestSuite


class SerialPortTest(TestSuite):

    def test_get_available_serial_ports(self):
        ports = get_available_serial_ports()
        self.log.debug(f"Available serial ports: {ports}")
        self.fail_if(not isinstance(ports, list), "Expected a list of available serial ports")


if __name__ == "__main__":

    SerialPortTest().run(True)
