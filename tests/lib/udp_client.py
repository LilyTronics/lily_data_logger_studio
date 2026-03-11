"""
UDP client.
"""

import socket


class UdpClient:

    _RX_BUFFER_SIZE = 1500
    _END_OF_LINE = "\n"
    _TIMEOUT = 0.5

    def __init__(self, ip_address, ip_port):
        self._server_ip_address = ip_address
        self._server_port = ip_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._TIMEOUT)

    ##########
    # Public #
    ##########

    def close(self):
        self._socket.close()

    def send_command(self, command):
        command += self._END_OF_LINE
        response = ""
        self._socket.sendto(command.encode("latin"), (self._server_ip_address, self._server_port))
        try:
            response = self._socket.recv(self._RX_BUFFER_SIZE).decode("latin")
            if response.endswith(self._END_OF_LINE):
                response = response.strip()
        except ConnectionResetError as e:
            raise ConnectionError(
                f"Could not connect to {self._server_ip_address}:{self._server_port}") from e
        except TimeoutError as e:
            raise TimeoutError("Error receiver timeout") from e

        return response


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulator_temperature_chamber_test import \
        SimulatorTemperatureChamberTest

    SimulatorTemperatureChamberTest().run()
