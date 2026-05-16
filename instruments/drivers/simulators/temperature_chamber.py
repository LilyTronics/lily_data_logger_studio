"""
Temperature chamber driver.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_udp import TransportUdp


class TemperatureChamber(DriverBase):

    id = "e5662459-c10d-4616-aa97-978024a825d0"
    manufacturer = "Simulator"
    model = "temperature chamber"
    description = "Simulates a temperature chamber with ASCII protocol over IP/UDP"

    driver_settings = [
        DriverSetting("host", str, "localhost", DriverSetting.CTRL_TEXT),
        DriverSetting("port", int, 51000, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("get_id", "get instrument ID", None, str),
        DriverChannel("get_act_temp", "get actual temperature", None, float),
        DriverChannel("get_temp_set", "get temperature setpoint", None, float),
        DriverChannel("set_temp_set", "set temperature setpoint", float, str),
        DriverChannel("get_pwr_state", "get power state", None, int),
        DriverChannel("set_pwr_state", "set power state", int, None, False)
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

    def build_command(self, channel, params):
        value = params.get("value", None)
        if value is not None and channel.value_type is not None:
            value = channel.value_type(value)

        match channel.channel_id:
            case "get_id":
                return b"id?"
            case "get_act_temp":
                return b"temp?"
            case "get_temp_set":
                return b"tset?"
            case "set_temp_set":
                if value is None:
                    raise ValueError("Invalid value")
                return f"temp={value:.1f}".encode("utf-8")
            case "get_pwr_state":
                return b"pwr?"
            case "set_pwr_state":
                if value is None:
                    raise ValueError("Invalid value")
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
        response = self.process_channel("get_id")
        if response != "Simulator Temperature Chamber":
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
