"""
Transport over IP/TCP.
"""

import socket

from instruments.transport.transport_base import TransportBase


class TransportTcp(TransportBase):

    socket = None

    _BUFFER_SIZE = 1500
    _DEFAULT_PORT = 50000

    def is_connection_ready(self):
        try:
            address = self.socket.getpeername()
            self.log_debug(f"Connected to: {address[0]}:{address[1]}")
            return True
        except:
            return False

    def connect(self):
        host = self.transport_settings.get("host", "")
        port = self.transport_settings.get("port", self._DEFAULT_PORT)
        self.log_debug(f"Connect to: {host}:{port}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # Small receiver timeout
        self.socket.settimeout(0.001)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self):
        data = b""
        try:
            data = self.socket.recv(self._BUFFER_SIZE)
        except socket.error:
            pass
        return data

    def close(self):
        self.socket.close()


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_analog_io_test import DriverAnalogIoTest

    DriverAnalogIoTest().run()
