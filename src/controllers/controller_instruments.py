"""
Controller for editing the instruments.
"""

import wx

from src.views.view_instruments import ViewInstruments
from src.views.view_dialogs import ViewDialogs


class ControllerInstruments:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Edit instruments")
        instruments = []
        logger.debug(f"Current instruments: {instruments}")
        dlg = ViewInstruments(parent_view)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                instruments = dlg.get_instruments()
                logger.debug(f"New instruments: {instruments}")
                configuration.update_instruments(instruments)
            except Exception as e:
                logger.error(f"Error updating instruments: {e}")
                ViewDialogs.show_message(parent_view, f"Error updating instruments: {e}",
                                         "Update instruments", wx.ICON_EXCLAMATION)
        dlg.Destroy()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True

    run_data_logger(TestOptions)
