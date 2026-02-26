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
        except ConnectionResetError:
            raise Exception(f"Could not connect to {self._server_ip_address}:{self._server_port}")
        except TimeoutError:
            raise Exception("Error receiver timeout")

        return response


if __name__ == "__main__":

    from src.simulators.test_simulators import test_simulators

    test_simulators()
