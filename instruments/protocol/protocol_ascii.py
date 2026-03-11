"""
ASCII protocol.
"""

from instruments.protocol.protocol_base import ProtocolBase


class ProtocolAscii(ProtocolBase):

    DEFAULT_END_OF_LINE = b"\n"

    def build_packet(self, data_in):
        eol = self.protocol_settings.get("end_of_line", self.DEFAULT_END_OF_LINE)
        return data_in + eol


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
