"""
Runs the process steps.
"""

import threading
import time

import src.models.process_steps as ProcessSteps


class ProcessRunner:

    def __init__(self, configuration, logger, update_callback):
        self._configuration = configuration
        self._logger = logger
        self._update_callback = update_callback
        self._thread = None
        self._stop_event = threading.Event()

    ###########
    # Private #
    ###########

    def _run_process(self):
        time.sleep(0.1)
        self._logger.debug("Process runner started")
        config_steps = self._configuration.get_process_steps()
        loop_steps = [x for x in config_steps if x["type"] == "ProcessStepLoop"]
        for loop_step in loop_steps:
            label = loop_step["settings"]["loop_from"]
            index = self._configuration.get_process_step_index_for_label(label)
            loop_step["settings"]["loop_from"] = index
        step_instances = {}
        step_index = 0
        while 0 <= step_index < len(config_steps) and not self._stop_event.is_set():
            # Check if we already have an instance of the step class
            if step_index not in step_instances:
                step_data = config_steps[step_index]
                step_class = [x for x in ProcessSteps.STEP_CLASSES
                              if x.get_class_name() == step_data.get("type")]
                if len(step_class) != 1:
                    raise Exception(f"Invalid step class: {step_data.get("type")}")
                step_instances[step_index] = step_class[0](step_data, self._stop_event,
                                                           self._logger)
            try:
                self._update_callback(step_index)
                step_index = step_instances[step_index].execute(step_index)
            except Exception as e:
                self._logger.error(f"Error running step {step_index}, abort process")
                self._logger.error(f"Error: {e}")
                self._stop_event.set()

        self._logger.debug("Process runner stopped")

    ##########
    # Public #
    ##########

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_process)
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

    from tests.unit_tests.model_tests.process_runner_test import ProcessRunnerTest

    ProcessRunnerTest().run()
