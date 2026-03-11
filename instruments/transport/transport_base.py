"""
Base class for all transport classes.
"""

import time

from abc import ABC
from abc import abstractmethod
from typing import final


class TransportBase(ABC):

    _DEFAULT_TIMEOUT = 2

    def __init__(self, transport_settings, debug):
        self.transport_settings = transport_settings
        self.debug = debug

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if "T" in self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def transceive(self, channel, tx_packet, validate_response):
        self.log_debug(f"Process packet: {tx_packet}")
        self.log_debug(f"Connection ready: {self.is_connection_ready()}")
        if not self.is_connection_ready():
            self.connect()
        self.log_debug(f"Connection ready: {self.is_connection_ready()}")
        if not self.is_connection_ready():
            self.log_debug("Connect to instrument")
            raise ConnectionError("No connection could be established")
        self.log_debug(f"Send packet: {tx_packet}")
        self.send(tx_packet)
        response = None
        if channel.expect_response:
            response = b""
            self.log_debug("Expecting response, waiting for response")
            t = time.time()
            t += self.transport_settings.get("timeout", self._DEFAULT_TIMEOUT)
            while (time.time() < t):
                response += self.receive()
                if validate_response(response):
                    break
            else:
                raise TimeoutError("Timout while waiting for response")
            self.log_debug(f"Response: {response}")
        else:
            self.log_debug(f"No response expected ({response})")
        return response

    #############
    # Overrides #
    #############

    @abstractmethod
    def is_connection_ready(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def receive(self):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
