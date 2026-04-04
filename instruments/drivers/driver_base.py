"""
Base class for all driver classes.
"""

import inspect
import uuid

from abc import ABC
from abc import abstractmethod
from typing import final

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting
from instruments.protocol.protocol_base import ProtocolBase
from instruments.transport.transport_base import TransportBase


class DriverBase(ABC):

    id = None
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
        # Driver ID
        if cls.id is None:
            raise ValueError(
                f"(Driver) Driver ID is not set in driver {cls.__name__}"
            )
        try:
            uid = uuid.UUID(cls.id)
            if uid.version != 4:
                raise Exception()
        except Exception as e:
            raise ValueError(
                f"(Driver) Driver ID is not a valid UUID V4 in driver {cls.__name__}"
            ) from e
        # Driver name
        if cls.name is DriverBase.name or not cls.name:
            raise ValueError(
                f"(Driver) Driver name is not set in driver {cls.__name__}"
            )
        # Driver settings
        if cls.driver_settings is None:
            raise ValueError(
                f"(Driver) Driver_settings is not set in driver {cls.__name__}"
            )
        if not isinstance(cls.driver_settings, list):
            raise TypeError(
                f"(Driver) Driver_settings must be a list in driver {cls.__name__}"
            )
        if not cls.driver_settings:
            raise ValueError(
                f"(Driver) Driver_settings is empty in driver {cls.__name__}"
            )
        for setting in cls.driver_settings:
            if not isinstance(setting, DriverSetting):
                raise TypeError(
                    f"(Driver) Driver_settings must contain only DriverSetting instances "
                    f"in driver {cls.__name__}"
                )
        # Channels
        if cls.channels is None:
            raise ValueError(
                f"(Driver) Channels is not set in driver {cls.__name__}"
            )
        if not isinstance(cls.channels, list):
            raise TypeError(
                f"(Driver) Channels must be a list in driver {cls.__name__}"
            )
        if not cls.channels:
            raise ValueError(
                f"(Driver) Channels is empty in driver {cls.__name__}"
            )
        for channel in cls.channels:
            if not isinstance(channel, DriverChannel):
                raise TypeError(
                    f"(Driver) Channels must contain only DriverChannel instances "
                    f"in driver {cls.__name__}"
                )
        # Transport
        if cls.transport is None:
            raise ValueError(
                f"Transport is not set in driver {cls.__name__}"
            )
        if TransportBase not in inspect.getmro(cls.transport):
            raise TypeError(
                f"(Driver) Transport must be a subclass of TransportBase in driver {cls.__name__}"
            )
        # Protocol
        if cls.protocol is None:
            raise ValueError(
                f"(Driver) Protocol is not set in driver {cls.__name__}"
            )
        if ProtocolBase not in inspect.getmro(cls.protocol):
            raise TypeError(
                f"(Driver) Protocol must be a subclass of ProtocolBase in driver {cls.__name__}"
            )

    ###########
    # Private #
    ###########

    @classmethod
    def _get_channels(cls, direction):
        channels = []
        if cls.channels is not None:
            channels = [x for x in cls.channels if x.direction == direction]
        return channels

    def _process_response(self, channel, response):
        if channel.expect_response:
            self.log_debug(f"Channel response: {response}")
            response = self.parse_response(channel, response)
            self.log_debug(f"Channel return value: {response}")
        else:
            self.log_debug(f"No channel response expected ({response})")
        return response

    def _process_callback(self, response, params):
        response = self._process_response(params["channel"], response)
        params["callback"](response, params["callback_params"])


    ##########
    # Public #
    ##########

    @staticmethod
    @final
    def get_driver_setting_class():
        return DriverSetting

    @classmethod
    @final
    def get_class_name(cls):
        return cls.__name__

    @final
    def log_debug(self, message):
        if "D" in self.debug:
            print(f"({self.get_class_name()})", message)

    @classmethod
    @final
    def get_input_channels(cls):
        return cls._get_channels(DriverChannel.DIR_INPUT)

    @classmethod
    @final
    def get_output_channels(cls):
        return cls._get_channels(DriverChannel.DIR_OUTPUT)

    @classmethod
    @final
    def get_channel(cls, query):
        # Get channel by ID or by name
        # Prio is ID
        matches = [x for x in cls.channels if x.channel_id == query]
        if len(matches) == 0:
            matches = [x for x in cls.channels if x.name == query]
        return None if len(matches) != 1 else matches[0]

    @final
    def process_channel(self, channel_query, value=None, callback=None, callback_params=None):
        self.log_debug(f"Get channel for query: '{channel_query}'")
        channel = self.get_channel(channel_query)
        if channel is None:
            raise LookupError(
                f"(Driver) Channel '{channel_query}' not found in driver {self.get_class_name()}"
            )
        self.log_debug(f"Process channel: {channel.channel_id} - {channel.name}")
        command = self.build_command(channel, value)
        if not isinstance(command, bytes):
            raise TypeError("(Driver) Command must be of type bytes")
        self.log_debug(f"Channel command: {command}")
        if callback is not None:
            callback_params = {
                "callback": callback,
                "callback_params": callback_params,
                "channel": channel
            }
            callback = self._process_callback
        response = self.protocol.process_command(channel, command, callback, callback_params)
        if callable(callback):
            # The callback is present
            return None
        return self._process_response(channel, response)

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_command(self, channel, value):
        pass

    @abstractmethod
    def parse_response(self, channel, response):
        pass

    @abstractmethod
    def test_driver(self):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
