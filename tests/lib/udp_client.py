"""
UDP client.
"""

import socket


class UdpClient:

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = "\n"

    def __init__(self, ip_address, ip_port, rx_timeout):
        self._server_ip_address = ip_address
        self._server_port = ip_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(rx_timeout)

    ##########
    # Public #
    ##########

    def close(self):
        self._socket.close()

    def send_command(self, command):
        command += self._TERMINATOR
        response = ""
        self._socket.sendto(command.encode("latin"), (self._server_ip_address, self._server_port))
        try:
            response = self._socket.recv(self._RX_BUFFER_SIZE).decode("latin")
            if response.endswith(self._TERMINATOR):
                response = response.strip()
        except ConnectionResetError as e:
            raise ConnectionError(
                f"Could not connect to {self._server_ip_address}:{self._server_port}") from e
        except TimeoutError as e:
            raise TimeoutError("Error receiver timeout") from e

        return response


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.temperature_chamber_test import TemperatureChamberTest

    TemperatureChamberTest().run(True)
