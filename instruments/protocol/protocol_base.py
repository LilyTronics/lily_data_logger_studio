"""
Base class for all protocol classes.
"""

from abc import ABC
from abc import abstractmethod

class ProtocolBase(ABC):

    def __init__(self, transport, protocol_settings, user_settings):
        self.transport = transport
        self.protocol_settings = protocol_settings
        self.user_settings = user_settings

    ##########
    # Public #
    ##########

    def process_command(self, channel, command):
        data = self.build_data()

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_data(self):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
