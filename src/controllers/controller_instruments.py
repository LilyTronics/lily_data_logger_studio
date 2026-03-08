"""
Controller for editing the instruments.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialogs import ViewDialogs
from src.views.view_instruments import ViewInstruments


class ControllerInstruments:

    def __init__(self, parent_view, logger):
        self._logger = logger
        self._logger.info("Edit instruments")
        instruments = []
        self._logger.debug(f"Current instruments: {instruments}")
        driver_names = [x.name for x in Drivers.get_drivers()]

        self._dlg = ViewInstruments(parent_view)
        self._dlg.set_driver_names(driver_names)

        self._dlg.Bind(wx.EVT_BUTTON, self._on_add, id=IdManager.ID_INSTRUMENT_ADD)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_INSTRUMENT_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_test, id=IdManager.ID_INSTRUMENT_TEST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_save, id=IdManager.ID_INSTRUMENT_SAVE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_INSTRUMENT_CANCEL)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_INSTRUMENT_CLOSE)

        self._dlg.Bind(wx.EVT_COMBOBOX, self._on_driver_select, id=IdManager.ID_INSTRUMENT_DRIVER)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ###########
    # Private #
    ###########

    def _test_instrument(self):
        settings = self._dlg.get_settings()
        self._dlg.clear_console()
        try:
            driver_class = Drivers.get_driver(settings["driver"])
            assert driver_class is not None, f"No driver found for '{settings["driver"]}'"
            self._dlg.add_console_message(f"Test driver: {driver_class.name}")
            if driver_class.is_simulator:
                start_simulators()
            driver = driver_class(settings["settings"])
            self._dlg.add_console_message("Initialize driver")
            driver.init()
            self._dlg.add_console_message("Run driver test")
            driver.test_driver()
            self._dlg.add_console_message("Shut down driver")
            driver.shut_down()
            self._dlg.add_console_message("Driver test finished (passed)")
        except Exception as e:
            self._dlg.add_console_message(f"Error: {e}")
            self._dlg.add_console_message("Driver test finished (failed)")
        finally:
            stop_simulators()

    ##################
    # Event handlers #
    ##################

    def _on_driver_select(self, event):
        try:
            settings = Drivers.get_settings(event.GetString())
            self._dlg.show_driver_settings(settings)
        except Exception as e:
            self._logger.error(f"Error loading setting: {e}")
            ViewDialogs.show_message(self._dlg, f"Error loading settings: {e}",
                                     "Select driver", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_add(self, event):
        event.Skip()

    def _on_delete(self, event):
        event.Skip()

    def _on_test(self, event):
        self._test_instrument()
        event.Skip()

    def _on_save(self, event):
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
