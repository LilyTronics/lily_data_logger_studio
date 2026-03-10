"""
Transport over IP/UDP.
"""

from instruments.transport.transport_base import TransportBase


class TransportUdp(TransportBase):
    pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
