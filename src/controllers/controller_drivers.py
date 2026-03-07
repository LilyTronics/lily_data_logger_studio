"""
Controller for the drivers.
"""

import wx

from src.models.drivers import Drivers
from src.views.view_progress_dialog import ViewProgressDialog


class ControllerDrivers:

    _step_delay = 1
    _item_delay = 0.5

    def __init__(self, parent_view):
        self._parent_view = parent_view
        self._view_progress = None

    ###########
    # Private #
    ###########

    def _update_view_progress(self, value, message, new_max=0):
        if self._view_progress is not None:
            t = 500
            if value < 0:
                t = 1000
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
        self._view_progress = ViewProgressDialog(self._parent_view, "Load drivers", 1, 500)
        wx.Yield()
        try:
            Drivers.load(self._update_view_progress)
        except Exception as e:
            self._logger.Error(f"Error loading driver: {e}")
        wx.Sleep(1)
        self._view_progress.destroy()
        self._view_progress = None


if __name__ == "__main__":

    app = wx.App(redirect=False)

    c = ControllerDrivers(None)
    c.load()

    app.MainLoop()
