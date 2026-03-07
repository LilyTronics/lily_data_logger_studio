"""
Controller for editing the instruments.
"""

import wx

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


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
