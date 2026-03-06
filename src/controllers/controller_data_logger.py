"""
Controller for the data logger.
"""

import wx

from src.models.data_logger import DataLogger
from src.views.view_dialogs import ViewDialogs


class ControllerDataLogger:

    def __init__(self, parent_view, configuration, logger):
        self._parent_view = parent_view
        self._configuration = configuration
        self._logger = logger
        self._data_logger = DataLogger(self._configuration, self._on_data_logger_update)

    ###########
    # Private #
    ###########

    def _on_data_logger_update(self, data):
        if "status" in data:
            wx.CallAfter(self._parent_view.update_status, data["status"])

    ##########
    # Public #
    ##########

    def start(self):
        self._logger.info("Start data logger")
        try:
            self._data_logger.start()
        except Exception as e:
            self._logger.error(f"Error starting data logger: {e}")
            ViewDialogs.show_message(self._parent_view, f"Error starting data logger: {e}",
                                     "Start data logger", wx.ICON_EXCLAMATION)

    def stop(self):
        self._logger.info("Stop data logger")
        self._data_logger.stop()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
