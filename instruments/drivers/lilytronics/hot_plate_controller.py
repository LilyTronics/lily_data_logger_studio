"""
Driver for the LilyTronics hot plate controller.
"""

from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting

from instruments.protocol.protocol_ascii import ProtocolAscii
from instruments.transport.transport_serial import TransportSerial


class LilyHotPlateController(DriverBase):

    id = "3464c377-f433-4e3d-b012-4821aef4bd33"
    manufacturer = "LilyTronics"
    model = "Hot plate controller"
    description = "LilyTronics hot plate controller 20-400 degrees Celcius"

    driver_settings = [
        DriverSetting("port", str, "", DriverSetting.CTRL_TEXT)
    ]

    channels = [
        DriverChannel("get_id", "get instrument ID", None, str),
        DriverChannel("get_temp_set", "get set point temperature", None, int),
        DriverChannel("set_temp_set", "set set point temperature", int, str),
        DriverChannel("get_temp_plate", "get plate temperature", None, int),
        DriverChannel("get_state", "get state", None, int),
        DriverChannel("set_state", "set state", int, str),
        DriverChannel("set_graph", "set graph", str, str),
    ]

    transport = TransportSerial
    protocol = ProtocolAscii

    transport_settings = {
        "timeout": 1,
        "baudrate": 19200,
    }

    protocol_settings = {
    }

    def init_driver(self):
        # Only needed for the prototype which is based on Arduino
        # End product will not have this issue.
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
                return b"ID?"
            case "get_temp_set":
                return b"TEMP_SET?"
            case "set_temp_set":
                return b"TEMP_SET=%d" % params["value"]
            case "get_temp_plate":
                return b"TEMP_PLATE?"
            case "get_state":
                return b"STATE?"
            case "set_state":
                return b"STATE=%d" % params["value"]
            case "set_graph":
                return b"GRAPH=%s" % params["value"].upper()

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
        if response != "Lily hot plate controller":
            raise AssertionError(f"Driver test failed: unexpected instrument ID ({response})")


if __name__ == "__main__":

    import time

    driver_test_settings = {
        "port": "COM16"
    }

    driver = LilyHotPlateController(driver_test_settings)
    driver.test_driver()
    value = driver.process_channel("get_temp_set")
    print("Temp set   :", value)
    print("Set temp   :", driver.process_channel("set_temp_set", {"value": value + 2}))
    print("Temp plate :", driver.process_channel("get_temp_plate"))
    print("State      :", driver.process_channel("get_state"))
    print("Set state  :", driver.process_channel("set_state", {"value": 1}))
    time.sleep(1)
    print("Set state  :", driver.process_channel("set_state", {"value": 0}))
    print("Graph stop :", driver.process_channel("set_graph", {"value": b"stop"}))
    time.sleep(2)
    print("Graph cont :", driver.process_channel("set_graph", {"value": b"cont"}))
    time.sleep(7)
    print("Graph clear:", driver.process_channel("set_graph", {"value": b"clear"}))
