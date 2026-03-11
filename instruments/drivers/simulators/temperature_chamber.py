"""
Temperature chamber driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_udp import TransportUdp


class TemperatureChamber(DriverBase):

    name = "Temperature chamber simulator"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 17000, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("gid", "get instrument ID", str),
        DriverChannel("gat", "get actual temperature", float),
        DriverChannel("gts", "get temperature setpoint", float),
        DriverChannel("sts", "set temperature setpoint", str),
        DriverChannel("gps", "get power state", int),
        DriverChannel("sps", "set power state", int, False)
    ]

    transport = TransportUdp
    protocol = ProtocolAscii

    transport_settings = {
        "timeout": 0.5
    }

    protocol_settings = {
        "end_of_line": b"\n"
    }

    is_simulator = True

    def build_command(self, channel, value):
        if channel.channel_id == "gid":
            return b"id?"
        elif channel.channel_id == "gat":
            return b"temp?"
        elif channel.channel_id == "gts":
            return b"tset?"
        elif channel.channel_id == "sts":
            return f"temp={value:.1f}".encode("utf-8")
        elif channel.channel_id == "gps":
            return b"pwr?"
        elif channel.channel_id == "sps":
            return f"pwr={value}".encode("utf-8")
        else:
            raise ValueError(f"Channel '{channel.channel_id}' is not implemented in "
                             f"driver {self.get_class_name()}")

    def parse_response(self, channel, response):
        if channel.response_type is float:
            response = float(response)
        elif channel.response_type is int:
            response = int(response)
        elif channel.response_type is str:
            response = response.decode("utf-8")
        else:
            raise ValueError(f"Value type '{channel.response_type}' is not implemented in "
                             f"driver {self.get_class_name()}")
        return response


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
