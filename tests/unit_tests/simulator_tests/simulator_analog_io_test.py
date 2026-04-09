"""
Unit test for the multi channel analog IO simulator.
"""

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite
from tests.lib.tcp_client import TcpClient


class SimulatorAnalogIoTest(TestSuite):

    def setup(self):
        start_simulators()

    def teardown(self):
        stop_simulators()

    def test_get_id(self):
        self.log.debug("Connect to analog IO")
        io = TcpClient(SimulatorSettings.AnalogIo["host"],
                       SimulatorSettings.AnalogIo["port"])
        sim_id = io.send_command(b"id?")
        self.log.debug(f"ID: {sim_id}")
        self.fail_if(sim_id != b"Multi channel analog IO", f"Unexpected simulator ID: {sim_id}")


if __name__ == "__main__":

    SimulatorAnalogIoTest().run()
