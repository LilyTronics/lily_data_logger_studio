"""
View for the log messages.
Auto refreshing text control.
"""

import wx

import src.app_data as AppData

from src.models.logger import Logger


class ViewLogMessages(wx.TextCtrl):

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
        super().__init__(parent, style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY |
                         wx.TE_RICH)

        self.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_NORMAL, False))

        self._update_timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self._on_update_timer, self._update_timer)

        self._update_timer.Start(self._UPDATE_TIME)

    ###########
    # Private #
    ###########

    def _on_update_timer(self, event):
        with open(AppData.APP_LOG_FILE, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        content = self.GetValue()
        for line in filter(lambda x: x not in content, lines):
            for key, value in self._TEXT_COLORS.items():
                if f" | {key:6} | " in line:
                    self.SetDefaultStyle(wx.TextAttr(value))
                    break
            else:
                self.SetDefaultStyle(wx.TextAttr(self._COLOR_DEFAULT))

            self.AppendText(line)

        event.Skip()


if __name__ == "__main__":

    app = wx.App(redirect=False)
    f = wx.Frame(None, title="Log messages")
    f.SetInitialSize((800, 600))
    log = ViewLogMessages(f)
    f.Show()
    app.MainLoop()
