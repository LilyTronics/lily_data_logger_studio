"""
Multi channel analog IO simulator using TCP.
"""

import socket

from src.simulators.simulator_base import SimulatorBase
from src.simulators.simulator_settings import SimulatorSettings


class MultiChannelAnalogIo(SimulatorBase):

    NAME = "Multi channel analog IO"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b"\n"

    def __init__(self):
        super().__init__()
        self._sock = None

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
            except (BlockingIOError):
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

                response += self._TERMINATOR
                self._conn.sendall(response)
            except (BlockingIOError):
                pass

    def cleanup(self):
        self._sock.close()


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulator_analog_io_test import SimulatorAnalogIoTest

    SimulatorAnalogIoTest().run()
