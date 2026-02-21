"""
View for the process.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images


class ViewProcess(wx.MDIChildFrame):

    _TITLE = "Process"
    _GAP = 5

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.process_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_process_list(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    def _create_process_list(self):
        self._lst_steps = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_VRULES |
                                      wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self._lst_steps.InsertColumn(0, "#")
        self._lst_steps.InsertColumn(1, "Label")
        self._lst_steps.InsertColumn(3, "Step")
        self._lst_steps.InsertColumn(4, "Params")

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(self._lst_steps, (0, 0), (1, 7), wx.EXPAND)

        grid.Add(wx.Button(self, IdManager.ID_PROCESS_ADD, "Add"), (1, 0))
        grid.Add(wx.Button(self, IdManager.ID_PROCESS_INSERT, "Insert"), (1, 1))
        grid.Add(wx.Button(self, IdManager.ID_PROCESS_INSERT, "Edit"), (1, 2))
        grid.Add(wx.Button(self, IdManager.ID_PROCESS_UP, "Up"), (1, 3))
        grid.Add(wx.Button(self, IdManager.ID_PROCESS_DOWN, "Down"), (1, 4))
        grid.Add(wx.Button(self, IdManager.ID_PROCESS_DOWN, "Delete"), (1, 6))

        grid.AddGrowableCol(6)
        grid.AddGrowableRow(0)
        return grid


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_process = True

    run_data_logger(TestOptions)
