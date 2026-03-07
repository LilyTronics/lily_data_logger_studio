"""
Data logger object
- Runs the process runner
- Does measurments
- Storing the results in the proper places.
"""


class DataLogger:

    def __init__(self, configuration, gui_callback):
        self._thread = None
        self._configuration = configuration
        self._gui_callback = gui_callback

    ##########
    # Public #
    ##########

    def start(self):
        self._gui_callback({"status": "running"})

    def stop(self):
        self._gui_callback({"status": "idle"})


if __name__ == "__main__":

    from tests.unit_tests.model_tests.data_logger_test import DataLoggerTest

    DataLoggerTest().run()
