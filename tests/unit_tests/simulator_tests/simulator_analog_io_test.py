"""
Unit test for the multi channel analog IO simulator.
"""

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite
from tests.lib.tcp_client import TcpClient


class SimulatorAnalogIoTest(TestSuite):

    client = None
    channel = 0
    expected_values = [4, 1]

    def setup(self):
        start_simulators()

    def teardown(self):
        stop_simulators()

    def check_input(self):
        self.fail_if(not (1 <= self.channel <= 2), f"Invalid channel {self.channel}")
        response = float(self.client.send_command(b"gi,%d" % self.channel))
        return response == self.expected_values[self.channel - 1]

    def test_get_id(self):
        self.log.debug("Connect to analog IO")
        self.client = TcpClient(SimulatorSettings.AnalogIo["host"],
                                SimulatorSettings.AnalogIo["port"])
        sim_id = self.client.send_command(b"id?")
        self.log.debug(f"ID: {sim_id}")
        self.fail_if(sim_id != b"SimulatorMultiChannelAnalogIo", f"Unexpected simulator ID: {sim_id}")

    def test_set_output(self):
        for self.channel in range(1, 3):
            self.log.debug(f"Set IO channel {self.channel}")
            response = self.client.send_command(b"so,%d,2" % self.channel)
            self.fail_if(response != b"ok", f"Invalid response: {response}")
            self.log.debug("Wait for input to follow")
            result = self.wait_for(self.check_input, True, 10, 0.5)
            response = float(self.client.send_command(b"gi,%d" % self.channel))
            self.log.debug(f"Input value: {response}")
            self.fail_if(not result, "Input did not follow the output")


if __name__ == "__main__":

    SimulatorAnalogIoTest().run()
