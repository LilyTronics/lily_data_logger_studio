"""
Mulit channel analog IO driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_tcp import TransportTcp


class MultiChannelAnalogIo(DriverBase):

    id = "24debf6c-9022-45cf-9900-99913c382dee"
    name = "Multi channel analog IO simulator"
    description = "Simulates a multi channel analog IO device with ASCII protocol over IP/TCP"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 51100, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("gid", "get instrument ID", None, str),
        DriverChannel("so", "set output", float, str, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("gi", "get input", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ])
    ]

    transport = TransportTcp
    protocol = ProtocolAscii

    transport_settings = {
        "timeout": 2
    }

    protocol_settings = {
        "end_of_line": b"\n"
    }

    is_simulator = True

    def build_command(self, channel, params):
        value = params.get("value", None)
        ch = params.get("channel", None)

        match channel.channel_id:
            case "gid":
                return b"id?"
            case "so":
                if None in (channel, value):
                    raise ValueError(f"Wrong values for channel and or value: {ch}, {value}")
                return b"so,%d,%f" % (ch, value)
            case "gi":
                if channel is None:
                    raise ValueError(f"Wrong value for channel: {ch}")
                return b"gi,%d" % ch

        raise ValueError(f"Channel '{channel.channel_id}' is not implemented in "
                            f"driver {self.get_class_name()}")

    def parse_response(self, channel, response):
        if channel.response_type is str:
            return response.decode("utf-8")
        if channel.response_type in [float, int]:
            return channel.response_type(response)

        raise ValueError(f"Value type '{channel.response_type}' is not implemented in "
                         f"driver {self.get_class_name()}")

    def test_driver(self):
        response = self.process_channel("gid")
        if response.lower() != "multi channel analog io":
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_analog_io_test import DriverAnalogIoTest

    DriverAnalogIoTest().run()
