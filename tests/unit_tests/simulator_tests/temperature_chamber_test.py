"""
Unit test for the temperature chamber simulator.
"""

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite
from tests.lib.udp_client import UdpClient


class TemperatureChamberTest(TestSuite):

    def setup(self):
        start_simulators()

    def teardown(self):
        stop_simulators()

    def test_temperature_chamber(self):
        self.log.debug("Connect to temperature chamber")
        tc = UdpClient(SimulatorSettings.TemperatureChamber.IP,
                    SimulatorSettings.TemperatureChamber.PORT,
                    SimulatorSettings.TemperatureChamber.RX_TIME_OUT)
        sim_id = tc.send_command("id?")
        self.log.debug(f"ID: {sim_id}")
        self.fail_if(sim_id != "Temperature chamber", f"Unexpected simulator ID: {sim_id}")
        temp = float(tc.send_command("temp?"))
        self.log.debug(f"Initial temperature: {temp}")
        self.fail_if(temp != 20.0, f"Unexpected initial temperature: {temp}")
        self.log.debug("Set temperature to 30")
        self.log.debug(f"Set temperature response: {tc.send_command('temp=30')}")
        result = self.wait_for(lambda: 29.5 < float(tc.send_command("temp?")) < 30.5, True,
                               timeout=60, interval=1)
        self.log.debug(f"Current temperature: {tc.send_command('temp?')}")
        self.fail_if(not result, "Temperature did not reach 30 within 60 seconds")


if __name__ == "__main__":

    TemperatureChamberTest().run(True)
