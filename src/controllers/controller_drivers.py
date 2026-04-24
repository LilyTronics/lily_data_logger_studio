"""
Controller for the drivers.
"""

import wx

from src.models.drivers import Drivers
from src.views.view_dialogs import ViewDialogs
from src.views.view_dialog_progress import ViewDialogProgress


class ControllerDrivers:

    _step_delay = 500
    _item_delay = 100

    def __init__(self, parent_view, logger, suppress_loading_drivers):
        self._parent_view = parent_view
        self._logger = logger
        self._suppress_loading_drivers = suppress_loading_drivers
        self._view_progress = None

    ###########
    # Private #
    ###########

    def _update_view_progress(self, value, message):
        if self._view_progress is not None:
            t = self._item_delay
            if value < 0 or value == 100:
                t = self._step_delay
            self._view_progress.update(int(value), message)
            while t > 0:
                wx.MilliSleep(10)
                t -= 10
                wx.Yield()

    ##########
    # Public #
    ##########

    def load(self):
        dlg_title = "Load drivers"
        if not self._suppress_loading_drivers:
            self._view_progress = ViewDialogProgress(self._parent_view, dlg_title, frame_width=500)
        try:
            Drivers.load(self._update_view_progress)
        except Exception as e:
            self._logger.error(f"Error loading drivers: {e}")
            ViewDialogs.show_message(self._parent_view, f"Error loading drivers: {e}",
                                     dlg_title, wx.ICON_EXCLAMATION)
        if self._view_progress is not None:
            self._view_progress.Destroy()
            self._view_progress = None


if __name__ == "__main__":

    import src.app_data as AppData
    from src.models.logger import Logger


    log = Logger(AppData.APP_LOG_FILE, True)

    app = wx.App(redirect=False)

    c = ControllerDrivers(None, log, False)
    c.load()

    app.MainLoop()

    log.shut_down()
