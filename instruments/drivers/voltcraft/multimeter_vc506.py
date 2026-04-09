"""
Driver for multimeter Voltcraft VC506.
"""

import re

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting

from instruments.transport.transport_serial import TransportSerial
from instruments.protocol.protocol_ascii import ProtocolAscii


class VoltcraftVC506(DriverBase):

    # Generate a valid ID using the driver_id.py script
    id = "2ecb8f48-2fb1-49e6-a3cc-a5d7bf489f2c"
    name = "Voltcraft VC506"
    description = "Multimeter Voltcraft VC506 "

    driver_settings = [
        DriverSetting("port", str, "", DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("meas", "get measurement", [], None, float),
    ]

    transport = TransportSerial
    protocol = ProtocolAscii

    transport_settings = {
        "baudrate": 1200,
        "bytesize": 7,
        "stopbits": 2,
        "timeout": 2,
        # The internal serial interface of the multimeter is powered by the RTS and DTR signals
        "rts": False,
        "dtr": True
    }

    protocol_settings = {
        "end_of_line": b"\r"
    }

    def build_command(self, _channel, _value):
        # We don't need a command, just send end of line
        return b""

    def parse_response(self, channel, response):
        return channel.response_type(re.search(rb'[-+]?\d*\.?\d+', response).group())

    def test_driver(self):
        response = self.process_channel("meas")
        if not isinstance(response, float):
            raise Exception(f"Invalid response: {response}")


if __name__ == "__main__":

    # Add some test code here to test your driver

    # Override the default settings with some test settings if needed
    driver_test_settings = {
        "port": "COM7"
    }

    # Initialize the driver with debug enabled to see the debug output
    # "DPT": 'D': driver debug, 'P': protocol debug, 'T': transport debug
    try:
        driver = VoltcraftVC506(driver_test_settings, "DPT")
        driver.test_driver()
    finally:
        driver.close()
