"""
Base driver for the Tektronics TDS series oscilloscopes.
"""

import time

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_serial import TransportSerial


class TektronixOscilloscopeTdsBase:

    manufacturer = "Tektronix"

    driver_settings = [
        DriverSetting("port", str, "", DriverSetting.CTRL_TEXT),
        DriverSetting("baudrate", int, 9600, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("gid", "get instrument ID", None, str),
        DriverChannel("mfr", "get frequency", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("mpd", "get period time", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("mmn", "get mean voltage", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("mpp", "get peak-peak voltage", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("mrm", "get RMS per cycle voltage", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
    ]

    transport = TransportSerial
    protocol = ProtocolAscii

    transport_settings = {
    }

    protocol_settings = {
        "end_of_line": b"\n"
    }

    internal_channels = [
        DriverChannel("dim", "set disable measurement", str, None, False, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("sou", "set measurement source", str, None, False, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT),
        ]),
        DriverChannel("typ", "set measurement type", str, None, False)
    ]

    # It takes about this time before a measurment is ready
    MEASUREMENT_DELAY = 1.2

    def init_driver(self):
        for channel in range(1, 5):
            self.process_channel("dim", {                           # pylint: disable=no-member
                "channel": channel,
                "value": b"none"
            })

    def setup_channel(self, params):
        self.process_channel("sou", params)                         # pylint: disable=no-member
        self.process_channel("typ", params)                         # pylint: disable=no-member
        time.sleep(self.MEASUREMENT_DELAY)

    def build_command(self, channel, params):
        match channel.channel_id:
            case "gid":
                return b"id?"
            case "dim":
                return b"measu:meas%d:typ %s" % (params["channel"], params["value"])
            case "sou":
                return b"measu:meas1:sou ch%d" % params["channel"]
            case "typ":
                return b"measu:meas1:typ %s" % params["value"]
            case "mfr":
                # Setup channel before measurement
                params["value"] = b"freq"
                self.setup_channel(params)
                # Do measurement
                return b"measu:meas1:val?"
            case "mpd":
                # Setup channel before measurement
                params["value"] = b"peri"
                self.setup_channel(params)
                # Do measurement
                return b"measu:meas1:val?"
            case "mmn":
                # Setup channel before measurement
                params["value"] = b"mean"
                self.setup_channel(params)
                # Do measurement
                return b"measu:meas1:val?"
            case "mpp":
                # Setup channel before measurement
                params["value"] = b"pk2"
                self.setup_channel(params)
                # Do measurement
                return b"measu:meas1:val?"
            case "mrm":
                # Setup channel before measurement
                params["value"] = b"crm"
                self.setup_channel(params)
                # Do measurement
                return b"measu:meas1:val?"

        raise ValueError(f"Channel '{channel.channel_id}' is not implemented in "
                         f"driver {self.get_class_name()}")         # pylint: disable=no-member

    def parse_response(self, channel, response):
        if channel.response_type is str:
            return response.decode("utf-8")
        if channel.response_type in [float, int]:
            return channel.response_type(response)

        raise ValueError(f"Value type '{channel.response_type}' is not implemented in "
                         f"driver {self.get_class_name()}")         # pylint: disable=no-member

    def test_driver(self):
        response = self.process_channel("gid")                      # pylint: disable=no-member
        if not response.startswith("ID TEK/TDS"):
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    from instruments.drivers.driver_base import DriverBase

    class TektronixOscilloscopeTdsBaseTest(TektronixOscilloscopeTdsBase, DriverBase):

        id = "c7713252-0da1-495a-bc8f-713fcd2d475d"
        model = "Base class test"
        description = "Base class test"


    driver_test_settings = {
        "port": "COM4"
    }

    driver = TektronixOscilloscopeTdsBaseTest(driver_test_settings)
    driver.test_driver()

    for ch in range(1, 3):
        print(f"Test CH{ch}:")
        print(f"CH {ch} frequency        :", driver.process_channel("mfr", {"channel": ch}))
        print(f"CH {ch} period time      :", driver.process_channel("mpd", {"channel": ch}))
        print(f"CH {ch} mean voltage     :", driver.process_channel("mmn", {"channel": ch}))
        print(f"CH {ch} peak-peak voltage:", driver.process_channel("mpp", {"channel": ch}))
        print(f"CH {ch} RMS voltage      :", driver.process_channel("mrm", {"channel": ch}))
