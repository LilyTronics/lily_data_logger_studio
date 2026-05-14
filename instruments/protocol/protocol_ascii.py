"""
ASCII protocol.
"""

from instruments.protocol.protocol_base import ProtocolBase


class ProtocolAscii(ProtocolBase):

    DEFAULT_END_OF_LINE = b"\n"

    def build_packet(self, data):
        """
        Take the data adds the end of line character to it.
        """
        eol = self.protocol_settings.get("end_of_line", self.DEFAULT_END_OF_LINE)
        return data + eol

    def parse_packet(self, data):
        """
        Take the received data and remove the end or line character.
        """
        eol = self.protocol_settings.get("end_of_line", self.DEFAULT_END_OF_LINE)
        return data.strip(eol)

    def validate_response(self, response):
        """
        A received packet is valid if it ends with the end of line character.
        """
        eol = self.protocol_settings.get("end_of_line", self.DEFAULT_END_OF_LINE)
        return response.endswith(eol)


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
