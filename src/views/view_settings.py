"""
View for the settings.
"""

import wx

import src.models.images as Images
import src.views.view_sizes as ViewSizes

from src.models.time_converter import TimeConverter


class ViewSettings(wx.Dialog):

    _TITLE = "Settings"
    _WINDOW_SIZE = (500, -1)

    def __init__(self, parent, settings):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.settings_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_controls(self), 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_buttons_box(self), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_sample_time)
        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_end_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_sample_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_continuous)

        value, units = TimeConverter.convert_seconds_to_time_with_unit(settings.get("sample_time", 3))
        self._txt_sample_time.SetValue(str(value))
        self._cmb_sample_time.SetValue(units)
        value, units = TimeConverter.convert_seconds_to_time_with_unit(settings.get("end_time", 60))
        self._txt_end_time.SetValue(str(value))
        self._cmb_end_time.SetValue(units)
        if settings.get("continuous_mode", False):
            self._radio_continuous.SetValue(True)
        else:
            self._radio_end_time.SetValue(True)
        self._update_total_samples()

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_controls(self, parent):
        lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, "Sample interval:")
        self._txt_sample_time = wx.TextCtrl(parent, wx.ID_ANY, size=ViewSizes.TEXT_SMALL)
        self._cmb_sample_time = wx.ComboBox(parent, wx.ID_ANY,
                                            style=wx.CB_READONLY, choices=TimeConverter.TIME_UNITS)
        self._radio_end_time = wx.RadioButton(parent, wx.ID_ANY, "Fixed end time:")
        self._radio_end_time.SetValue(True)
        self._txt_end_time = wx.TextCtrl(parent, wx.ID_ANY, size=ViewSizes.TEXT_SMALL)
        self._cmb_end_time = wx.ComboBox(parent, wx.ID_ANY, style=wx.CB_READONLY,
                                         choices=TimeConverter.TIME_UNITS)
        self._radio_continuous = wx.RadioButton(parent, wx.ID_ANY, "Continuous mode:")
        lbl_continuous = wx.StaticText(parent, wx.ID_ANY, "Process must be stopped manually.")
        lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, "Total samples:")
        self._lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, "-")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(lbl_sample_time, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_sample_time, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_sample_time, (0, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_end_time, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_end_time, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_end_time, (1, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_continuous, (2, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(lbl_continuous, (2, 1), (1, 2), wx.ALIGN_TOP)
        grid.Add(lbl_total_samples, (3, 0), wx.DefaultSpan)
        grid.Add(self._lbl_total_samples, (3, 1), (1, 2))

        return grid

    def _create_buttons_box(self, parent):
        btn_ok = wx.Button(parent, wx.ID_OK, "Ok")
        btn_cancel = wx.Button(parent, wx.ID_CANCEL, "Cancel")

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(btn_ok, 0, wx.ALL, ViewSizes.GRID_SPACING)
        box.Add(btn_cancel, 0, wx.ALL, ViewSizes.GRID_SPACING)

        return box

    ##################
    # Event handlers #
    ##################

    def _on_time_change(self, event):
        self._update_total_samples()
        event.Skip()

    ###########
    # Private #
    ###########

    @staticmethod
    def _get_time(value_control, units_control):
        value = 0
        try:
            value = int(value_control.GetValue().strip())
        except ValueError:
            return None
        unit = units_control.GetValue()
        return TimeConverter.convert_time_with_unit_to_seconds(value, unit)

    def _update_total_samples(self):
        total_samples = "-"
        if not self._radio_continuous.GetValue():
            sample_time = self._get_time(self._txt_sample_time, self._cmb_sample_time)
            if sample_time is None or sample_time <= 0:
                total_samples = "Inavlid sample time"
            else:
                end_time = self._get_time(self._txt_end_time, self._cmb_end_time)
                if end_time is None or end_time <= 0:
                    total_samples = "Inavlid end time"
                else:
                    if sample_time > end_time:
                        total_samples = "The sample time must be smaller than the end time"
                    else:
                        total_samples = int(end_time / sample_time) + 1
        self._lbl_total_samples.SetLabel(str(total_samples))

    ##########
    # Public #
    ##########

    def get_settings(self):
        sample_time = self._get_time(self._txt_sample_time, self._cmb_sample_time)
        end_time = self._get_time(self._txt_end_time, self._cmb_end_time)
        if sample_time is None or sample_time <= 0:
            raise Exception("The sample time is invalid")
        if end_time is None or end_time <= 0:
            raise Exception("The end time is invalid")
        if sample_time > end_time:
            raise Exception("The sample time must be smaller than the end time")
        return {
            "sample_time" : sample_time,
            "end_time" : end_time,
            "continuous_mode" : self._radio_continuous.GetValue()
        }


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_settings = True

    run_data_logger(TestOptions)
