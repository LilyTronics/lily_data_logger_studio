"""
Base class for all protocol classes.
"""

import queue
import threading

from abc import ABC
from abc import abstractmethod
from typing import final


class ProtocolBase(ABC):
    """
    Base class for all protocol classes.

    :param transport:           Instance of a transport class to use for communication.
    :param protocol_settings:   Settings for the protocol.
    :param debug:               Debug value from driver.

    The settings is a dictionary that contains the driver settings controlled by the user
    and the fixed protocol settings defined in the driver (see driver base class).

    A queue processor thread is started to process commands added to the queue by the driver.
    This allows for asynchronous processing of commands and responses.
    This prevents the driver from being blocked while waiting for a response from the instrument.
    """

    def __init__(self, transport, protocol_settings, debug=""):
        self.transport = transport
        self.protocol_settings = protocol_settings
        self.debug = debug
        self.log_debug(f"Transport: {self.transport.get_class_name()}")
        self.log_debug(f"Protocol settings: {self.protocol_settings}")
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        self._thread = threading.Thread(target=self._process_queue, name="ProtocolQueueProcessor",
                                        daemon=True)
        self._thread.start()

    ###########
    # Private #
    ###########

    def _process_queue(self):
        self.log_debug("Queue processor started")
        while not self._stop_event.is_set():
            try:
                data = self._queue.get(True, 0.001)
                response = self._process_command(data["channel"], data["channel_params"],
                                                 data["command"])
                data["callback"](response, data["channel_params"], data["callback_params"])
            except queue.Empty:
                pass
        self.log_debug("Queue processor stopped")

    def _process_command(self, channel, channel_params, command):
        with self._lock:
            self.log_debug(f"Process command: {command}")
            data = self.build_packet(command)
            self.log_debug(f"Command data: {data}")
            expect_response = (channel.expect_response or
                               channel_params.get("response type", "none") != "none")
            response =  self.transport.transceive(data, expect_response,
                                                  self.validate_response)
            if expect_response:
                self.log_debug(f"Response data: {response}")
                response = self.parse_packet(response)
            else:
                self.log_debug(f"No response expected ({response})")
            return response

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if "P" in self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def process_command(self, channel, channel_params, command, callback, callback_params):
        """
        Process a command by either adding it to the queue (if a callback is provided) or
        processing it immediately (if no callback is provided).

        :param channel:         DriverChannel instance to use for communication.
        :param channel_params:  Dictionary with parameters for the channel (optional).
        :param command:         Command to process.
        :param callback:        Callback function to call with the response (if any).
        :param callback_params: Parameters to pass to the callback function.

        The command is provided by the build_command method of the driver.
        The callback parameters are directly passed from the driver.
        """
        if callable(callback):
            self.log_debug("Add data to queue")
            self._queue.put({
                "channel": channel,
                "channel_params": channel_params,
                "command": command,
                "callback": callback,
                "callback_params": callback_params
            })
            return None
        # No callback, process immediately
        return self._process_command(channel, channel_params, command)

    @final
    def close(self):
        """
        Close the protocol by stopping the queue processor thread.
        """
        if self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_packet(self, data) -> bytes:
        """
        Build a packet to send to the instrument.

        :param data: Data to insert into the packet.

        Must be overridden by the protocol class.
        """

    @abstractmethod
    def parse_packet(self, data) -> bytes:
        """
        Parse a packet received from the instrument.

        :param data: Data received from the instrument.

        Must be overridden by the protocol class.
        """

    @abstractmethod
    def validate_response(self, response) -> bool:
        """
        Validate a response received from the instrument.

        :param response: Response received from the instrument.

        Must be overridden by the protocol class.
        """


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
