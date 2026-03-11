"""
Base class for all transport classes.
"""

from abc import ABC
from typing import final


class TransportBase(ABC):

    def __init__(self, transport_settings, user_settings, debug):
        self.transport_settings = transport_settings
        self.user_settings = user_settings
        self.debug = debug

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if self.debug:
            print(f"({self.__class__.__name__})", message)


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
