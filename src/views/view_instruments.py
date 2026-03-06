"""
View for the instruments.
"""

import wx

import src.models.images as Images
import src.views.view_sizes as ViewSizes


class ViewInstruments(wx.Dialog):

    _TITLE = "Instruments"
    _WINDOW_SIZE = (800, 500)

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.instruments_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(self), 2, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        box.Add(self._create_controls(self), 3, wx.EXPAND)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self, parent):
        self._lst_instruments = wx.ListCtrl(parent)
        btn_add = wx.Button(parent, wx.ID_ANY, "Add")
        btn_delete = wx.Button(parent, wx.ID_ANY,"Delete")

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(self._lst_instruments, (0, 0), (1, 2), wx.EXPAND)
        grid.Add(btn_add, (1, 0), wx.DefaultSpan)
        grid.Add(btn_delete, (1, 1), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self, parent):
        box = wx.BoxSizer(wx.VERTICAL)

        # General controls
        lbl_name = wx.StaticText(parent, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(parent, wx.ID_ANY)
        lbl_driver = wx.StaticText(parent, wx.ID_ANY, "Driver:")
        self._cmb_driver = wx.ComboBox(parent, wx.ID_ANY, style=wx.CB_READONLY)

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(lbl_driver, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_driver, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(1)

        box.Add(grid, 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)
        # Driver specific controls would go here
        box.Add(wx.Panel(parent), 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        # Buttons
        btn_test = wx.Button(parent, wx.ID_ANY, "Test")
        btn_apply = wx.Button(parent, wx.ID_ANY, "Apply")
        btn_cancel = wx.Button(parent, wx.ID_ANY, "Cancel")
        btn_close = wx.Button(parent, wx.ID_ANY, "Close")
        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(btn_test, (0, 0), wx.DefaultSpan)
        grid.Add(btn_apply, (0, 1), wx.DefaultSpan)
        grid.Add(btn_cancel, (0, 2), wx.DefaultSpan)
        grid.Add(btn_close, (0, 3), wx.DefaultSpan, wx.ALIGN_RIGHT)
        grid.AddGrowableCol(3)

        box.Add(grid, 0, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        return box


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True

    run_data_logger(TestOptions)
