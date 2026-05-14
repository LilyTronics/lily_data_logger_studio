"""
Base class for all transport classes.
"""

import time

from abc import ABC
from abc import abstractmethod
from typing import final


class TransportBase(ABC):
    """
    Base class for all transport classes.

    :param transport_settings:  Settings for the transport.
    :param debug:               Debug value from driver.

    The settings is a dictionary that contains the driver settings controlled by the user
    and the fixed transport settings defined in the driver (see driver base class).
    """

    _DEFAULT_TIMEOUT = 2

    def __init__(self, transport_settings, debug=""):
        self.transport_settings = transport_settings
        self.debug = debug
        self.log_debug(f"Transport settings: {self.transport_settings}")

    ##########
    # Public #
    ##########

    @classmethod
    @final
    def get_class_name(cls):
        return cls.__name__

    @final
    def log_debug(self, message):
        if "T" in self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def transceive(self, tx_packet, expect_response, validate_response):
        """
        Send data and return the response (if any).

        :param tx_packet            data to send.
        :param expect_response      whether to expect a response.
        :param validate_response    callback function for valifating the response.
        """
        self.log_debug(f"Process packet: {tx_packet}")
        is_ready = self.is_connection_ready()
        self.log_debug(f"Connection ready: {is_ready}")
        if not is_ready:
            self.connect()
        is_ready = self.is_connection_ready()
        self.log_debug(f"Connection ready: {is_ready}")
        if not is_ready:
            self.log_debug("Connect to instrument")
            raise ConnectionError("(Transport) No connection could be established")
        self.log_debug(f"Send packet: {tx_packet}")
        self.send(tx_packet)
        response = None
        if expect_response:
            response = b""
            self.log_debug("Expecting response, waiting for response")
            t = time.time() + self.transport_settings.get("timeout", self._DEFAULT_TIMEOUT)
            while time.time() < t:
                response += self.receive()
                if validate_response(response):
                    break
            else:
                raise TimeoutError("(Transport) Timeout while waiting for response")
            self.log_debug(f"Response: {response}")
        else:
            self.log_debug(f"No response expected ({response})")
        return response

    #############
    # Overrides #
    #############

    @abstractmethod
    def get_id(self):
        """
        Returns the ID for the transport to use in the transport pool.
        Must be overridden by the transport class.
        """

    @abstractmethod
    def is_connection_ready(self):
        """
        Retuns true if the transport is connected.
        Must be overridden by the transport class.
        """

    @abstractmethod
    def connect(self):
        """
        Open the connection.
        Must be overridden by the transport class.
        """

    @abstractmethod
    def send(self, data):
        """
        Send the data.
        Must be overridden by the transport class.
        """

    @abstractmethod
    def receive(self):
        """
        Return the received data.
        Must be overridden by the transport class.
        """

    @abstractmethod
    def close(self):
        """
        Close the connection.
        Must be overridden by the transport class.
        """

if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
