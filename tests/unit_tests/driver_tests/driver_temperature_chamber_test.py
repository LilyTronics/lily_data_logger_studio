"""
Test the temperature chamber driver for the simulator.
"""

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite


class DriverTemperatureChamberTest(TestSuite):

    driver = None
    async_response = [False]

    def _callback(self, *response):
        self.log.debug(f"Async response: {response}")
        self.async_response[0] = True

    def setup(self):
        self.log.debug("Start simulators")
        start_simulators()
        Drivers.load()
        driver_class = Drivers.get_driver("TemperatureChamber")
        self.fail_if(driver_class is None, "The driver is not found")
        self.driver = driver_class(SimulatorSettings.TemperatureChamber, "DPT")

    def teardown(self):
        self.log.debug("Stop simulators")
        stop_simulators()

    def test_get_id(self):
        self.log.debug("Get ID")
        response = self.driver.process_channel("gid")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "Temperature chamber", "The ID is not correct")

    def test_get_actual_temperature(self):
        self.log.debug("Get actual temperature")
        response = self.driver.process_channel("gat")
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, float), "The response is not a float")

    def test_temperature_setpoint(self):
        self.log.debug("Get temperature setpoint")
        set_point = self.driver.process_channel("gts")
        self.log.debug(f"Response: {set_point}")
        self.fail_if(not isinstance(set_point, float), "The response is not a float")
        set_point += 5
        response = self.driver.process_channel("sts", set_point)
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "The response is not 'ok'")
        response = self.driver.process_channel("gts")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != set_point, "The setpoint was not updated correctly")

    def test_power_state(self):
        self.log.debug("Get power state")
        state = self.driver.process_channel("gps")
        self.log.debug(f"Response: {state}")
        self.fail_if(not isinstance(state, int), "The response is not an int")
        state = 1 - state
        response = self.driver.process_channel("sps", state)
        self.log.debug(f"Response: {response}")
        self.fail_if(response is not None, "The response is not Non")
        response = self.driver.process_channel("gps")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != state, "The power state was not updated correctly")

    def test_get_id_async(self):
        self.async_response[0] = False
        self.log.debug("Get ID")
        response = self.driver.process_channel("gid", callback=self._callback)
        self.fail_if(response is not None, f"No response expected, got: {response}")
        if not self.wait_for(self.async_response, True, 2, 0.1):
            self._fail("No async response received")


if __name__ == "__main__":

    DriverTemperatureChamberTest().run()
