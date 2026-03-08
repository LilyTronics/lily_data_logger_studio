"""
View for the instruments.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.view_sizes as ViewSizes


class ViewInstruments(wx.Dialog):

    _TITLE = "Instruments"
    _WINDOW_SIZE = (800, 500)

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)
        self._settins_controls = {}

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.instruments_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(), 2, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_controls(), 3, wx.EXPAND)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self):
        self._lst_instruments = wx.ListCtrl(self)
        btn_add = wx.Button(self, IdManager.ID_INSTRUMENT_ADD, "Add")
        btn_delete = wx.Button(self, IdManager.ID_INSTRUMENT_DELETE,"Delete")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(self._lst_instruments, (0, 0), (1, 2), wx.EXPAND)
        grid.Add(btn_add, (1, 0), wx.DefaultSpan)
        grid.Add(btn_delete, (1, 1), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self):
        box = wx.BoxSizer(wx.VERTICAL)

        # General controls
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

        # Driver specific settings
        self._settings_grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        self._settings_grid.Add(wx.Panel(self), (0, 0))
        box.Add(grid, 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._settings_grid, 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        # Buttons
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

        box.Add(grid, 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        return box

    ##########
    # Public #
    ##########

    def set_driver_names(self, driver_names):
        self._cmb_drivers.SetItems(driver_names)

    def show_driver_settings(self, settings):
        self._settins_controls.clear()
        self._settings_grid.Clear(True)
        try:
            for i, setting in enumerate(settings):
                lbl = wx.StaticText(self, wx.ID_ANY, setting.name)
                ctrl_class = getattr(wx, setting.gui_control)
                ctrl = ctrl_class(self, wx.ID_ANY, size=ViewSizes.TEXT_MEDIUM)
                ctrl.SetValue(str(setting.default_value))
                self._settings_grid.Add(lbl, (i, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                self._settings_grid.Add(ctrl, (i, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        except:
            # Restore layout
            self._settings_grid.Add(wx.Panel(self), (0, 0))
            raise

        self.Layout()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
