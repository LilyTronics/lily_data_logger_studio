"""
Controller for editing the measurements.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_measurements import ViewEditMeasurements


class ControllerEditMeasurements:

    def __init__(self, parent_view, logger, configuration):
        self._logger = logger
        self._configuration = configuration
        self._logger.info("Edit measurements")
        self._selected_id = None
        instrument_names = [x["name"] for x in self._configuration.get_instruments()]

        self._dlg = ViewEditMeasurements(parent_view)
        self._dlg.set_instrument_names(instrument_names)

        self._update_measurements()

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_MEASUREMENT_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_new, id=IdManager.ID_MEASUREMENT_NEW)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_MEASUREMENT_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_test, id=IdManager.ID_MEASUREMENT_TEST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_save, id=IdManager.ID_MEASUREMENT_SAVE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_MEASUREMENT_CANCEL)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_MEASUREMENT_CLOSE)
        self._dlg.Bind(wx.EVT_COMBOBOX, self._on_instrument_select,
                       id=IdManager.ID_MEASUREMENT_INSTRUMENT)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ###########
    # Private #
    ###########

    def _update_measurements(self):
        self._dlg.set_measurements(self._configuration.get_measurements())

    def _show_measurement(self):
        measurement = self._configuration.get_measurement(self._selected_id)
        instrument = self._get_instrument_from_configuration(measurement["instrument_id"])
        driver_class = self._get_driver_class_for_instrument(measurement["instrument_id"])
        channel = driver_class.get_channel(measurement["channel_id"])
        measurement["instrument_name"] = instrument["name"]
        measurement["channels"] = driver_class.get_input_channels()
        measurement["channel_name"] = channel.name
        self._dlg.show_measurement(measurement)

    def _get_instrument_from_configuration(self, instrument_name):
        instrument = self._configuration.get_instrument(instrument_name)
        if instrument is None:
            raise Exception("instrument not found in the configuration")
        return instrument

    def _get_driver_class_for_instrument(self, instrument_name):
        instrument = self._get_instrument_from_configuration(instrument_name)
        driver_class = Drivers.get_driver(instrument.get("driver_id"))
        if driver_class is None:
            raise Exception(f"driver not found for {instrument_name}")
        return driver_class

    def _log_to_console(self, message):
        self._dlg.add_console_message(message.strip())

    def _test_measurement(self):
        try:
            settings = self._dlg.get_settings()
            self._dlg.clear_console()
            instrument = self._get_instrument_from_configuration(settings.get("instrument_name"))
            driver_class = self._get_driver_class_for_instrument(settings.get("instrument_name"))
            self._log_to_console(f"Test measurement using driver: {driver_class.name}")
            if driver_class.is_simulator:
                start_simulators()
            driver = driver_class(instrument.get("settings", {}))
            channel_name = settings.get("channel_name")
            self._log_to_console(f"Get value for channel: {channel_name}")
            value = driver.process_channel(channel_name)
            self._log_to_console(f"Value from channel: {value}")
            if isinstance(value, (int, float)):
                unit = settings.get("unit")
                gain = settings.get("gain")
                offset = settings.get("offset")
                self._log_to_console(f"Apply gain and offset: {gain}, {offset}")
                value = type(value)(value * gain + offset)
                self._log_to_console(f"Measurement value: {value} {unit}")
            self._log_to_console("Measurement test finished (passed)")
        except Exception as e:
            self._log_to_console(f"Error: {e}")
            self._log_to_console("Measurement test finished (failed)")
        finally:
            stop_simulators()

    def _get_measurement_from_view(self):
        settings = self._dlg.get_settings()
        instrument = self._get_instrument_from_configuration(settings.get("instrument_name"))
        driver_class = self._get_driver_class_for_instrument(settings.get("instrument_name"))
        channel = driver_class.get_channel(settings.get("channel_name"))
        if channel is None:
            raise Exception("Channel not found in the driver")
        measurement = self._configuration.get_new_measurement()
        measurement["id"] = self._selected_id
        measurement["name"] = settings.get("name")
        measurement["instrument_id"] = instrument["id"]
        measurement["channel_id"] = channel.channel_id
        measurement["unit"] = settings.get("unit")
        measurement["gain"] = settings.get("gain")
        measurement["offset"] = settings.get("offset")
        if measurement["name"] == "":
            raise Exception("Name cannot be empty")
        return measurement

    ##################
    # Event handlers #
    ##################

    def _on_activated(self, event):
        measurement_id = event.GetEventObject().id_map.get(event.GetIndex())
        if measurement_id is not None:
            self._selected_id = measurement_id
            self._show_measurement()
        event.Skip()

    def _on_instrument_select(self, event):
        try:
            driver_class = self._get_driver_class_for_instrument(event.GetString())
            self._dlg.update_channels(driver_class.get_input_channels())
        except Exception as e:
            self._logger.error(f"Error loading channels: {e}")
            ViewDialogs.show_message(self._dlg, f"Error loading channels: {e}",
                                     "Select instrument", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_new(self, event):
        measurement = self._configuration.get_new_measurement()
        self._selected_id = None
        measurement["instrument_name"] = ""
        measurement["channels"] = []
        measurement["channel_name"] = ""
        self._dlg.show_measurement(measurement)
        event.Skip()

    def _on_test(self, event):
        self._test_measurement()
        event.Skip()

    def _on_save(self, event):
        try:
            measurement = self._get_measurement_from_view()
            self._logger.debug(f"Save instrument: {measurement}")
            if self._selected_id is None:
                self._configuration.add_measurement(measurement["name"],
                    measurement["instrument_id"],measurement["channel_id"], measurement["unit"],
                    measurement["gain"], measurement["offset"])
            else:
                self._configuration.update_measurement(self._selected_id, measurement["name"],
                    measurement["instrument_id"],measurement["channel_id"], measurement["unit"],
                    measurement["gain"], measurement["offset"])
        except Exception as e:
            self._logger.error(f"Error saving measurement: {e}")
            ViewDialogs.show_message(self._dlg, f"Error saving measurement: {e}",
                                     "Save measurement", wx.ICON_EXCLAMATION)
            return
        self._update_measurements()
        event.Skip()

    def _on_cancel(self, event):
        self._show_measurement()
        event.Skip()

    def _on_delete(self, event):
        if self._selected_id is not None:
            dlg_title = "Delete measurement"
            btn = ViewDialogs.show_confirm(self._dlg,
                                           "Are you sure you want to delete this measurement?",
                                           dlg_title)
            if btn == wx.ID_YES:
                try:
                    self._configuration.delete_measurement(self._selected_id)
                    self._selected_id = None
                    self._update_measurements()
                except Exception as e:
                    self._logger.error(f"Error deleting measurement: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting measurement: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
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
    TestOptions.show_edit_measurements = True

    run_data_logger(TestOptions)
