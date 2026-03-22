"""
Runs the measurements.
"""

import threading
import time

from src.models.instrument_pool import InstrumentPool
from src.models.time_converter import TimeConverter


class MeasurementsRunner:

    def __init__(self, configuration, logger, measurement_callback):
        self._configuration = configuration
        self._logger = logger
        self._measurement_callback = measurement_callback
        self._thread = None
        self._stop_event = threading.Event()

    ###########
    # Private #
    ###########

    def _request_measurements(self, request_time):
        measurements = self._configuration.get_measurements()
        for measurement in measurements:
            instrument = InstrumentPool.get_instrument(measurement["instrument_id"])
            instrument.process_channel(measurement["channel_id"],
                                       callback=self._process_measurement,
                                       callback_params=(request_time,))

    def _process_measurement(self, value, params):
        _response_time = int(time.time())
        request_time = params[0]
        self._measurement_callback(request_time, value)

    def _run_measurement(self):
        self._logger.debug("Measurement runner started")
        settings = self._configuration.get_settings()
        end_time = 0
        if settings["continuous_mode"]:
            self._logger.debug("Running measurements in continuous mode")
        else:
            end_time = settings["end_time"]
            self._logger.debug(
                f"Running measurements for: {TimeConverter.create_duration_time_string(end_time)}")
        start = int(time.time())
        do_sample = True
        while not self._stop_event.is_set():
            if do_sample:
                sample_start = int(time.time())
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


if __name__ == "__main__":

    from tests.unit_tests.model_tests.measurements_runner_test import MeasurementsRunnerTest

    MeasurementsRunnerTest().run()
