"""
Controller for editing the instruments.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.views.view_instruments import ViewInstruments


class ControllerInstruments:

    def __init__(self, parent_view, logger):
        logger.info("Edit instruments")
        instruments = []
        logger.debug(f"Current instruments: {instruments}")
        driver_names = [x.name for x in Drivers.get_drivers()]

        self._dlg = ViewInstruments(parent_view)
        self._dlg.set_driver_names(driver_names)

        self._dlg.Bind(wx.EVT_BUTTON, self._on_add, id=IdManager.ID_INSTRUMENT_ADD)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_INSTRUMENT_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_test, id=IdManager.ID_INSTRUMENT_TEST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_apply, id=IdManager.ID_INSTRUMENT_APPLY)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_INSTRUMENT_CANCEL)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_INSTRUMENT_CLOSE)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ##################
    # Event handlers #
    ##################

    def _on_add(self, event):
        event.Skip()

    def _on_delete(self, event):
        event.Skip()

    def _on_test(self, event):
        event.Skip()

    def _on_apply(self, event):
        event.Skip()

    def _on_cancel(self, event):
        event.Skip()

    def _on_close(self, event):
        self._dlg.Close()
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
