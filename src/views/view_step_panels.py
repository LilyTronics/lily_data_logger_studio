"""
View with settings for each process step.
"""

import wx

from src.models.time_converter import TimeConverter

import src.models.id_manager as IdManager
import src.views.gui_sizes as GuiSizes


class ViewStepPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.create_controls(), 1, wx.EXPAND | wx.LEFT | wx.RIGHT, GuiSizes.BOX_SPACING)

        self.SetSizer(box)


class ViewStepPanelSetOutput(ViewStepPanel):

    name = "Set output"

    def create_controls(self):
        lbl_instrument = wx.StaticText(self, wx.ID_ANY, "Instrument:")
        self._cmb_instruments = wx.ComboBox(self, IdManager.ID_PROCESS_INSTRUMENTS,
                                            style=wx.CB_READONLY)
        lbl_channel = wx.StaticText(self, wx.ID_ANY, "Channel:")
        self._cmb_channels = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY)
        lbl_value = wx.StaticText(self, wx.ID_ANY, "Value:")
        self._txt_value = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_MEDIUM)

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_instrument, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_instruments, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_channel, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_channels, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_value, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_value, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)

        return grid

    def update_settings(self, settings):
        if "instruments" in settings:
            self._cmb_instruments.SetItems(sorted(settings["instruments"]))
        if "channels" in settings:
            self._cmb_channels.SetItems(sorted(settings["channels"]))
        if "selected_instrument" in settings:
            if settings["selected_instrument"] in self._cmb_instruments.GetItems():
                self._cmb_instruments.SetValue(settings["selected_instrument"])
        if "selected_channel" in settings:
            if settings["selected_channel"] in self._cmb_channels.GetItems():
                self._cmb_channels.SetValue(settings["selected_channel"])
        if "value" in settings.get("settings", {}):
            self._txt_value.SetValue(str(settings["settings"]["value"]))

    def get_settings(self):
        return {
            "instrument_name": self._cmb_instruments.GetValue(),
            "channel_name": self._cmb_channels.GetValue(),
            "value": self._txt_value.GetValue().strip()
        }


