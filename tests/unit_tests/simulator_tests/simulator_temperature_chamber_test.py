"""
Unit test for the temperature chamber simulator.
"""

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite
from tests.lib.udp_client import UdpClient


class SimulatorTemperatureChamberTest(TestSuite):

    _TIMEOUT = 15

    def setup(self):
        start_simulators()

    def teardown(self):
        stop_simulators()

    def _wait_for_temperature(self, tc, target_temp):
        t = self._TIMEOUT
        while t > 0:
            temp = tc.send_command("temp?")
            self.log.debug(f"Current temperature: {temp}")
            if target_temp - 0.5 < float(temp) < target_temp + 0.5:
                return True
            self.sleep(3)
            t -= 3
        return False

    def test_temperature_chamber(self):
        self.log.debug("Connect to temperature chamber")
        tc = UdpClient(SimulatorSettings.TemperatureChamber["host"],
                       SimulatorSettings.TemperatureChamber["port"])
        sim_id = tc.send_command("id?")
        self.log.debug(f"ID: {sim_id}")
        self.fail_if(sim_id != "Temperature chamber", f"Unexpected simulator ID: {sim_id}")
        temp = float(tc.send_command("temp?"))
        self.log.debug(f"Initial temperature: {temp}")
        self.fail_if(temp != 20.0, f"Unexpected initial temperature: {temp}")
        self.log.debug("Set temperature to 30")
        response = tc.send_command("temp=30")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "Invalid response received. Expected 'ok'.")
        result = self._wait_for_temperature(tc, 30.0)
        self.fail_if(result, "Temperature should not have reached 30 degrees")
        self.log.debug("Switch chamber on")
        tc.send_command("pwr=1", False)
        self.fail_if(response != "ok", "Invalid response received. Expected 'ok'.")
        result = self._wait_for_temperature(tc, 30.0)
        self.fail_if(not result, "Temperature did not reach 30 degrees")
        self.log.debug("Switch chamber off")
        tc.send_command("pwr=0", False)
        result = self._wait_for_temperature(tc, 20.0)
        self.log.debug(f"Current temperature: {temp}")
        self.fail_if(not result, f"Temperature did not return to 20 degrees")


if __name__ == "__main__":

    SimulatorTemperatureChamberTest().run()
