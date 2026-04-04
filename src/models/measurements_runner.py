"""
Runs the measurements.
"""

import threading
import time

from src.models.measurements_pool import MeasurementsPool
from src.models.test_runs import TestRuns
from src.models.time_converter import TimeConverter


class MeasurementsRunner:

    def __init__(self, configuration, logger):
        self._configuration = configuration
        self._logger = logger
        self._thread = None
        self._stop_event = threading.Event()
        self._run_id = None

    ###########
    # Private #
    ###########

    def _request_measurements(self, request_time):
        measurements = self._configuration.get_measurements()
        for measurement in measurements:
            MeasurementsPool.process_measurement(
                measurement["id"], self._process_measurement,
                {"measurement_id": measurement["id"], "request_time": request_time}
            )

    def _process_measurement(self, value, params):
        settings = self._configuration.get_settings()
        response_time = int(time.time())
        # Compare response time to sample window
        next_request_time = params["request_time"] + settings["sample_time"]
        if response_time >= next_request_time:
            # Response came too late
            self._logger.error(f"Response received too late. Response time: {response_time}")
            self._logger.error(f"Must be between: {params["request_time"]} and {next_request_time}")
            self._logger.error(f"Value: {value}")
            value = "time error"
        # Response within the sample window
        TestRuns.store_measurement(self._run_id, params["request_time"],
                                    params["measurement_id"], value)

    def _run_measurement(self):
        time.sleep(0.1)
        self._logger.debug("Measurement runner started")
        settings = self._configuration.get_settings()
        end_time = 0
        if settings["continuous_mode"]:
            self._logger.debug("Running measurements in continuous mode")
        else:
            end_time = settings["end_time"]
            self._logger.debug(
                f"Running measurements for: {TimeConverter.create_duration_time_string(end_time)}")
        self._run_id = TestRuns.new_test_run(self._configuration.get_measurements())
        start = int(time.time())
        do_sample = True
        while not self._stop_event.is_set():
            if do_sample:
                sample_start = int(time.time())
                TestRuns.init_cycle(self._run_id, sample_start)
                self._request_measurements(sample_start)
                do_sample = False
            if time.time() - sample_start >= settings["sample_time"]:
                do_sample = True
            elif 0 < end_time <= time.time() - start:
                self._stop_event.set()
            time.sleep(0.01)
        self._logger.debug("Measurment runner stopped")

    ##########
    # Public #
    ##########

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_measurement)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        if self._thread is not None and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
        self._thread = None

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    def get_run_id(self):
        return self._run_id

    def get_test_run(self):
        return TestRuns.get_test_run(self._run_id)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.measurements_runner_test import MeasurementsRunnerTest

    MeasurementsRunnerTest().run()
