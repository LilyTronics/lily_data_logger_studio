"""
View for the data table.
"""

import wx

import src.app_data as AppData
import src.models.images as Images

from src.models.logger import Logger


class ViewLogMessages(wx.MDIChildFrame):

    _UPDATE_TIME = 250
    _COLOR_DEFAULT = "#000"
    _TEXT_COLORS = {
        Logger.TYPE_DEBUG: "#666",
        Logger.TYPE_ERROR: "#f60",
        Logger.TYPE_INFO: "#00f",
        Logger.TYPE_STDERR: "#f00",
        Logger.TYPE_STDOUT: "#999"
    }

    def __init__(self, parent):
        super().__init__(parent)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.log_messages_24.GetBitmap())
        self.SetIcon(icon)

        self._txt_console = wx.TextCtrl(self, wx.ID_ANY,
                                        style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY |
                                              wx.TE_RICH)
        self._txt_console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_NORMAL, False))

        self._update_timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self._on_update_timer, self._update_timer)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        self._update_timer.Start(self._UPDATE_TIME)

    ###########
    # Private #
    ###########

    def _on_update_timer(self, event):
        with open(AppData.APP_LOG_FILE, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        content = self._txt_console.GetValue()
        for line in filter(lambda x: x not in content, lines):
            for key, value in self._TEXT_COLORS.items():
                if f" | {key:6} | " in line:
                    self._txt_console.SetDefaultStyle(wx.TextAttr(value))
                    break
            else:
                self._txt_console.SetDefaultStyle(wx.TextAttr(self._COLOR_DEFAULT))

            self._txt_console.AppendText(line)

        event.Skip()

    def _on_close(self, event):
        self._update_timer.Stop()
        self._update_timer.Destroy()
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_log_messages = True

    run_data_logger(TestOptions)
