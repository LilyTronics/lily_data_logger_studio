"""
Base class for all driver classes.
"""

import inspect
import uuid

from abc import ABC
from abc import abstractmethod
from typing import final

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_setting import DriverSetting
from instruments.protocol.protocol_base import ProtocolBase
from instruments.transport.transport_base import TransportBase


class DriverBase(ABC):
    """
    Base class for all drivers.

    :param settings:    Instrument specific settings like port, baudrate, etc.
    :param debug:       Debug options ('D': Driver, 'P': Protocol, 'T': Transport)
                        (e.g.: "DT": show debug output for driver and transport)
    """

    #: Driver ID. Must be a valid UUID V4 string.
    id = None
    #: Driver manufacturer name.
    manufacturer = "not set"
    #: Driver model name.
    model = "not set"
    #: Driver description. Short description of the instrument.
    description = "Base class for all drivers"
    #: Driver settings. Dictionary of setting that are required to configure the driver.
    driver_settings = None
    #: Channels. List of channel objects that represents the instrument's functionality.
    #: These are exposed in the application.
    channels = None
    #: Internal channels (optional). List of channel objects that are used internally by the driver.
    #: These are not exposed in the application
    internal_channels = []
    #: Transport class (not an instance). Must be a subclass of TransportBase.
    transport = None
    #: Transport settings. Dictionary of settings that are required to configure the transport.
    transport_settings = {}
    #: Protocol class (not an instance). Must be a subclass of ProtocolBase.
    protocol = None
    #: Protocol settings. Dictionary of settings that are required to configure the protocol.
    protocol_settings = {}
    is_simulator = False

    def __init__(self, settings, debug=""):
        self.user_settings = settings
        # Debug: D/P/T: Driver, Protocol, Transport (e.g.: "DT": driver and transport)
        self.debug = debug
        self.transport = self.transport(self.transport_settings | self.user_settings, self.debug)
        self.protocol = self.protocol(self.transport, self.protocol_settings | self.user_settings,
                                      self.debug)
        self.init_driver()

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
        if cls.manufacturer is DriverBase.manufacturer or not cls.manufacturer:
            raise ValueError(
                f"(Driver) Driver manufacturer is not set in driver {cls.__name__}"
            )
        # Driver model
        if cls.model is DriverBase.model or not cls.model:
            raise ValueError(
                f"(Driver) Driver manufacturer is not set in driver {cls.__name__}"
            )
        # Driver description
        if cls.description is DriverBase.description or not cls.description:
            raise ValueError(
                f"(Driver) Driver description is not set in driver {cls.__name__}"
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

        cls.name = f"{cls.manufacturer} {cls.model}"

    ###########
    # Private #
    ###########

    @classmethod
    def _get_channels(cls, direction):
        channels = []
        if cls.channels is not None:
            channels = [x for x in cls.channels if x.direction == direction]
        return channels

    def _get_internal_channel(self, query):
        # Internal channel always by ID
        matches = [x for x in self.internal_channels if x.channel_id == query]
        return None if len(matches) != 1 else matches[0]

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
    def get_driver_setting_class() -> type[DriverSetting]:
        """
        Returns the class used for driver settings.
        Used for programmatically creating driver settings.
        """
        return DriverSetting

    @classmethod
    @final
    def get_class_name(cls) -> str:
        """
        Returns the class name of the driver class.
        """
        return cls.__name__

    @final
    def log_debug(self, message):
        if "D" in self.debug:
            print(f"({self.get_class_name()})", message)

    @classmethod
    @final
    def get_input_channels(cls) -> list[DriverChannel]:
        """
        Returns a list of input channels.
        """
        return cls._get_channels(DriverChannel.DIR_INPUT)

    @classmethod
    @final
    def get_output_channels(cls) -> list[DriverChannel]:
        """
        Returns a list of output channels.
        """
        return cls._get_channels(DriverChannel.DIR_OUTPUT)

    @classmethod
    @final
    def get_channel(cls, query) -> DriverChannel | None:
        """"
        Returns the channel by ID or by name (query).
        Prio is ID.
        """
        matches = [x for x in cls.channels if x.channel_id == query]
        if len(matches) == 0:
            matches = [x for x in cls.channels if x.name == query]
        return None if len(matches) != 1 else matches[0]

    @final
    def process_channel(self, channel_query, params=None,
                        callback=None, callback_params=None) -> any:
        """
        Process a channel by ID or by name (prio is ID).

        :param channel_query:       Channel ID or name.
        :param params:              Dictionary with parameters for the channel (optional).
        :param callback:            Callback function for asynchronous processing (optional).
        :param callback_params:     Parameters for the callback function (optional).

        :return:                    Response from the instrument or None if a callback is used.

        The channel parameters must match with the channel parameters as defined in the list of
        channels. For output channels there is at least one parameter: 'value'. This is the value
        that is sent to the instrument. For input channels there are no mandatory parameters,
        but the driver settings can define parameters.

        If a channel is processed without a callback, the channel is processed immediately and
        the response is returned. If the instrument responds slow, this can block the application.

        If a channel is processed with a callback, the channel is processed in the background by
        the protocol class and the response is passed to the callback function when it is received.

        The callback function must have the following signature:
        :code:`function_name(response, params)`
        """
        params = {} if params is None else params
        self.log_debug(f"Get channel for query: '{channel_query}'")
        channel = self.get_channel(channel_query)
        if channel is None:
            # Check internal channels
            channel = self._get_internal_channel(channel_query)
        if channel is None:
            raise LookupError(
                f"(Driver) Channel '{channel_query}' not found in driver {self.get_class_name()}"
            )
        self.log_debug(f"Process channel: {channel.channel_id} - {channel.name}")
        command = self.build_command(channel, params)
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

    @final
    def close(self) -> None:
        """
        Closes the driver and the underlying protocol and transport connections.
        """
        self.protocol.close()
        self.transport.close()

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_command(self, channel, params) -> bytes:
        """
        Builds the command to send to the instrument based on the channel and parameters.
        Must be overridden by the driver class.

        :param channel: Driver channel object.
        :param params:  Dictionary with parameters for the channel.

        :return: Data to send to the instrument.
        """

    @abstractmethod
    def parse_response(self, channel, response) -> any:
        """
        Parses the response from the instrument based on the channel.
        Must be overridden by the driver class.

        :param channel:     Driver channel object.
        :param response:    Response from the instrument.

        :return: Parsed response. The type depends on the driver channel settings.
        """

    @abstractmethod
    def test_driver(self):
        """
        This method is used to test if the instrument is connected and responding correctly.
        This should be a short test. For example, retrieving the instrument ID or a
        simple status command.
        Must be overridden by the driver class.
        """

    def init_driver(self):
        """
        This function is called after the driver is instantiated. It can be used to initialize
        the instrument by sending some commands to the instrument.
        Note that using this, the application needs to wait until the initialization is completed.
        If this takes too long, it can block the application.
        This is optional and can be overridden by the driver class if needed.
        """


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
