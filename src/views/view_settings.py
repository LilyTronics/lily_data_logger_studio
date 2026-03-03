"""
View for the settings.
"""

import wx.grid

import src.models.images as Images


class ViewSettings(wx.MDIChildFrame):

    _TITLE = "Settings"
    _GAP = 5

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.settings_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_controls(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    def _create_controls(self):
        grid = wx.GridBagSizer(self._GAP, self._GAP)
        return grid


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_settings = True

    run_data_logger(TestOptions)
