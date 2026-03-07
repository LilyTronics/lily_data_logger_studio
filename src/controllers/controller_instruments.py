"""
Controller for editing the instruments.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.views.view_instruments import ViewInstruments
from src.views.view_dialogs import ViewDialogs


class ControllerInstruments:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Edit instruments")
        instruments = []
        logger.debug(f"Current instruments: {instruments}")
        driver_names = [x.name for x in Drivers.get_drivers()]

        dlg = ViewInstruments(parent_view)
        dlg.set_driver_names(driver_names)

        dlg.Bind(wx.EVT_BUTTON, self._on_add, id=IdManager.ID_INSTRUMENT_ADD)
        dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_INSTRUMENT_DELETE)
        dlg.Bind(wx.EVT_BUTTON, self._on_test, id=IdManager.ID_INSTRUMENT_TEST)
        dlg.Bind(wx.EVT_BUTTON, self._on_apply, id=IdManager.ID_INSTRUMENT_APPLY)
        dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_INSTRUMENT_CANCEL)
        dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_INSTRUMENT_CLOSE)

        if dlg.ShowModal() == wx.ID_OK:
            pass
            # try:
            #     instruments = dlg.get_instruments()
            #     logger.debug(f"New instruments: {instruments}")
            #     configuration.update_instruments(instruments)
            # except Exception as e:
            #     logger.error(f"Error updating instruments: {e}")
            #     ViewDialogs.show_message(parent_view, f"Error updating instruments: {e}",
            #                              "Update instruments", wx.ICON_EXCLAMATION)
        dlg.Destroy()

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
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
