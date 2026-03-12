"""
Base class for all driver classes.
"""

import inspect

from abc import ABC
from abc import abstractmethod
from typing import final

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting
from instruments.protocol.protocol_base import ProtocolBase
from instruments.transport.transport_base import TransportBase


class DriverBase(ABC):

    name = "base class"
    driver_settings = None
    channels = None
    transport = None
    transport_settings = {}
    protocol = None
    protocol_settings = {}
    is_simulator = False

    def __init__(self, settings, debug=""):
        self.user_settings = settings
        # Debug: D/P/T: Driver, Protocol, Transport (e.g.: "DT": driver and transport)
        self.debug = debug
        self.transport = self.transport(self.transport_settings | self.user_settings, self.debug)
        self.protocol = self.protocol(self.transport, self.protocol_settings | self.user_settings,
                                      self.debug)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Driver name
        if cls.name is DriverBase.name or not cls.name:
            raise ValueError(
                f"Driver name is not set in driver {cls.__name__}"
            )
        # Driver settings
        if cls.driver_settings is None:
            raise ValueError(
                f"Driver_settings is not set in driver {cls.__name__}"
            )
        if not isinstance(cls.driver_settings, list):
            raise TypeError(
                f"Driver_settings must be a list in driver {cls.__name__}"
            )
        if not cls.driver_settings:
            raise ValueError(
                f"Driver_settings is empty in driver {cls.__name__}"
            )
        for setting in cls.driver_settings:
            if not isinstance(setting, DriverSetting):
                raise TypeError(
                    f"Driver_settings must contain only DriverSetting instances "
                    f"in driver {cls.__name__}"
                )
        # Channels
        if cls.channels is None:
            raise ValueError(
                f"Channels is not set in driver {cls.__name__}"
            )
        if not isinstance(cls.channels, list):
            raise TypeError(
                f"Channels must be a list in driver {cls.__name__}"
            )
        if not cls.channels:
            raise ValueError(
                f"Channels is empty in driver {cls.__name__}"
            )
        for channel in cls.channels:
            if not isinstance(channel, DriverChannel):
                raise TypeError(
                    f"Channels must contain only DriverChannel instances "
                    f"in driver {cls.__name__}"
                )
        # Transport
        if cls.transport is None:
            raise ValueError(
                f"Transport is not set in driver {cls.__name__}"
            )
        if TransportBase not in inspect.getmro(cls.transport):
            raise TypeError(
                f"Transport must be a subclass of TransportBase in driver {cls.__name__}"
            )
        # Protocol
        if cls.protocol is None:
            raise ValueError(
                f"Protocol is not set in driver {cls.__name__}"
            )
        if ProtocolBase not in inspect.getmro(cls.protocol):
            raise TypeError(
                f"Protocol must be a subclass of ProtocolBase in driver {cls.__name__}"
            )

    ##########
    # Public #
    ##########

    @classmethod
    @final
    def get_class_name(cls):
        return cls.__name__

    @final
    def log_debug(self, message):
        if "D" in self.debug:
            print(f"({self.get_class_name()})", message)

    @final
    def process_channel(self, channel_query, value=None):
        self.log_debug(f"Get channel for query: '{channel_query}'")
        query = channel_query.strip().lower()
        matches = [
            channel for channel in self.channels
            if query == channel.channel_id.lower()
            or query == channel.name.lower()
        ]
        if len(matches) == 0:
            raise LookupError(
                f"Channel '{channel_query}' not found in driver {self.get_class_name()}"
            )
        if len(matches) > 1:
            raise LookupError(
                f"Channel '{channel_query}' is ambiguous in driver {self.get_class_name()}"
            )
        channel = matches[0]
        self.log_debug(f"Process channel: {channel.channel_id} - {channel.name}")
        command = self.build_command(channel, value)
        if not isinstance(command, bytes):
            raise TypeError("Command must be of type bytes")
        self.log_debug(f"Channel command: {command}")
        response = self.protocol.process_command(channel, command)
        if channel.expect_response:
            self.log_debug(f"Channel response: {response}")
            response = self.parse_response(channel, response)
            self.log_debug(f"Channel return value: {response}")
        else:
            self.log_debug(f"No channel response expected ({response})")
        return response

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_command(self, channel, value=None):
        pass

    @abstractmethod
    def parse_response(self, channel, response):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
