"""
Transport over TCP.
"""

import socket

from instruments.transport.transport_base import TransportBase


class TransportTcp(TransportBase):
    """
    Transport layer for TCP connections.
    """

    socket = None

    _BUFFER_SIZE = 1500

    def get_id(self):
        """
        The ID is defined by the IP address and port number.
        In case host names are used, they are converted to the IP address.
        """
        ip = socket.gethostbyname(self.transport_settings.get("host", None))
        return f"tcp_{ip}_{self.transport_settings.get("port", None)}"

    def is_connection_ready(self):
        """
        Check if a connection is active.
        """
        try:
            address = self.socket.getpeername()
            self.log_debug(f"Connected to: {address[0]}:{address[1]}")
            return True
        except:
            return False

    def connect(self):
        """
        Connect to the host.
        """
        host = self.transport_settings.get("host", "")
        port = self.transport_settings.get("port", None)
        self.log_debug(f"Connect to: {host}:{port}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # Small receiver timeout
        self.socket.settimeout(0.001)

    def send(self, data):
        """
        Send data.
        """
        self.socket.sendall(data)

    def receive(self):
        """
        Check for data and return the data.
        """
        data = b""
        try:
            data = self.socket.recv(self._BUFFER_SIZE)
        except socket.error:
            pass
        return data

    def close(self):
        """
        Close the socket.
        """
        if self.socket is not None:
            self.socket.close()


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_analog_io_test import DriverAnalogIoTest

    DriverAnalogIoTest().run()
