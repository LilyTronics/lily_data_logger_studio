"""
View for the instruments.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as ViewSizes


class ViewEditInstruments(wx.Dialog):

    _TITLE = "Instruments"
    _WINDOW_SIZE = (800, 500)
    _COL_WIDTH = 180
    _COLOR_DEFAULT = "#000"
    _COLOR_ERROR = "#f60"

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)
        self._settings_controls = {}

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.instruments_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(), 2, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_controls(), 5, wx.EXPAND)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self):
        self._lst_instruments = wx.ListCtrl(self, IdManager.ID_INSTRUMENT_LIST,
                                            style=wx.LC_SINGLE_SEL | wx.LC_REPORT |
                                            wx.LC_NO_SORT_HEADER)
        self._lst_instruments.InsertColumn(0, "Instruments:", width=self._COL_WIDTH)
        self._lst_instruments.id_map = {}

        btn_add = wx.Button(self, IdManager.ID_INSTRUMENT_NEW, "New")
        btn_delete = wx.Button(self, IdManager.ID_INSTRUMENT_DELETE,"Delete")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(self._lst_instruments, (0, 0), (1, 2), wx.EXPAND)
        grid.Add(btn_add, (1, 0), wx.DefaultSpan)
        grid.Add(btn_delete, (1, 1), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self):
        # Placeholder for driver settings
        self._settings_grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        self._settings_grid.Add(wx.Panel(self), (0, 0))

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_general_controls(), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._settings_grid, 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_test_console(), 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_buttons(), 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        return box

    def _create_general_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, wx.ID_ANY)
        lbl_drivers = wx.StaticText(self, wx.ID_ANY, "Driver:")
        self._cmb_drivers = wx.ComboBox(self, IdManager.ID_INSTRUMENT_DRIVER,
                                        style=wx.CB_READONLY)

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(lbl_drivers, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_drivers, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(1)

        return grid

    def _create_test_console(self):
        self._txt_console = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP |
                                        wx.TE_READONLY | wx.TE_RICH)
        self._txt_console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_NORMAL, False))
        return self._txt_console

    def _create_buttons(self):
        btn_test = wx.Button(self, IdManager.ID_INSTRUMENT_TEST, "Test")
        btn_save = wx.Button(self, IdManager.ID_INSTRUMENT_SAVE, "Save")
        btn_cancel = wx.Button(self, IdManager.ID_INSTRUMENT_CANCEL, "Cancel")
        btn_close = wx.Button(self, IdManager.ID_INSTRUMENT_CLOSE, "Close")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(btn_test, (0, 0), wx.DefaultSpan)
        grid.Add(btn_save, (0, 1), wx.DefaultSpan)
        grid.Add(btn_cancel, (0, 2), wx.DefaultSpan)
        grid.Add(btn_close, (0, 3), wx.DefaultSpan, wx.ALIGN_RIGHT)
        grid.AddGrowableCol(3)

        return grid

    ##########
    # Public #
    ##########

    def get_selected_instrument(self):
        index = self._lst_instruments.GetFirstSelected()
        if index >= 0:
            return self._lst_instruments.GetItemText(index)
        return ""

    def set_instruments(self, instruments):
        self._lst_instruments.DeleteAllItems()
        self._lst_instruments.id_map.clear()
        for instrument in sorted(instruments, key=lambda x: x["name"]):
            index = self._lst_instruments.InsertItem(self._lst_instruments.GetItemCount(),
                                                     instrument["name"])
            self._lst_instruments.id_map[index] = instrument["id"]

    def set_driver_names(self, driver_names):
        self._cmb_drivers.SetItems(driver_names)
        self.Layout()

    def show_driver_settings(self, settings):
        self._settings_controls.clear()
        self._settings_grid.Clear(True)
        if settings is None:
            self._settings_grid.Add(wx.Panel(self), (0, 0))
        else:
            try:
                for i, setting in enumerate(settings):
                    lbl = wx.StaticText(self, wx.ID_ANY, f"{setting.name}:")
                    ctrl_class = getattr(wx, setting.gui_control)
                    ctrl = ctrl_class(self, wx.ID_ANY, size=ViewSizes.TEXT_MEDIUM)
                    ctrl.SetValue(str(setting.default_value))
                    self._settings_grid.Add(lbl, (i, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                    self._settings_grid.Add(ctrl, (i, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                    self._settings_controls[setting.name] = (ctrl, setting.type)
            except:
                # Restore layout
                self._settings_grid.Add(wx.Panel(self), (0, 0))
                self.Layout()
                raise
        self.Layout()

    def show_instrument(self, instrument, driver_settings):
        self._txt_name.SetValue(instrument["name"])
        if instrument["driver_name"] in self._cmb_drivers.GetItems():
            self._cmb_drivers.SetValue(instrument["driver_name"])
        else:
            self._cmb_drivers.SetSelection(wx.NOT_FOUND)
        self.show_driver_settings(driver_settings)
        for key, value in instrument["settings"].items():
            if key in self._settings_controls:
                ctrl, _ctrl_type = self._settings_controls[key]
                ctrl.SetValue(str(value))

    def get_settings(self):
        settings = {
            "name": self._txt_name.GetValue().strip(),
            "driver_name": self._cmb_drivers.GetValue(),
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
    TestOptions.show_edit_instruments = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
