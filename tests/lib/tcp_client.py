"""
TCP client.
"""

import socket


class TcpClient:

    _RX_BUFFER_SIZE = 1500
    _END_OF_LINE = b"\n"
    _TIMEOUT = 2

    def __init__(self, ip_address, ip_port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._TIMEOUT)
        self._socket.connect((ip_address, ip_port))

    ##########
    # Public #
    ##########

    def close(self):
        self._socket.close()

    def send_command(self, command, expect_response=True):
        command += self._END_OF_LINE
        response = None
        self._socket.sendall(command)
        if expect_response:
            try:
                response = self._socket.recv(self._RX_BUFFER_SIZE)
                if response.endswith(self._END_OF_LINE):
                    response = response.strip()
            except TimeoutError as e:
                raise TimeoutError("Error receiver timeout") from e
        return response


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulator_analog_io_test import SimulatorAnalogIoTest

    SimulatorAnalogIoTest().run()
