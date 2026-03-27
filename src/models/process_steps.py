"""
Definitions of process steps.

Possible steps:
- Set output of instrument.
- Wait
  - fixed time
  - measurement value has reached a certain value
- Loop

All steps can be conditional on the value of a measurement.
Meaning measurements must be defined prior to the process step.

Process steps are defined using a base class.
"""

import time

from abc import ABC
from abc import abstractmethod
from typing import final

from src.models.instrument_pool import InstrumentPool
from src.models.measurements_pool import MeasurementsPool
from src.models.time_converter import TimeConverter


class ProcessStepBase(ABC):

    def __init__(self, step_data, stop_event, logger):
        self.step_data = step_data
        self.stop_event = stop_event
        self.logger = logger
        self.loop_counter = 0

    ##########
    # Public #
    ##########

    @classmethod
    @final
    def get_class_name(cls):
        return cls.__name__

    @abstractmethod
    def execute(self, step_index):
        pass


class ProcessStepSetOutput(ProcessStepBase):

    name = "Set output"

    def execute(self, step_index):
        instrument = InstrumentPool.get_instrument(self.step_data["instrument_id"])
        self.logger.debug(f"Set output: {instrument.name}, "
                          f"{self.step_data["channel_id"]}, {self.step_data["value"]}")
        instrument.process_channel(self.step_data["channel_id"], self.step_data["value"])
        return step_index + 1


class ProcessStepWait(ProcessStepBase):

    name = "Wait"

    def execute(self, step_index):
        wait_for = self.step_data.get("wait_for")
        wait_time = 0
        interval = 0
        measurement_id = None
        if wait_for == "time":
            wait_time = self.step_data.get("wait_time", 0)
            self.logger.debug(f"Wait for {TimeConverter.create_duration_time_string(wait_time)}")
        elif wait_for == "measurement":
            wait_time = self.step_data.get("timeout", 0)
            interval = self.step_data.get("poll_interval", None)
            min_value = self.step_data.get("min_value", None)
            max_value = self.step_data.get("max_value", None)
            measurement_id = self.step_data.get("measurement_id", None)
            if None in [interval, min_value, max_value, measurement_id]:
                self.logger.error("Invalid settings for this step, skip step")
                return step_index + 1
            self.logger.debug(f"Wait for measurement to be in range of {min_value} - {max_value} "
                f"with a timeout of {TimeConverter.create_duration_time_string(wait_time)}")
        else:
            self.logger.error(f"Invalid wait for: {wait_for}, skip step")
            return step_index + 1

        start = int(time.time())
        sample_time = start
        while not self.stop_event.is_set() and time.time() - start < wait_time:
            if measurement_id is not None and time.time() - sample_time >= interval:
                value = MeasurementsPool.process_measurement(measurement_id)
                if value is None:
                    self.logger.error("Measurement failed, continue with next step")
                    break
                if min_value < value < max_value:
                    self.logger.debug(f"Value is reached: {value}")
                    break
                sample_time = int(time.time())
            time.sleep(0.1)
        else:
            if measurement_id is not None:
                self.logger.error("Measurement timeout, continue with next step")
                self.logger.error(f"Measured value: {value}")

        return step_index + 1


class ProcessStepLoop(ProcessStepBase):

    name = "Loop"

    def execute(self, step_index):
        loop_from = self.step_data.get("loop_from", -1)
        if loop_from < 0:
            self.logger.debug(f"Invalid loop from index ({loop_from}), skip loop")
            return step_index + 1
        count = self.step_data.get("count", 0)
        self.loop_counter += 1
        self.logger.debug(f"Loop: {count} times, current iteration: {self.loop_counter}")
        return loop_from if self.loop_counter < count else step_index + 1


# Export test classes for process runner
STEP_CLASSES = [
    cls for cls in globals().values()
    if isinstance(cls, type)
    and issubclass(cls, ProcessStepBase)
    and cls is not ProcessStepBase
    and cls.__module__ == __name__
]


if __name__ == "__main__":

    from tests.unit_tests.model_tests.process_runner_test import ProcessRunnerTest

    ProcessRunnerTest().run()
