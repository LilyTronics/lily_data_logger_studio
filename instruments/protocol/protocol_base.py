"""
Base class for all protocol classes.
"""

import queue
import threading

from abc import ABC
from abc import abstractmethod
from typing import final


class ProtocolBase(ABC):

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
                response = self._process_command(data["channel"], data["command"])
                data["callback"](response, data["callback_params"])
            except queue.Empty:
                pass
        self.log_debug("Queue processor stopped")

    def _process_command(self, channel, command):
        with self._lock:
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

    ##########
    # Public #
    ##########

    @final
    def log_debug(self, message):
        if "P" in self.debug:
            print(f"({self.__class__.__name__})", message)

    @final
    def process_command(self, channel, command, callback, callback_params):
        if callable(callback):
            self.log_debug("Add data to queue")
            self._queue.put({
                "channel": channel,
                "command": command,
                "callback": callback,
                "callback_params": callback_params
            })
            return None
        # No callback, process immediately
        return self._process_command(channel, command)

    #############
    # Overrides #
    #############

    @abstractmethod
    def build_packet(self, data):
        pass

    @abstractmethod
    def parse_packet(self, data):
        pass

    @abstractmethod
    def validate_response(self, response):
        pass


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
