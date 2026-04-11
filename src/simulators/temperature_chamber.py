"""
Temperature chamber simulator using UDP.
"""

import socket

from src.simulators.simulator_base import SimulatorBase
from src.simulators.simulator_settings import SimulatorSettings


class TemperatureChamber(SimulatorBase):

    NAME = "SimulatorTemperatureChamber"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b"\n"
    _SPEED = 0.5    # Degrees per 0.1 seconds (loop interval)
    _TIMEOUT = 0.1
    _OFF_TEMPERATURE = 20.0

    def __init__(self):
        super().__init__()
        self._sock = None
        self._temperature = self._OFF_TEMPERATURE
        self._set_point = self._OFF_TEMPERATURE
        self._on_state = False

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(self._TIMEOUT)
        self._sock.bind((SimulatorSettings.TemperatureChamber["host"],
                         SimulatorSettings.TemperatureChamber["port"]))

    def run_handler(self):
        try:
            response = b"unknown command"
            data, client_address = self._sock.recvfrom(self._RX_BUFFER_SIZE)
            if data.endswith(self._TERMINATOR):
                data = data.strip()
                if data == b"id?":
                    response = self.NAME.encode("utf-8")
                elif data == b"temp?":
                    response = f"{self._temperature}".encode("utf-8")
                elif data == b"tset?":
                    response = f"{self._set_point}".encode("utf-8")
                elif data == b"pwr?":
                    response = b"1" if self._on_state else b"0"
                elif data.startswith(b"temp="):
                    self._set_point = float(data.split(b"=")[1])
                    response = b"ok"
                elif data.startswith(b"pwr="):
                    self._on_state = bool(int(data.split(b"=")[1]))
                    response = None

            if response is not None:
                response += self._TERMINATOR
                self._sock.sendto(response, client_address)
        except TimeoutError:
            pass

        if self._on_state:
            if self._temperature < self._set_point:
                self._temperature += self._SPEED
            if self._temperature > self._set_point:
                self._temperature -= self._SPEED
        else:
            if self._temperature > self._OFF_TEMPERATURE:
                self._temperature -= self._SPEED
            if self._temperature < self._OFF_TEMPERATURE:
                self._temperature += self._SPEED

    def cleanup(self):
        self._sock.close()


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulator_temperature_chamber_test import \
        SimulatorTemperatureChamberTest

    SimulatorTemperatureChamberTest().run()
