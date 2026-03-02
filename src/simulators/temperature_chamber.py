"""
Temperature chamber simulator using UDP.
"""

import socket

from src.simulators.simulator_base import SimulatorBase
from src.simulators.simulator_settings import SimulatorSettings


class TemperatureChamber(SimulatorBase):

    NAME = "Temperature chamber"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = "\n"
    _SPEED = 0.5    # Degrees per 0.1 seconds (loop interval)

    def __init__(self):
        super().__init__()
        self._sock = None
        self._temperature = 20.0
        self._set_point = 20.0

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(SimulatorSettings.TemperatureChamber.RX_TIME_OUT)
        self._sock.bind((SimulatorSettings.TemperatureChamber.IP,
                         SimulatorSettings.TemperatureChamber.PORT))

    def run_handler(self):
        try:
            response = "unknown command"
            data, client_address = self._sock.recvfrom(self._RX_BUFFER_SIZE)
            data = data.decode("latin")
            if data.endswith(self._TERMINATOR):
                data = data.strip()
                if data == "id?":
                    response = self.NAME
                if data == "temp?":
                    response = f"{self._temperature}"
                if data.startswith("temp="):
                    self._set_point = float(data.split("=")[1])
                    response = "ok"
            response += self._TERMINATOR
            self._sock.sendto(response.encode("latin"), client_address)
        except TimeoutError:
            pass

        if self._temperature < self._set_point:
            self._temperature += self._SPEED
        if self._temperature > self._set_point:
            self._temperature -= self._SPEED

    def cleanup(self):
        self._sock.close()


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.temperature_chamber_test import TemperatureChamberTest

    TemperatureChamberTest().run(True)
