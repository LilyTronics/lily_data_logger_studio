"""
Multi channel analog IO simulator using TCP.
"""

import socket
import threading
import time

from src.simulators.simulator_base import SimulatorBase
from src.simulators.simulator_settings import SimulatorSettings


class MultiChannelAnalogIo(SimulatorBase):

    NAME = "SimulatorMultiChannelAnalogIo"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b"\n"

    # Analog conversion from output to input
    _CONVERSIONS = [
        {"gain": 2, "speed": 0.1},
        {"gain": 0.5, "speed": 0.05},
    ]

    def __init__(self):
        super().__init__()
        self._outputs = [0, 0]
        self._inputs = [0, 0]
        self._sock = None
        self._lock = threading.RLock()
        self._analog_thread = threading.Thread(target=self._process_analog,
                                               name="SimulatorAnalogIoProcess", daemon=True)
        self._analog_thread.start()

    ###########
    # Private #
    ###########

    def _process_analog(self):
        while not self._stop_event.is_set():
            for i, conversion in enumerate(self._CONVERSIONS):
                with self._lock:
                    target = self._outputs[i] * conversion["gain"]
                    if self._inputs[i] < target:
                        self._inputs[i] += conversion["speed"]
                    elif self._inputs[i] > target:
                        self._inputs[i] -= conversion["speed"]
                    self._inputs[i] = round(self._inputs[i], 3)
            time.sleep(0.1)

    #############
    # Overrides #
    #############

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setblocking(False)
        self._sock.bind((SimulatorSettings.AnalogIo["host"],
                         SimulatorSettings.AnalogIo["port"]))
        self._sock.listen(1)
        self._conn = None

    def run_handler(self):
        if self._conn is None:
            try:
                self._conn, _ = self._sock.accept()
            except BlockingIOError:
                pass

        if self._conn is not None:
            self._conn.setblocking(False)
            try:
                data = self._conn.recv(self._RX_BUFFER_SIZE)
                if data == b"":
                    # Connection lost
                    self._conn.close()
                    self._conn = None
                    return

                # process data
                response = b"unknown command"
                if data.endswith(self._TERMINATOR):
                    data = data.strip()
                    if data == b"id?":
                        response = self.NAME.encode("utf-8")
                    elif data.startswith(b"so,"):
                        parts = data.split(b",")
                        if len(parts) == 3:
                            channel = int(parts[1])
                            value = float(parts[2])
                            with self._lock:
                                self._outputs[channel - 1] = value
                            response = b"ok"
                    elif data.startswith(b"gi,"):
                        parts = data.split(b",")
                        if len(parts) == 2:
                            channel = int(parts[1])
                            with self._lock:
                                response = b"%f" % self._inputs[channel - 1]
                response += self._TERMINATOR
                self._conn.sendall(response)
            except BlockingIOError:
                pass

    def cleanup(self):
        self._sock.close()


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulator_analog_io_test import SimulatorAnalogIoTest

    SimulatorAnalogIoTest().run()
