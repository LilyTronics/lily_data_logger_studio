"""
Base class for all protocol classes.
"""

from abc import ABC
from abc import abstractmethod
from typing import final


class ProtocolBase(ABC):

    def __init__(self, transport, protocol_settings, user_settings, debug):
        self.transport = transport
        self.protocol_settings = protocol_settings
        self.user_settings = user_settings
        self.debug = debug

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def process_command(self, channel, command):
        self.log_debug(f"Process command: {command}")
        data = self.build_packet(command)
        self.log_debug(f"Command data: {data}")

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_packet(self):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
