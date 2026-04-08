"""
Transport over IP/UDP.
"""

import socket

from instruments.transport.transport_base import TransportBase


class TransportUdp(TransportBase):

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    _BUFFER_SIZE = 1500
    _DEFAULT_PORT = 50000

    def is_connection_ready(self):
        try:
            address = self.socket.getpeername()
            self.log_debug(f"Connect to: {address[0]}:{address[1]}")
            return True
        except:
            return False

    def connect(self):
        self.socket.connect((
            self.transport_settings.get("host", ""),
            self.transport_settings.get("port", self._DEFAULT_PORT)
        ))
        # Small receiver timeout
        self.socket.settimeout(0.001)

    def send(self, data):
        self.socket.send(data)

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

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
