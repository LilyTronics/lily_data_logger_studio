"""
Main controller.
"""

import wx

from src.views.view_main import MainView
from src.models.application_settings import ApplicationSettings

class MainController:

    def __init__(self, title, logger):
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
        self._logger.debug("Show main view")
        self._view.Show()

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)

    ##################
    # Event handlers #
    ##################

    def _on_view_close(self, event):
        self._logger.debug("Close main view")
        self._app_settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_main_window_position(*self._view.GetPosition())
            self._app_settings.store_main_window_size(*self._view.GetSize())

        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger

    run_data_logger(True)
