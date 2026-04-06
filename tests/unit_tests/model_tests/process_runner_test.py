"""
Unit test for the process runner.
"""

import os

import src.app_data as AppData

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from src.models.instrument_pool import InstrumentPool
from src.models.measurements_pool import MeasurementsPool
from src.models.process_runner import ProcessRunner
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from tests.lib.test_suite import TestSuite


class ProcessRunnerTest(TestSuite):

    EXPECTED_INDEXES = [0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7]

    process_runner = None
    indexes = []

    def setup(self):
        Drivers.load()
        config = Configuration()
        config.load(os.path.join(AppData.TEST_CONFIG_PATH, "test_process_runner.json"))
        instruments = config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        InstrumentPool.add_instruments(instruments)
        self.fail_if(len(InstrumentPool.get_instruments()) == 0,
                     "No instruments added to the pool")
        if InstrumentPool.has_simulators():
            start_simulators()
        measurements = config.get_measurements()
        MeasurementsPool.add_measurements(measurements)
        self.process_runner = ProcessRunner(config, self.app_test_logger, self.callback)

    def teardown(self):
        if self.process_runner is not None and self.process_runner.is_running():
            self.process_runner.stop()
        if InstrumentPool.has_simulators():
            stop_simulators()

    def callback(self, step_index):
        self.log.debug(f"Current index: {step_index}")
        self.indexes.append(step_index)

    def test_process_run(self):
        self.app_test_logger.errors = 0
        self.process_runner.start()
        is_running = self.process_runner.is_running()
        self.log.debug(f"Process running: {is_running}")
        self.fail_if(not is_running, "Process should be running")
        while self.process_runner.is_running():
            self.sleep(0.1)
        is_running = self.process_runner.is_running()
        self.log.debug(f"Process running: {is_running}")
        self.fail_if(is_running, "Process should not be running")
        self.fail_if(self.app_test_logger.errors > 0,
                     f"The logger reported {self.app_test_logger.errors} errors")
        self.fail_if(self.indexes != self.EXPECTED_INDEXES,
                     "Sequency of indexes is not correct.")


if __name__ == "__main__":

    ProcessRunnerTest().run()
