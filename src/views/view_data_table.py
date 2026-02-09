"""
View for the data table.
"""

import wx.grid

import src.models.images as Images


class ViewDataTable(wx.MDIChildFrame):

    def __init__(self, parent):
        super().__init__(parent)


        # bmp = wx.Bitmap("myicon.png")
        icon = wx.Icon()
        icon.CopyFromBitmap(Images.data_table_24.GetBitmap())
        self.SetIcon(icon)


        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_data_table(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    def _create_data_table(self):
        self._data_table = wx.grid.Grid(self, wx.ID_ANY)
        self._data_table.CreateGrid(0, 1)
        self._data_table.SetColLabelValue(0, "Time")
        self._data_table.EnableEditing(False)
        self._data_table.EnableDragRowSize(False)
        self._data_table.EnableDragColMove(False)
        self._data_table.EnableDragColSize(False)
        return self._data_table


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_data_table = True

    run_data_logger(TestOptions)