class ViewStepPanelWait(ViewStepPanel):

    name = "Wait"

    def create_controls(self):
        self._radio_time = wx.RadioButton(self, wx.ID_ANY, "Time:", size=GuiSizes.TEXT_MEDIUM)
        self._radio_time.SetValue(True)
        self._txt_time = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_SMALL)
        self._cmb_time = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                     choices=TimeConverter.TIME_UNITS)

        time_grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        time_grid.Add(self._radio_time, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        time_grid.Add(self._txt_time, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        time_grid.Add(self._cmb_time, (0, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)

        self._radio_measurement = wx.RadioButton(self, wx.ID_ANY, "Measurement:",
                                                 size=GuiSizes.TEXT_MEDIUM)
        lbl_measurement = wx.StaticText(self, wx.ID_ANY, "Measurement:")
        self._cmb_measurements = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY)
        lbl_min = wx.StaticText(self, wx.ID_ANY, "Min:")
        self._txt_min = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_MEDIUM)
        lbl_max = wx.StaticText(self, wx.ID_ANY, "Min:")
        self._txt_max = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_MEDIUM)
        lbl_interval = wx.StaticText(self, wx.ID_ANY, "Poll interval:")
        self._txt_interval = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_SMALL)
        self._cmb_interval = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                         choices=TimeConverter.TIME_UNITS)
        lbl_timeout = wx.StaticText(self, wx.ID_ANY, "Timeout:")
        self._txt_timeout = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_SMALL)
        self._cmb_timeout = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                         choices=TimeConverter.TIME_UNITS)

        measurement_grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        measurement_grid.Add(self._radio_measurement, (1, 0), wx.DefaultSpan,
                             wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(lbl_measurement, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._cmb_measurements, (1, 2), (1, 3), wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(lbl_min, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._txt_min, (2, 2), (1, 3), wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(lbl_max, (3, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._txt_max, (3, 2), (1, 3), wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(lbl_interval, (4, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._txt_interval, (4, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._cmb_interval, (4, 3), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(lbl_timeout, (5, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._txt_timeout, (5, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        measurement_grid.Add(self._cmb_timeout, (5, 3), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(time_grid, 0, wx.EXPAND)
        box.Add(measurement_grid, 0, wx.EXPAND)

        return box

    def update_settings(self, settings):
        if "measurements" in settings:
            self._cmb_measurements.SetItems(sorted(settings["measurements"]))
        if "selected_measurement" in settings:
            if settings["selected_measurement"] in self._cmb_measurements.GetItems():
                self._cmb_measurements.SetValue(settings["selected_measurement"])
        if "wait_for" in settings.get("settings", {}):
            if settings["settings"]["wait_for"] == "time":
                self._radio_time.SetValue(True)
            if settings["settings"]["wait_for"] == "measurement":
                self._radio_measurement.SetValue(True)
        if "wait_time" in settings.get("settings", {}):
            value = settings["settings"]["wait_time"]
            value, unit = TimeConverter.convert_seconds_to_time_with_unit(value)
            self._txt_time.SetValue(str(value))
            if unit in self._cmb_time.GetItems():
                self._cmb_time.SetValue(unit)
        if "min_value" in settings.get("settings", {}):
            self._txt_min.SetValue(str(settings["settings"]["min_value"]))
        if "max_value" in settings.get("settings", {}):
            self._txt_max.SetValue(str(settings["settings"]["max_value"]))
        if "poll_interval" in settings.get("settings", {}):
            value = settings["settings"]["poll_interval"]
            value, unit = TimeConverter.convert_seconds_to_time_with_unit(value)
            self._txt_interval.SetValue(str(value))
            if unit in self._cmb_interval.GetItems():
                self._cmb_interval.SetValue(unit)
        if "timeout" in settings.get("settings", {}):
            value = settings["settings"]["timeout"]
            value, unit = TimeConverter.convert_seconds_to_time_with_unit(value)
            self._txt_timeout.SetValue(str(value))
            if unit in self._cmb_timeout.GetItems():
                self._cmb_timeout.SetValue(unit)

    def get_settings(self):
        settings = {}
        if self._radio_time.GetValue():
            settings["wait_for"] = "time"
            value = int(self._txt_time.GetValue().strip())
            unit = self._cmb_time.GetValue()
            settings["wait_time"] = TimeConverter.convert_time_with_unit_to_seconds(value, unit)
        if self._radio_measurement.GetValue():
            settings["wait_for"] = "measurement"
            settings["measurement_name"] = self._cmb_measurements.GetValue()
            settings["min_value"] = float(self._txt_min.GetValue().strip())
            settings["max_value"] = float(self._txt_max.GetValue().strip())
            value = int(self._txt_interval.GetValue().strip())
            unit = self._cmb_interval.GetValue()
            settings["poll_interval"] = TimeConverter.convert_time_with_unit_to_seconds(value, unit)
            value = int(self._txt_timeout.GetValue().strip())
            unit = self._cmb_timeout.GetValue()
            settings["timeout"] = TimeConverter.convert_time_with_unit_to_seconds(value, unit)
        return settings


class ViewStepPanelLoop(ViewStepPanel):

    name = "Loop"

    def create_controls(self):
        lbl_loop_from = wx.StaticText(self, wx.ID_ANY, "Loop from:")
        self._cmb_labels = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY)
        lbl_count = wx.StaticText(self, wx.ID_ANY, "Count:")
        self._txt_count = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_MEDIUM)

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_loop_from, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_labels, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_count, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_count, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)

        return grid

    def update_settings(self, settings):
        if "labels" in settings:
            self._cmb_labels.SetItems(sorted(settings["labels"]))
        if "loop_from" in settings.get("settings", {}):
            if settings["settings"]["loop_from"] in self._cmb_labels.GetItems():
                self._cmb_labels.SetValue(settings["settings"]["loop_from"])
        if "count" in settings.get("settings", {}):
            self._txt_count.SetValue(str(settings["settings"]["count"]))

    def get_settings(self):
        return {
            "loop_from": self._cmb_labels.GetValue(),
            "count": int(self._txt_count.GetValue().strip())
        }


# Export panels classes for edit process
STEP_PANELS = [
    cls for cls in globals().values()
    if isinstance(cls, type)
    and issubclass(cls, ViewStepPanel)
    and cls is not ViewStepPanel
    and cls.__module__ == __name__
]


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.show_edit_process = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
