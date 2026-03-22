"""
Controller for the data logger.
"""


class ControllerDataLogger:

    def __init__(self, parent_view, configuration, logger):
        self._parent_view = parent_view
        self._configuration = configuration
        self._logger = logger

    ##########
    # Public #
    ##########

    def start(self):
        self._logger.info("Start data logger")

    def stop(self):
        self._logger.info("Stop data logger")


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
