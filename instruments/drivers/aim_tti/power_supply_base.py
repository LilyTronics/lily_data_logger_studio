"""
Base class for Aim-TTi power supplies.
"""

import re

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting
from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_serial import TransportSerial


class AimTtiPowerSupplyBase:

    # Generate a valid ID using the driver_id.py script
    manufacturer = "Aim-TTi"

    # The only settings that is required is the port.
    driver_settings = [
        DriverSetting("port", str, "", DriverSetting.CTRL_TEXT)
    ]

    channels = [
        DriverChannel("gid", "get instrument ID", None, str),
        DriverChannel("gav", "get actual output voltage", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("gac", "get actual output current", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("gsv", "get output set voltage", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("gsc", "get output set current", None, float, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("sov", "set output voltage", float, str, False, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("soc", "set output current", float, str, False, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("gos", "get output state", None, int, True, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("sos", "set output state", int, str, False, [
            DriverSetting("channel", int, 1, DriverSetting.CTRL_TEXT)
        ]),
        DriverChannel("sas", "set all output state", int, str, False),
    ]

    transport = TransportSerial
    protocol = ProtocolAscii

    transport_settings = {
    }

    protocol_settings = {
        "end_of_line": b"\r\n"
    }

    def build_command(self, channel, params):
        match channel.channel_id:
            case "gid":
                return b"*IDN?"
            case "gav":
                return b"V%dO?" % params["channel"]
            case "gac":
                return b"I%dO?" % params["channel"]
            case "gsv":
                return b"V%d?" % params["channel"]
            case "gsc":
                return b"I%d?" % params["channel"]
            case "sov":
                return b"V%d %f" % (params["channel"], params["value"])
            case "soc":
                return b"I%d %f" % (params["channel"], params["value"])
            case "gos":
                return b"OP%d?" % params["channel"]
            case "sos":
                return b"OP%d %d" % (params["channel"], params["value"])
            case "sas":
                return b"OPALL %d" % params["value"]

        raise ValueError(f"Channel '{channel.channel_id}' is not implemented in "
                         f"driver {self.get_class_name()}")         # pylint: disable=no-member

    def parse_response(self, channel, response):
        if channel.response_type is str:
            return response.decode("utf-8")
        if channel.response_type in [float, int]:
            response = response.split(b" ")[-1]
            return channel.response_type(re.search(rb"[-+]?\d*\.?\d+", response).group())

        raise ValueError(f"Value type '{channel.response_type}' is not implemented in "
                         f"driver {self.get_class_name()}")         # pylint: disable=no-member

    def test_driver(self):
        response = self.process_channel("gid")                      # pylint: disable=no-member
        if not response.startswith("THURLBY THANDAR"):
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    import time

    from instruments.drivers.driver_base import DriverBase

    class PowerSupplyBaseTest(AimTtiPowerSupplyBase, DriverBase):

        id = "ff6bdbc9-6f12-402f-9320-55a5a80a7a8b"
        model = "driver test"
        description = "Test for the power supply base driver"

    # Override the default settings with some test settings if needed
    driver_test_settings = {
        "port": "COM5",
    }

    # Initialize the driver with debug enabled to see the debug output
    # "DPT": 'D': driver debug, 'P': protocol debug, 'T': transport debug
    driver = PowerSupplyBaseTest(driver_test_settings)
    driver.test_driver()

    for ch in range(1, 3):
        voltage = driver.process_channel("gsv", {"channel": ch})
        current = driver.process_channel("gsc", {"channel": ch})
        print(f"CH{ch} voltage set point:", voltage)
        print(f"CH{ch} current set point:", current)
        voltage -= 0.1
        current -= 0.1
        driver.process_channel("sov", {"channel": ch, "value": voltage})
        driver.process_channel("soc", {"channel": ch, "value": current})
        print(f"CH{ch} voltage set point:", driver.process_channel("gsv", {"channel": ch}))
        print(f"CH{ch} current set point:", driver.process_channel("gsc", {"channel": ch}))
        print(f"CH{ch} actual voltage   :", driver.process_channel("gav", {"channel": ch}))
        print(f"CH{ch} actual current   :", driver.process_channel("gac", {"channel": ch}))
        print(f"CH{ch} output state     :", driver.process_channel("gos", {"channel": ch}))
        driver.process_channel("sos", {"channel": ch, "value": 1})
        print(f"CH{ch} output state     :", driver.process_channel("gos", {"channel": ch}))
        time.sleep(0.5)
        print(f"CH{ch} actual voltage   :", driver.process_channel("gav", {"channel": ch}))
        print(f"CH{ch} actual current   :", driver.process_channel("gac", {"channel": ch}))

    driver.process_channel("sas", {"value": 0})
    time.sleep(0.5)
    for ch in range(1, 3):
        print(f"CH{ch} output state     :", driver.process_channel("gos", {"channel": ch}))
        print(f"CH{ch} actual voltage   :", driver.process_channel("gav", {"channel": ch}))
        print(f"CH{ch} actual current   :", driver.process_channel("gac", {"channel": ch}))
