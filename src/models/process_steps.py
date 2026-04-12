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
from copy import deepcopy
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
        settings = self.step_data["settings"]
        instrument = InstrumentPool.get_instrument(settings["instrument_id"])
        params = deepcopy(settings)
        del params["instrument_id"]
        del params["channel_id"]
        self.logger.debug(f"Step {step_index + 1}: set output: {instrument.name}, "
                          f"{settings["channel_id"]}, {params}")
        instrument.process_channel(settings["channel_id"], params)
        return step_index + 1


class ProcessStepWait(ProcessStepBase):

    name = "Wait"

    def execute(self, step_index):
        settings = self.step_data["settings"]
        wait_for = settings["wait_for"]
        wait_time = 0
        interval = 0
        measurement_id = None
        if wait_for == "time":
            wait_time = settings.get("wait_time", 0)
            self.logger.debug(
                f"Step {step_index + 1}: "
                f"wait for {TimeConverter.create_duration_time_string(wait_time)}"
            )
        elif wait_for == "measurement":
            wait_time = settings.get("timeout", 0)
            interval = settings.get("poll_interval", None)
            min_value = settings.get("min_value", None)
            max_value = settings.get("max_value", None)
            measurement_id = settings.get("measurement_id", None)
            if None in [interval, min_value, max_value, measurement_id]:
                self.logger.error("Invalid settings for this step, skip step")
                return step_index + 1
            self.logger.debug(
                f"Step {step_index + 1}: "
                f"wait for measurement to be in range of {min_value} - {max_value} "
                f"with a timeout of {TimeConverter.create_duration_time_string(wait_time)}"
            )
        else:
            self.logger.error(f"Error in step {step_index + 1}")
            self.logger.error(f"Invalid wait for: {wait_for}, skip step")
            return step_index + 1

        start = int(time.time())
        sample_time = start
        value = None
        while not self.stop_event.is_set() and time.time() - start < wait_time:
            if measurement_id is not None:
                if (time.time() - sample_time) >= interval:
                    sample_time = int(time.time())
                    value = MeasurementsPool.process_measurement(measurement_id)
                    if value is None:
                        self.logger.error(f"Error in step {step_index + 1}")
                        self.logger.error("Measurement failed, continue with next step")
                        break
                    if min_value < value < max_value:
                        self.logger.debug(f"Value is reached: {value}")
                        break
            time.sleep(0.1)
        else:
            if measurement_id is not None:
                self.logger.error(f"Error in step {step_index + 1}")
                self.logger.error("Measurement timeout, continue with next step")
                self.logger.error(f"Measured value: {value}")

        return step_index + 1


class ProcessStepLoop(ProcessStepBase):

    name = "Loop"

    def execute(self, step_index):
        settings = self.step_data["settings"]
        loop_from = settings.get("loop_from", -1)
        if loop_from < 0:
            self.logger.error(f"Invalid loop from index ({loop_from}), skip loop")
            return step_index + 1
        count = settings.get("count", 0)
        self.loop_counter += 1
        self.logger.debug(
            f"Step {step_index + 1}: loop: {count} times, current iteration: {self.loop_counter}"
        )
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
