"""
Controller for editing the instruments.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_instruments import ViewEditInstruments


class ControllerEditInstruments:

    def __init__(self, parent_view, logger, configuration):
        self._logger = logger
        self._configuration = configuration
        self._logger.info("Edit instruments")
        driver_names = [x.name for x in Drivers.get_drivers()]
        self._selected_id = None

        self._dlg = ViewEditInstruments(parent_view)
        self._dlg.set_driver_names(driver_names)
        self._update_instruments()

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_INSTRUMENT_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_new, id=IdManager.ID_INSTRUMENT_NEW)
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

    def _update_instruments(self):
        self._dlg.set_instruments(self._configuration.get_instruments())

    def _log_to_console(self, message):
        if "|" in message:
            message = message.split("|")[-1]
        self._dlg.add_console_message(message.strip())

    def _test_instrument(self):
        self._logger.set_stdout_callback(self._log_to_console)
        try:
            settings = self._dlg.get_settings()
            self._dlg.clear_console()
            driver_class = Drivers.get_driver(settings["driver_name"])
            if driver_class is None:
                raise ValueError(f"No driver found for '{settings['driver_name']}'")
            self._log_to_console(f"Test driver: {driver_class.name}")
            if driver_class.is_simulator:
                start_simulators()
            self._log_to_console("Initialize driver")
            driver = driver_class(settings["settings"], "DPT")
            self._log_to_console("Run driver test")
            driver.test_driver()
            self._log_to_console("Driver test finished (passed)")
        except Exception as e:
            self._log_to_console(f"Error: {e}")
            self._log_to_console("Driver test finished (failed)")
        finally:
            stop_simulators()
        self._logger.set_stdout_callback(None)

    def _get_instrument_from_view(self):
        settings = self._dlg.get_settings()
        driver_class = Drivers.get_driver(settings["driver_name"])
        if driver_class is None:
            raise Exception(f"Driver {settings["driver_name"]} is not found")
        instrument = self._configuration.get_new_instrument()
        instrument["id"] = self._selected_id
        instrument["name"] = settings["name"]
        instrument["driver_id"] = driver_class.id
        instrument["settings"] = settings["settings"]
        if instrument["name"] == "":
            raise Exception("Name cannot be empty")
        return instrument

    def _show_instrument(self):
        instrument = self._configuration.get_instrument(self._selected_id)
        driver_class = Drivers.get_driver(instrument["driver_id"])
        instrument["driver_name"] = driver_class.name
        self._dlg.show_instrument(instrument, driver_class.driver_settings)

    ##################
    # Event handlers #
    ##################

    def _on_activated(self, event):
        instrument_id = event.GetEventObject().id_map.get(event.GetIndex(), None)
        if instrument_id is not None:
            self._selected_id = instrument_id
            self._show_instrument()
        event.Skip()

    def _on_driver_select(self, event):
        try:
            settings = Drivers.get_settings(event.GetString())
            self._dlg.show_driver_settings(settings)
        except Exception as e:
            self._logger.error(f"Error loading setting: {e}")
            ViewDialogs.show_message(self._dlg, f"Error loading settings: {e}",
                                     "Select driver", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_new(self, event):
        instrument = self._configuration.get_new_instrument()
        self._selected_id = None
        self._dlg.show_instrument(instrument, None)
        event.Skip()

    def _on_delete(self, event):
        instrument_name = self._dlg.get_selected_instrument()
        instrument = self._configuration.get_instrument(instrument_name)
        if instrument is not None:
            dlg_title = "Delete instrument"
            btn = ViewDialogs.show_confirm(self._dlg,
                                           f"Are you sure you want to delete {instrument["name"]}?",
                                           dlg_title)
            if btn == wx.ID_YES:
                try:
                    self._configuration.delete_instrument(instrument["id"])
                    self._selected_id = None
                    self._update_instruments()
                except Exception as e:
                    self._logger.error(f"Error deleting instrument: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting instrument: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_test(self, event):
        self._test_instrument()
        event.Skip()

    def _on_save(self, event):
        try:
            instrument = self._get_instrument_from_view()
            self._logger.debug(f"Save instrument: {instrument}")
            if self._selected_id is None:
                self._configuration.add_instrument(instrument["name"], instrument["driver_id"],
                                                   instrument["settings"])
            else:
                self._configuration.update_instrument(instrument["id"], instrument["name"],
                                                      instrument["driver_id"],
                                                      instrument["settings"])
        except Exception as e:
            self._logger.error(f"Error saving instrument: {e}")
            ViewDialogs.show_message(self._dlg, f"Error saving instrument: {e}",
                                     "Save Instrument", wx.ICON_EXCLAMATION)
            return
        self._update_instruments()
        event.Skip()

    def _on_cancel(self, event):
        self._show_instrument()
        event.Skip()

    def _on_close(self, event):
        self._dlg.Close()
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.suppress_loading_drivers = True
    TestOptions.show_edit_instruments = True

    run_data_logger(TestOptions)
