"""
Base class for all protocol classes.
"""

from abc import ABC
from abc import abstractmethod
from typing import final


class ProtocolBase(ABC):

    def __init__(self, transport, protocol_settings, debug):
        self.transport = transport
        self.protocol_settings = protocol_settings
        self.debug = debug

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if "P" in self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def process_command(self, channel, command):
        self.log_debug(f"Process command: {command}")
        data = self.build_packet(command)
        self.log_debug(f"Command data: {data}")
        response =  self.transport.transceive(channel, data, self.validate_response)
        if channel.expect_response:
            self.log_debug(f"Response data: {response}")
            response = self.parse_packet(response)
        else:
            self.log_debug(f"No response expected ({response})")
        return response

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_packet(self):
        pass

    @abstractmethod
    def parse_packet(self):
        pass

    @abstractmethod
    def validate_response(self):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
