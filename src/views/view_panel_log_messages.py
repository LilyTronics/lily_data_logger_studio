"""
View for the log messages.
Auto refreshing text control.
"""

import wx

import src.app_data as AppData

from src.models.logger import Logger


class ViewPanelLogMessages(wx.Panel):

    _UPDATE_TIME = 250
    _COLOR_DEFAULT = "#000"
    _TEXT_COLORS = {
        Logger.TYPE_DEBUG: "#666",
        Logger.TYPE_ERROR: "#f60",
        Logger.TYPE_INFO: "#00f",
        Logger.TYPE_STDERR: "#f00",
        Logger.TYPE_STDOUT: "#999"
    }

    def __init__(self, parent, filename):
        super().__init__(parent, wx.ID_ANY)
        self._filename = filename

        self._console = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY |
                                    wx.TE_RICH)
        self._console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                                     wx.FONTWEIGHT_NORMAL, False))

        self._update_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_update_timer, self._update_timer)
        self._update_timer.Start(self._UPDATE_TIME)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._console, 1, wx.EXPAND)
        self.SetSizer(box)

        wx.CallAfter(self._show_messages)

    ###########
    # Private #
    ###########

    def _show_messages(self):
        with open(self._filename, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        n_lines = self._console.GetValue().count("\n")
        lines = lines[n_lines:]
        for line in lines:
            for key, value in self._TEXT_COLORS.items():
                if f" | {key:6} | " in line:
                    self._console.SetDefaultStyle(wx.TextAttr(value))
                    break
            else:
                self._console.SetDefaultStyle(wx.TextAttr(self._COLOR_DEFAULT))
            self._console.AppendText(line)

    ##################
    # Event handlers #
    ##################

    def _on_update_timer(self, event):
        self._show_messages()
        event.Skip()


if __name__ == "__main__":

    app = wx.App(redirect=False)
    f = wx.Frame(None, title="Log messages")
    f.SetInitialSize((800, 600))
    log = ViewPanelLogMessages(f, AppData.APP_LOG_FILE)
    f.Show()
    app.MainLoop()
