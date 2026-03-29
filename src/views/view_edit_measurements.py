"""
View for the measurements.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as ViewSizes


class ViewEditMeasurements(wx.Dialog):

    _TITLE = "Measurements"
    _WINDOW_SIZE = (800, 500)
    _COL_WIDTH = 180
    _COLOR_DEFAULT = "#000"
    _COLOR_ERROR = "#f60"

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)
        self._settings_controls = {}
        self._channels = []

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.data_table_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(), 2, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_controls(), 5, wx.EXPAND)

        self.Bind(wx.EVT_COMBOBOX, self._on_channel_select, id=IdManager.ID_MEASUREMENT_CHANNEL)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    ###########
    # Private #
    ###########

    def _create_list(self):
        self._lst_measurements = wx.ListCtrl(self, IdManager.ID_MEASUREMENT_LIST,
                                            style=wx.LC_REPORT | wx.LC_NO_SORT_HEADER)
        self._lst_measurements.InsertColumn(0, "Measurements:", width=self._COL_WIDTH)
        self._lst_measurements.id_map = {}

        btn_add = wx.Button(self, IdManager.ID_MEASUREMENT_NEW, "New")
        btn_delete = wx.Button(self, IdManager.ID_MEASUREMENT_DELETE,"Delete")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(self._lst_measurements, (0, 0), (1, 2), wx.EXPAND)
        grid.Add(btn_add, (1, 0), wx.DefaultSpan)
        grid.Add(btn_delete, (1, 1), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self):
        # Placeholder for channel settings
        self._settings_grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        self._settings_grid.Add(wx.Panel(self), (0, 0))

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_general_controls(), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._settings_grid, 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_conversion_settings(), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_test_console(), 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_buttons(), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        return box

    def _create_general_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, wx.ID_ANY)
        lbl_instrument = wx.StaticText(self, wx.ID_ANY, "Instrument:")
        self._cmb_instruments = wx.ComboBox(self, IdManager.ID_MEASUREMENT_INSTRUMENT,
                                            style=wx.CB_READONLY)
        lbl_channel = wx.StaticText(self, wx.ID_ANY, "Channel:")
        self._cmb_channels = wx.ComboBox(self, IdManager.ID_MEASUREMENT_CHANNEL,
                                            style=wx.CB_READONLY)

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(lbl_instrument, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_instruments, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_channel, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_channels, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(1)

        return grid

    def _create_conversion_settings(self):
        lbl_unit = wx.StaticText(self, wx.ID_ANY, "Unit:")
        self._txt_unit = wx.TextCtrl(self, wx.ID_ANY, size=ViewSizes.WIDTH_MEDIUM)
        lbl_gain = wx.StaticText(self, wx.ID_ANY, "Gain:")
        self._txt_gain = wx.TextCtrl(self, wx.ID_ANY, size=ViewSizes.WIDTH_MEDIUM)
        lbl_offset = wx.StaticText(self, wx.ID_ANY, "Offset:")
        self._txt_offset = wx.TextCtrl(self, wx.ID_ANY, size=ViewSizes.WIDTH_MEDIUM)
        lbl_msg_1 = wx.StaticText(self, wx.ID_ANY, "The actual value will be: "
                                                   "actual = measured * gain + offset")
        self._txt_gain.SetValue("1.0")
        self._txt_offset.SetValue("0.0")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(lbl_unit, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_unit, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_gain, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_gain, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_offset, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_offset, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_msg_1, (3, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)

        return grid

    def _create_test_console(self):
        self._txt_console = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP |
                                        wx.TE_READONLY | wx.TE_RICH)
        self._txt_console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_NORMAL, False))
        return self._txt_console

    def _create_buttons(self):
        btn_test = wx.Button(self, IdManager.ID_MEASUREMENT_TEST, "Test")
        btn_save = wx.Button(self, IdManager.ID_MEASUREMENT_SAVE, "Save")
        btn_cancel = wx.Button(self, IdManager.ID_MEASUREMENT_CANCEL, "Cancel")
        btn_close = wx.Button(self, IdManager.ID_MEASUREMENT_CLOSE, "Close")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(btn_test, (0, 0), wx.DefaultSpan)
        grid.Add(btn_save, (0, 1), wx.DefaultSpan)
        grid.Add(btn_cancel, (0, 2), wx.DefaultSpan)
        grid.Add(btn_close, (0, 3), wx.DefaultSpan, wx.ALIGN_RIGHT)
        grid.AddGrowableCol(3)

        return grid

    def _show_channel_parameters(self, parameters):
        # Show channel settings
        self._settings_controls.clear()
        self._settings_grid.Clear(True)
        if len(parameters) == 0:
            self._settings_grid.Add(wx.Panel(self), (0, 0))
        else:
            try:
                for i, param in enumerate(parameters):
                    lbl = wx.StaticText(self, wx.ID_ANY, f"{param.name}:")
                    ctrl_class = getattr(wx, param.gui_control)
                    ctrl = ctrl_class(self, wx.ID_ANY, size=ViewSizes.WIDTH_MEDIUM)
                    ctrl.SetValue(str(param.default_value))
                    self._settings_grid.Add(lbl, (i, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                    self._settings_grid.Add(ctrl, (i, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                    self._settings_controls[param.name] = (ctrl, param.type)
            except:
                # Restore layout
                self._settings_grid.Add(wx.Panel(self), (0, 0))
                self.Layout()
                raise
        self.Layout()

    ##################
    # Event handlers #
    ##################

    def _on_channel_select(self, event):
        channel = [x for x in self._channels if x.name == event.GetString()]
        if len(channel) > 0:
            self._show_channel_parameters(channel[0].parameters)

    ##########
    # Public #
    ##########

    def get_selected_measurement(self):
        index = self._lst_measurements.GetFirstSelected()
        if index >= 0:
            return self._lst_measurements.GetItemText(index)
        return ""

    def set_measurements(self, measurements):
        self._lst_measurements.DeleteAllItems()
        self._lst_measurements.id_map.clear()
        for measurement in sorted(measurements, key=lambda x: x["name"]):
            index = self._lst_measurements.InsertItem(self._lst_measurements.GetItemCount(),
                                                      measurement["name"])
            self._lst_measurements.id_map[index] = measurement["id"]

    def set_instrument_names(self, instrument_names):
        self._cmb_instruments.SetItems(instrument_names)
        self.Layout()

    def update_channels(self, channels):
        names = [x.name for x in channels]
        self._cmb_channels.SetItems(sorted(names))
        self._channels = channels
        self.Layout()

    def show_measurement(self, measurement):
        self._txt_name.SetValue(measurement["name"])
        if measurement["instrument_name"] in self._cmb_instruments.GetItems():
            self._cmb_instruments.SetValue(measurement["instrument_name"])
            self.update_channels(measurement["channels"])
            if measurement["channel_name"] in self._cmb_channels.GetItems():
                self._cmb_channels.SetValue(measurement["channel_name"])
            else:
                self._cmb_channels.SetSelection(wx.NOT_FOUND)
        else:
            self._cmb_instruments.SetSelection(wx.NOT_FOUND)
        self._txt_unit.SetValue(measurement["unit"])
        self._txt_gain.SetValue(str(measurement["gain"]))
        self._txt_offset.SetValue(str(measurement["offset"]))

    def get_settings(self):
        settings = {
            "name": self._txt_name.GetValue().strip(),
            "instrument_name": self._cmb_instruments.GetValue(),
            "channel_name": self._cmb_channels.GetValue(),
            "unit": self._txt_unit.GetValue().strip(),
            "gain": float(self._txt_gain.GetValue().strip()),
            "offset": float(self._txt_offset.GetValue().strip()),
            "settings": {}
        }
        for key, (ctrl, ctrl_type) in self._settings_controls.items():
            value = None
            try:
                value = ctrl.GetValue().strip()
                settings["settings"][key] = ctrl_type(value)
            except Exception as e:
                raise ValueError(
                    f"Invalid value for setting {key}: '{value}'. "
                    f"Expected type: {ctrl_type.__name__}"
                ) from e
        return settings

    def clear_console(self):
        self._txt_console.Clear()

    def add_console_message(self, message):
        self._txt_console.SetDefaultStyle(wx.TextAttr(self._COLOR_DEFAULT))
        if "error" in message.lower():
            self._txt_console.SetDefaultStyle(wx.TextAttr(self._COLOR_ERROR))
        self._txt_console.AppendText(f"{message}\n")


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.show_edit_measurements = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
