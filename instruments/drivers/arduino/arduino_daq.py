"""
Driver for the Arduino DAQ.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting

from instruments.transport.transport_serial import TransportSerial
from instruments.protocol.protocol_ascii import ProtocolAscii


class ArduinoDaq(DriverBase):

    id = "c7a393e0-8838-4e58-8170-4bd96bf3ef00"
    manufacturer = "Arduino"
    model = "DAQ"
    description = "Basic DAQ using an Arduino board"

    transport = TransportSerial
    protocol = ProtocolAscii

    driver_settings = [
        DriverSetting("port", str, "", DriverSetting.CTRL_TEXT)
    ]

    transport_settings = {
        "timeout": 1,
        "baudrate": 115200,
    }

    protocol_settings = {
    }
    # End settings

    channels = [
        DriverChannel("get_id", "get instrument ID", None, str),
        DriverChannel("get_ana", "get analog channel", None, float, True, [
            DriverSetting("channel", int, None, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("get_dig", "get digital channel", None, int, True, [
            DriverSetting("channel", int, None, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("set_dig", "set digital channel", int, str, True, [
            DriverSetting("channel", int, None, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("set_inp", "set digital channel as input", None, str, True, [
            DriverSetting("channel", int, None, DriverSetting.CTRL_TEXT)
        ])
    ]
    # End channels

    def init_driver(self):
        # When opening the port for the first time the Arduino will reset
        # So we try to do the driver test a couple of times until passed.
        n = 4
        while n > 0:
            try:
                self.test_driver()
                break
            except:
                pass
            n -= 1
        else:
            raise AssertionError("Could not initialize the driver")

    def build_command(self, channel, params):
        match channel.channel_id:
            case "get_id":
                return b"id"
            case "get_ana":
                return b"ra%d" % params["channel"]
            case "get_dig":
                return b"rd%d" % params["channel"]
            case "set_dig":
                return b"wd%d %d" % (params["channel"], params["value"])
            case "set_inp":
                return b"si%d" % params["channel"]

        raise ValueError(f"Channel '{channel.channel_id}' is not implemented in "
                         f"driver {self.get_class_name()}")         # pylint: disable=no-member

    def parse_response(self, channel, response):
        if channel.response_type is str:
            return response.decode("utf-8")
        if channel.response_type in [float, int]:
            return channel.response_type(response)

        raise ValueError(f"Value type '{channel.response_type}' is not implemented in "
                         f"driver {self.get_class_name()}")

    def test_driver(self):
        response = self.process_channel("get_id")
        if response != "Arduino DAQ":
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    # Override the default settings with some test settings
    driver_test_settings = {
        "port": "COM9"
    }

    # Initialize the driver with debug enabled to see the debug output
    # "DPT": 'D': driver debug, 'P': protocol debug, 'T': transport debug
    driver = ArduinoDaq(driver_test_settings, "DPT")
    driver.test_driver()

    print(driver.process_channel("get_ana", {"channel": 0}))
    print(driver.process_channel("get_dig", {"channel": 2}))
    print(driver.process_channel("set_dig", {"channel": 2, "value": 1}))
    print(driver.process_channel("set_inp", {"channel": 2}))
