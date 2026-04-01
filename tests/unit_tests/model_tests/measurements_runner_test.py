"""
Unit test for the measurement runner.
"""

import os

import src.app_data as AppData

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from src.models.instrument_pool import InstrumentPool
from src.models.measurements_runner import MeasurementsRunner
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from tests.lib.test_suite import TestSuite


class MeasurementsRunnerTest(TestSuite):

    measurement_runner = None
    config = Configuration()
    timestamps = []

    def _call_back(self, *params):
        self.log.debug(f"Measurement: {params}")
        self.timestamps.append(params[0])

    def _load_config(self, config_filename):
        self.config.load(os.path.join(AppData.TEST_CONFIG_PATH, config_filename))
        instruments = self.config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        InstrumentPool.clear()
        InstrumentPool.add_instruments(instruments)
        self.fail_if(len(InstrumentPool.get_instruments()) == 0,
                     "No instruments added to the pool")
        measurements = self.config.get_measurements()
        self.fail_if(len(measurements) == 0, "No measurements in the configuration")

    def setup(self):
        start_simulators()
        Drivers.load()
        self.measurement_runner = MeasurementsRunner(
            self.config, self.app_test_logger, self._call_back
        )

    def teardown(self):
        if self.measurement_runner is not None and self.measurement_runner.is_running():
            self.measurement_runner.stop()
        stop_simulators()

    def test_run_measurements_end_time(self):
        del self.timestamps[:]
        self._load_config("test_measurements_end_time.json")
        self.measurement_runner.start()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(not is_running, "Measurements should be running")
        result = self.wait_for(self.measurement_runner.is_running, False, 15, 1)
        self.fail_if(not result, "Measurement runner did not stop")
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(is_running, "Measurements should not be running")
        # Wait for the last callback to be processed
        self.sleep(1)
        self.log.debug(f"Number of measurements: {len(self.timestamps)}")
        self.fail_if(len(self.timestamps) != 6, "Expected 6 measurments")

    def test_run_measurements_continuously(self):
        del self.timestamps[:]
        self._load_config("test_measurements_continuous.json")
        self.measurement_runner.start()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(not is_running, "Measurements should be running")
        result = self.wait_for(self.measurement_runner.is_running, False, 15, 1)
        self.fail_if(result, "Measurement runner stopped unexpectedly")
        self.log.debug("Stop measurement runner")
        self.measurement_runner.stop()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(is_running, "Measurements should not be running")
        # Wait for the last callback to be processed
        self.sleep(1)
        self.log.debug(f"Number of measurements: {len(self.timestamps)}")
        self.fail_if(len(self.timestamps) != 8, "Expected 8 measurments")


if __name__ == "__main__":

    MeasurementsRunnerTest().run()
