"""
View for the instruments.
"""

import wx

import src.models.images as Images
import src.views.view_sizes as ViewSizes


class ViewInstruments(wx.Dialog):

    _TITLE = "Instruments"
    _WINDOW_SIZE = (600, 400)

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.instruments_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(self), 1, wx.EXPAND | wx.ALL, ViewSizes.BOX_SPACING)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self, parent):
        self._lst_instruments = wx.ListCtrl(parent)

        grid = wx.GridBagSizer(ViewSizes.GRID_SPACING, ViewSizes.GRID_SPACING)
        grid.Add(self._lst_instruments, (0, 0), wx.DefaultSpan)
        return grid


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_instruments = True

    run_data_logger(TestOptions)
