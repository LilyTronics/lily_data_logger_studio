"""
Unit test for the temperature chamber simulator.
"""

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite
from tests.lib.udp_client import UdpClient


class SimulatorTemperatureChamberTest(TestSuite):

    def setup(self):
        start_simulators()

    def teardown(self):
        stop_simulators()

    def test_temperature_chamber(self):
        self.log.debug("Connect to temperature chamber")
        tc = UdpClient(SimulatorSettings.TemperatureChamber["host"],
                       SimulatorSettings.TemperatureChamber["port"],
                       SimulatorSettings.TemperatureChamber["timeout"])
        sim_id = tc.send_command("id?")
        self.log.debug(f"ID: {sim_id}")
        self.fail_if(sim_id != "Temperature chamber", f"Unexpected simulator ID: {sim_id}")
        temp = float(tc.send_command("temp?"))
        self.log.debug(f"Initial temperature: {temp}")
        self.fail_if(temp != 20.0, f"Unexpected initial temperature: {temp}")
        self.log.debug("Set temperature to 30")
        response = tc.send_command('temp=30')
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "Invalid response received. Expected 'ok'.")
        result = self.wait_for(lambda: 29.5 < float(tc.send_command("temp?")) < 30.5, True,
                               timeout=10, interval=1)
        self.log.debug(f"Current temperature: {tc.send_command('temp?')}")
        self.fail_if(result, "Temperature should not have reached 30 degrees")
        self.log.debug("Switch chamber on")
        response = tc.send_command('on')
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "Invalid response received. Expected 'ok'.")
        result = self.wait_for(lambda: 29.5 < float(tc.send_command("temp?")) < 30.5, True,
                               timeout=10, interval=1)
        self.log.debug(f"Current temperature: {tc.send_command('temp?')}")
        self.fail_if(not result, "Temperature did not have reach 30 degrees")
        self.log.debug("Switch chamber off")
        response = tc.send_command('off')
        self.log.debug(f"Response: {response}")
        temp = float(tc.send_command("temp?"))
        self.log.debug(f"Current temperature: {temp}")
        self.fail_if(temp != 20.0, f"Unexpected temperature: {temp}")


if __name__ == "__main__":

    SimulatorTemperatureChamberTest().run()
