"""
Unit test for the measurement runner.
"""

import os
import uuid

import src.app_data as AppData

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from src.models.instrument_pool import InstrumentPool
from src.models.measurements_pool import MeasurementsPool
from src.models.measurements_runner import MeasurementsRunner
from src.models.test_runs import TestRuns
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from tests.lib.test_suite import TestSuite


class MeasurementsRunnerTest(TestSuite):

    measurement_runner = None
    config = Configuration()
    run_id = None

    def setup(self):
        start_simulators()
        Drivers.load()
        self.measurement_runner = MeasurementsRunner(self.config, self.app_test_logger)

    def teardown(self):
        if self.measurement_runner is not None and self.measurement_runner.is_running():
            self.measurement_runner.stop()
        stop_simulators()

    def load_config(self, config_filename):
        self.config.load(os.path.join(AppData.TEST_CONFIG_PATH, config_filename))
        instruments = self.config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        InstrumentPool.clear()
        InstrumentPool.add_instruments(instruments)
        self.fail_if(len(InstrumentPool.get_instruments()) == 0,
                     "No instruments added to the pool")
        measurements = self.config.get_measurements()
        self.fail_if(len(measurements) == 0, "No measurements in the configuration")
        MeasurementsPool.clear()
        MeasurementsPool.add_measurements(measurements)
        self.fail_if(len(MeasurementsPool.get_measurements()) == 0,
                     "No measurements added to the pool")

    def check_test_run_id(self):
        # We need to wait unit the process is running and the test run ID is created
        self.sleep(0.2)
        self.run_id = self .measurement_runner.get_test_run_id()
        self.log.debug(f"Run ID: {self.run_id}")
        uid = uuid.UUID(self.run_id)
        self.fail_if(uid.version != 4, "Invalid run ID")

    def check_test_run_data(self, n_expected):
        test_run = TestRuns.get_test_run(self.run_id)
        self.log.debug(f"Timestamps: {test_run["timestamps"]}")
        n_timestamps = len(test_run["timestamps"])
        self.log.debug(f"Number of timestamps: {n_timestamps}")
        self.fail_if(n_timestamps != n_expected, f"Expected {n_expected} measurments")
        n_samples = set()
        for measurement in test_run["measurements"]:
            self.log.debug(f"Measurement: {measurement["name"]} ({measurement["id"]})")
            self.log.debug(f"Values: {measurement["values"]}")
            n_samples.add(len(measurement["values"]))
            self.fail_if(None in measurement["values"], "Not all values were updated")
        self.log.debug(f"Samples: {n_samples}")
        self.fail_if(len(n_samples) != 1,
                     "Number of samples in the measurement are not consistent")
        n_samples = n_samples.pop()


    def test_run_measurements_end_time(self):
        self.load_config("test_measurements_end_time.json")
        self.measurement_runner.start()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(not is_running, "Measurements should be running")
        self.check_test_run_id()
        result = self.wait_for(self.measurement_runner.is_running, False, 15, 1)
        self.fail_if(not result, "Measurement runner did not stop")
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(is_running, "Measurements should not be running")
        self.check_test_run_data(6)

    def test_run_measurements_continuously(self):
        self.load_config("test_measurements_continuous.json")
        self.measurement_runner.start()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(not is_running, "Measurements should be running")
        self.check_test_run_id()
        result = self.wait_for(self.measurement_runner.is_running, False, 15, 1)
        self.fail_if(result, "Measurement runner stopped unexpectedly")
        self.log.debug("Stop measurement runner")
        self.measurement_runner.stop()
        is_running = self.measurement_runner.is_running()
        self.log.debug(f"Measurements running: {is_running}")
        self.fail_if(is_running, "Measurements should not be running")
        self.check_test_run_data(8)


if __name__ == "__main__":

    MeasurementsRunnerTest().run()
