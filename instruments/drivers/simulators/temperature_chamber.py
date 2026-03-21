"""
Temperature chamber driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_udp import TransportUdp


class TemperatureChamber(DriverBase):

    id = "e5662459-c10d-4616-aa97-978024a825d0"
    name = "Temperature chamber simulator"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 51000, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("gid", "get instrument ID", [], str),
        DriverChannel("gat", "get actual temperature", [], float),
        DriverChannel("gts", "get temperature setpoint", [], float),
        DriverChannel("sts", "set temperature setpoint", [], str),
        DriverChannel("gps", "get power state", [], int),
        DriverChannel("sps", "set power state", [], int, False)
    ]

    transport = TransportUdp
    protocol = ProtocolAscii

    transport_settings = {
        "timeout": 2
    }

    protocol_settings = {
        "end_of_line": b"\n"
    }

    is_simulator = True

    def build_command(self, channel, value):
        match channel.channel_id:
            case "gid":
                return b"id?"
            case "gat":
                return b"temp?"
            case "gts":
                return b"tset?"
            case "sts":
                return f"temp={value:.1f}".encode("utf-8")
            case "gps":
                return b"pwr?"
            case "sps":
                return f"pwr={value}".encode("utf-8")

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
        if response.lower() != "temperature chamber":
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
