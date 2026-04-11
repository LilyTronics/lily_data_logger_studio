"""
Test the temperature chamber driver for the simulator.
"""

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite


class DriverAnalogIoTest(TestSuite):

    driver = None
    async_response = [False]

    def _callback(self, *response):
        self.log.debug(f"Async response: {response}")
        self.async_response[0] = True
        self.fail_if(not isinstance(response[0], response[1]),
                     "The type is incorrect")

    def setup(self):
        self.log.debug("Start simulators")
        start_simulators()
        Drivers.load()
        driver_class = Drivers.get_driver("MultiChannelAnalogIo")
        self.fail_if(driver_class is None, "The driver is not found")
        self.driver = driver_class(SimulatorSettings.AnalogIo, "DPT")

    def teardown(self):
        # self.driver.close()
        self.log.debug("Stop simulators")
        stop_simulators()

    def test_driver_test(self):
        self.driver.test_driver()

    def test_get_id(self):
        self.log.debug("Get ID")
        response = self.driver.process_channel("gid")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "SimulatorMultiChannelAnalogIo", "The ID is not correct")

    def test_get_id_async(self):
        self.async_response[0] = False
        self.log.debug("Get ID")
        response = self.driver.process_channel("gid", callback=self._callback,
                                               callback_params=str)
        self.fail_if(response is not None, f"No response expected, got: {response}")
        if not self.wait_for(self.async_response, True, 2, 0.1):
            self._fail("No async response received")

    def test_set_output(self):
        params = {
            "channel": 1,
            "value": 7
        }
        response = self.driver.process_channel("so", params)
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "Invalid response")

    def test_get_input(self):
        params = {
            "channel": 1
        }
        response = self.driver.process_channel("gi", params)
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, float), "Invalid response")


if __name__ == "__main__":

    DriverAnalogIoTest().run()
