"""
ASCII protocol.
"""

from instruments.protocol.protocol_base import ProtocolBase


class ProtocolAscii(ProtocolBase):
    pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
