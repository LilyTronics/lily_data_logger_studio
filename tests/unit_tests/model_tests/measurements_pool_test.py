"""
Unit tests for the measurements pool.
"""

import os

import src.app_data as AppData

from src.models.drivers import Drivers
from src.models.instrument_pool import InstrumentPool
from src.models.measurements_pool import MeasurementsPool
from src.models.configuration import Configuration
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from tests.lib.test_suite import TestSuite


class MeasurementsPoolTest(TestSuite):

    config = None

    def setup(self):
        self.config = Configuration()
        self.config.load(os.path.join(AppData.TEST_CONFIG_PATH, "test_measurements_end_time.json"))
        Drivers.load()
        instruments = self.config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        InstrumentPool.add_instruments(instruments)
        start_simulators()

    def teardown(self):
        stop_simulators()

    def test_add_measurements_from_config(self):
        MeasurementsPool.clear()
        measurements = self.config.get_measurements()
        self.fail_if(len(measurements) == 0, "No measurements in the configuration")
        MeasurementsPool.add_measurements(measurements)
        self.fail_if(len(MeasurementsPool.get_measurements()) == 0,
                     "No measurements added to the pool")

    def test_process_measurement(self):
        measurements = self.config.get_measurements()
        for measurement in measurements:
            self.log.debug(f"Process measurement: {measurement["name"]} ({measurement["id"]})")
            result = MeasurementsPool.process_measurement(measurement["id"])
            self.log.debug(f"Result: {result}")


if __name__ == "__main__":

    MeasurementsPoolTest().run()
