"""
View for the process.
"""

import wx


class ViewPanelProcess(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_process_list(), 1, wx.EXPAND)
        self.SetSizer(box)

    def _create_process_list(self):
        self._lst_steps = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_VRULES |
                                      wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self._lst_steps.InsertColumn(0, "#")
        self._lst_steps.InsertColumn(1, "Label")
        self._lst_steps.InsertColumn(3, "Step")
        self._lst_steps.InsertColumn(4, "Params")

        return self._lst_steps


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
