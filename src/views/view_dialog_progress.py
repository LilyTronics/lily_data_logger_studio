"""
Progress dialog.
"""

import wx

import src.views.gui_sizes as GuiSizes


class ViewDialogProgress(wx.Dialog):

    def __init__(self, parent, title, maximum=100, frame_width=400):
        super().__init__(parent, wx.ID_ANY, title)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        self._lbl_message = wx.StaticText(self, wx.ID_ANY)
        self._gauge = wx.Gauge(self, wx.ID_ANY, maximum, style=wx.GA_HORIZONTAL)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._lbl_message, 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._gauge, 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        self.SetSizer(box)
        self.SetInitialSize((frame_width, 120))
        self.CenterOnParent()
        self.Show()
        wx.Yield()

    ##########
    # Public #
    ##########

    def _on_close(self, _):
        self.Destroy()

    def update(self, value, message):
        self._gauge.SetValue(value)
        self._lbl_message.SetLabel(message)
        wx.Yield()


if __name__ == "__main__":

    app = wx.App(redirect=False)

    dlg = ViewDialogProgress(None, "Test progress", 5)
    dlg.update(5, "Full")

    app.MainLoop()
