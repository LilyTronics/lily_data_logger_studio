"""
Driver template.
"""

# Basic import, always needed
from instruments.drivers.driver_base import DriverBase
from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting

# Import the appropriate transport and protocol classes for your instrument.
# Best is to reuse existing ones, but you can also create your own
from instruments._templates.transport_template import TransportTemplate
from instruments._templates.protocol_template import ProtocolTemplate


class DriverTemplate(DriverBase):

    # Generate a valid ID using the driver_id.py script
    id = "b265ba50-628a-40fc-99ef-9a0df21c156c"
    name = "Driver template"

    driver_settings = [
        DriverSetting("integer setting", int, 0, DriverSetting.CTRL_TEXT),
        DriverSetting("string setting", str, "", DriverSetting.CTRL_TEXT),
        DriverSetting("float setting", float, 0.0, DriverSetting.CTRL_TEXT),
    ]

    channels = [
        DriverChannel("channel_id", "get instrument ID", [], None, str),
    ]

    transport = TransportTemplate
    protocol = ProtocolTemplate

    transport_settings = {
    }

    protocol_settings = {
    }


    def build_command(self, channel, value):
        command = b""
        # Build your command here depending on the channel properties and value
        return command

    def parse_response(self, channel, response):
        response = None
        # Parse the response depending on the channel properties and return the appropriate type
        return response

    def test_driver(self):
        response = self.process_channel("channel_id")
        # Evaluate reposense and raise an exception if the response is not as expected
        print(response)


if __name__ == "__main__":

    # Add some test code here to test your driver

    # Override the default settings with some test settings if needed
    driver_test_settings = {
    }

    # Initialize the driver with debug enabled to see the debug output
    # "DPT": 'D': driver debug, 'P': protocol debug, 'T': transport debug
    driver = DriverTemplate(driver_test_settings, "DPT")
    driver.test_driver()
