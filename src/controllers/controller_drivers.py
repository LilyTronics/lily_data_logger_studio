"""
Controller for the drivers.
"""

import wx

from src.models.drivers import Drivers
from src.views.view_dialogs import ViewDialogs
from src.views.view_progress_dialog import ViewProgressDialog


class ControllerDrivers:

    _step_delay = 500
    _item_delay = 250

    def __init__(self, parent_view, logger, suppress_loading_drivers):
        self._parent_view = parent_view
        self._logger = logger
        self._suppress_loading_drivers = suppress_loading_drivers
        self._view_progress = None

    ###########
    # Private #
    ###########

    def _update_view_progress(self, value, message, new_max=0):
        if self._view_progress is not None:
            t = self._item_delay
            if value < 0:
                t = self._step_delay
                value = 0
            if new_max > 0:
                self._view_progress.set_maximum(new_max)
            self._view_progress.update(value, message)
            wx.YieldIfNeeded()
            wx.MilliSleep(t)

    ##########
    # Public #
    ##########

    def load(self):
        dlg_title = "Load drivers"
        if not self._suppress_loading_drivers:
            self._view_progress = ViewProgressDialog(self._parent_view, dlg_title, 1, 500)
            wx.Yield()
        try:
            Drivers.load(self._update_view_progress)
        except Exception as e:
            self._logger.error(f"Error loading drivers: {e}")
            ViewDialogs.show_message(self._parent_view, f"Error loading drivers: {e}",
                                     dlg_title, wx.ICON_EXCLAMATION)
        if not self._suppress_loading_drivers:
            self._view_progress.destroy()
            self._view_progress = None


if __name__ == "__main__":

    from src.models.logger import Logger

    log = Logger(True)

    app = wx.App(redirect=False)

    c = ControllerDrivers(None, log, False)
    c.load()

    app.MainLoop()

    log.shut_down()
