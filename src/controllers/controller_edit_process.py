"""
Controller for editing the instruments.
"""

import wx

import src.models.id_manager as IdManager

from src.models.drivers import Drivers
from src.models.process_steps import STEP_CLASSES
from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_process import ViewEditProcess


class ControllerEditProcess:

    def __init__(self, parent_view, logger, configuration):
        self._logger = logger
        self._configuration = configuration
        self._logger.info("Edit process")
        self._selected_index = None

        self._dlg = ViewEditProcess(parent_view)
        self._dlg.set_step_names([x.name for x in STEP_CLASSES])
        self._update_steps()

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_PROCESS_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_new, id=IdManager.ID_PROCESS_NEW)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_down_up,
                       id=IdManager.ID_PROCESS_DOWN, id2=IdManager.ID_PROCESS_UP)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_PROCESS_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_save, id=IdManager.ID_PROCESS_SAVE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_PROCESS_CANCEL)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_PROCESS_CLOSE)
        self._dlg.Bind(wx.EVT_COMBOBOX, self._on_step_select, id=IdManager.ID_PROCESS_STEP)
        self._dlg.Bind(wx.EVT_COMBOBOX, self._on_instrument_select,
                       id=IdManager.ID_PROCESS_INSTRUMENTS)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ###########
    # Private #
    ###########

    def _get_step_name(self, step_type):
        matches = [x.name for x in STEP_CLASSES if x.get_class_name() == step_type]
        return "unknown" if len(matches) != 1 else matches [0]

    def _get_label_names(self):
        steps = self._configuration.get_process_steps()
        return [x["label"] for x in steps if x["label"] != ""]

    def _get_instrument_names(self):
        instruments = self._configuration.get_instruments()
        return [x["name"] for x in instruments]

    def _get_instrument_name(self, instrument_id):
        instrument = self._configuration.get_instrument(instrument_id)
        return "" if instrument is None else instrument["name"]

    def _get_instrument(self, instrument_query):
        instrument = self._configuration.get_instrument(instrument_query)
        if instrument is None:
            raise Exception(f"instrument not found for {instrument_query}")
        return instrument

    def _get_channels(self, instrument, name_filter=None):
        driver_class = Drivers.get_driver(instrument.get("driver_id"))
        if driver_class is None:
            raise Exception(f"driver not found for {instrument["name"]}")
        channels = [x for x in driver_class.get_output_channels()
                        if name_filter is None or x.name == name_filter]
        if len(channels) == 0:
            raise Exception("No channels available")
        return channels

    def _get_channel_names(self, instrument_query, id_filter=None):
        names = []
        try:
            instrument = self._get_instrument(instrument_query)
            channels = self._get_channels(instrument)
            names = [x.name for x in channels if id_filter is None or x.channel_id == id_filter]
        except Exception as e:
            self._logger.error(f"Error loading channels: {e}")
            ViewDialogs.show_message(self._dlg, f"Error loading channels: {e}",
                                     "Select instrument", wx.ICON_EXCLAMATION)
        return names

    def _get_channel_name(self, instrument_id, channel_id):
        channels = self._get_channel_names(instrument_id, channel_id)
        return "" if len(channels) != 1 else channels[0]

    def _get_measurement_names(self):
        measurements = self._configuration.get_measurements()
        return [x["name"] for x in measurements]

    def _get_measurement_name(self, measurement_id):
        measurement = self._configuration.get_measurement(measurement_id)
        return "" if measurement is None else measurement["name"]

    def _get_measurement_id(self, measurement_name):
        measurement = self._configuration.get_measurement(measurement_name)
        return "" if measurement is None else measurement["id"]

    def _update_steps(self, selected_index=-1):
        steps = self._configuration.get_process_steps()
        for step in steps:
            step["step_name"] = self._get_step_name(step["type"])
        self._dlg.set_steps(steps, selected_index)

    def _show_step_data(self, index):
        step = self._configuration.get_process_step(index)
        if step is not None:
            step["step_name"] = self._get_step_name(step["type"])
            step["instruments"] = self._get_instrument_names()
            step["measurements"] = self._get_measurement_names()
            step["labels"] = self._get_label_names()
            if "instrument_id" in step.get("settings", {}):
                instrument_id = step["settings"]["instrument_id"]
                step["selected_instrument"] = self._get_instrument_name(instrument_id)
                step["channels"] = self._get_channel_names(instrument_id)
                if "channel_id" in step.get("settings", {}):
                    channel_id = step["settings"]["channel_id"]
                    step["selected_channel"] = self._get_channel_name(instrument_id, channel_id)
            if "measurement_id" in step.get("settings", {}):
                measurement_id = step["settings"]["measurement_id"]
                step["selected_measurement"] = self._get_measurement_name(measurement_id)
            self._dlg.update_settings(step)
            self._selected_index = index

    def _get_process_step_from_view(self):
        settings = self._dlg.get_settings()
        if settings["name"] == "":
            raise Exception("The name cannot be empty")
        matches = [x for x in STEP_CLASSES if x.name == settings["step_name"]]
        if len(matches) != 1:
            raise Exception(f"No step class found for step {settings["step_name"]}")
        step_settings = settings["settings"]
        value_type = None
        if "instrument_name" in step_settings:
            instrument = self._get_instrument(step_settings["instrument_name"])
            step_settings["instrument_id"] = instrument["id"]
            del step_settings["instrument_name"]
            if "channel_name" in step_settings:
                channel = self._get_channels(instrument, step_settings["channel_name"])
                if len(channel) == 1:
                    step_settings["channel_id"] = channel[0].channel_id
                    value_type = channel[0].value_type
                del step_settings["channel_name"]
        if "value" in step_settings:
            if value_type is None:
                raise Exception("The value type is not defined for this channel")
            step_settings["value"] = value_type(step_settings["value"])
        if "measurement_name" in step_settings:
            step_settings["measurement_id"] = self._get_measurement_id(
                step_settings["measurement_name"])
            del step_settings["measurement_name"]
        if "loop_from" in step_settings:
            if step_settings["loop_from"] == "":
                raise Exception("Loop from cannot be empty")
        step = self._configuration.get_new_process_step()
        step["insert"] = settings["insert"]
        step["name"] = settings["name"]
        step["label"] = settings["label"]
        step["type"] = matches[0].get_class_name()
        step["settings"] = step_settings
        return step

    ##################
    # Event handlers #
    ##################

    def _on_activated(self, event):
        self._show_step_data(event.GetIndex())
        event.Skip()

    def _on_step_select(self, event):
        settings = {
            "instruments": self._get_instrument_names(),
            "measurements": self._get_measurement_names(),
            "labels": self._get_label_names()
        }
        self._dlg.show_step_panel(event.GetString())
        self._dlg.update_settings(settings)
        event.Skip()

    def _on_instrument_select(self, event):
        instrument_name = event.GetString()
        self._dlg.update_settings({"channels": self._get_channel_names(instrument_name)})
        event.Skip()

    def _on_new(self, event):
        step = self._configuration.get_new_process_step()
        self._dlg.update_settings(step, True)
        self._selected_index = None
        event.Skip()

    def _on_down_up(self, event):
        index = self._dlg.get_selected_index()
        if index >= 0:
            btn_id = event.GetId()
            direction = 1 if btn_id == IdManager.ID_PROCESS_DOWN else -1
            self._configuration.move_process_step(index, direction)
            self._update_steps(index + direction)
        event.Skip()

    def _on_save(self, event):
        try:
            step = self._get_process_step_from_view()
            self._logger.debug(f"Save step: {step}")
            if self._selected_index is None:
                position = step["insert"]
                del step["insert"]
                self._configuration.add_process_step(step["name"], step["label"], step["type"],
                                                     step["settings"], position)
                steps = self._configuration.get_process_steps()
                self._selected_index = position if position >= 0 else len(steps) - 1
            else:
                self._configuration.update_process_step(self._selected_index, step["name"],
                                                    step["label"], step["type"], step["settings"])
        except Exception as e:
            self._logger.error(f"Error saving instrument: {e}")
            ViewDialogs.show_message(self._dlg, f"Error saving instrument: {e}",
                                     "Save Instrument", wx.ICON_EXCLAMATION)
            return
        self._update_steps()
        event.Skip()

    def _on_cancel(self, event):
        if self._selected_index is not None:
            self._show_step_data(self._selected_index)
        event.Skip()

    def _on_delete(self, event):
        index = self._dlg.get_selected_index()
        if index >= 0:
            dlg_title = "Delete process step"
            btn = ViewDialogs.show_confirm(
                self._dlg,
                f"Are you sure you want to delete the process stap at position {index + 1}?",
                dlg_title
            )
            if btn == wx.ID_YES:
                try:
                    self._configuration.delete_process_step(index)
                    self._selected_index = None
                    self._update_steps()
                except Exception as e:
                    self._logger.error(f"Error deleting process step: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting process step: {e}",
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
    TestOptions.show_edit_process = True

    run_data_logger(TestOptions)
