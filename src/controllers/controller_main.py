"""
Main controller.
"""

import wx

from src.models.application_settings import ApplicationSettings
from src.models.test_options import TestOptions
from src.views.view_data_table import ViewDataTable
from src.views.view_main import MainView


class MainController:

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start main controller")
        self._app_settings = ApplicationSettings()

        self._logger.debug("Load main view")
        self._view = MainView(title)
        value = self._app_settings.get_main_window_position()
        if -1 not in value:
            self._view.SetPosition(value)
        value = self._app_settings.get_main_window_size()
        if -1 not in value:
            self._view.SetSize(value)
        self._view.Maximize(self._app_settings.get_main_window_maximized())
        self._view.set_tree_width(self._app_settings.get_main_window_tree_width())
        self._logger.debug("Show main view")
        self._view.Show()

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)

        # Test options
        if test_options.show_view_data_table:
            self._logger.debug("Test option: show view data table")
            cw = ViewDataTable(self._view)
            cw.Show()

    ##################
    # Event handlers #
    ##################

    def _on_view_close(self, event):
        self._logger.debug("Close main view")
        self._app_settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_main_window_position(*self._view.GetPosition())
            self._app_settings.store_main_window_size(*self._view.GetSize())
        self._app_settings.store_main_window_tree_width(self._view.get_tree_width())

        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
