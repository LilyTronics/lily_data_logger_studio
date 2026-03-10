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

    def setup(self):
        self.log.debug("Start simulators")
        start_simulators()
        Drivers.load()
        driver_class = Drivers.get_driver("TemperatureChamber")
        self.fail_if(driver_class is None, "The driver is not found")
        self.driver = driver_class(SimulatorSettings.TemperatureChamber)

    def teardown(self):
        self.log.debug("Stop simulators")
        stop_simulators()

    def test_id(self):
        self.log.debug("Get ID synchronously")
        response = self.driver.process_channel("gid")
        self.log.debug(f"Response: {response}")


if __name__ == "__main__":

    DriverTemperatureChamberTest().run()
