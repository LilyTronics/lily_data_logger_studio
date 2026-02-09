"""
Main view
"""

import wx.adv


class MainView(wx.MDIParentFrame):

    _MIN_WINDOW_SIZE = (900, 600)
    _ID_WINDOW_LEFT = wx.NewIdRef()
    _LEFT_WINDOW_MIN_WIDTH = 50
    _LEFT_WINDOW_WIDTH = 150
    _STATUS_SIZE = 170

    def __init__(self, title):
        super().__init__(None, title=title, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU)

        self._create_toolbar()
        self._create_layout()
        self._create_status_bar()

        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self._on_sash_drag)

        self.SetInitialSize(self._MIN_WINDOW_SIZE)


    ###########
    # Private #
    ###########

    def _create_toolbar(self):
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tb.Realize()

    def _create_layout(self):
        self.left_win =  wx.adv.SashLayoutWindow(self, self._ID_WINDOW_LEFT,
                                                 style=wx.NO_BORDER|wx.adv.SW_3D)
        self.left_win.SetDefaultSize((self._LEFT_WINDOW_WIDTH, -1))
        self.left_win.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self.left_win.SetAlignment(wx.adv.LAYOUT_LEFT)
        self.left_win.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._tree = wx.TreeCtrl(self.left_win, style=wx.TR_HIDE_ROOT)

    def _create_status_bar(self):
        sb = self.CreateStatusBar()
        sb.SetFieldsCount(5)
        sb.SetStatusWidths([self._STATUS_SIZE, self._STATUS_SIZE,
                            self._STATUS_SIZE, self._STATUS_SIZE,-1])
        sb.SetStatusText("Sample time: -", 0)
        sb.SetStatusText("End time: -", 1)
        sb.SetStatusText("Total samples: -", 2)
        sb.SetStatusText("Elapsed time: -", 3)
        sb.SetStatusText("Status: idle", 4)

    ##################
    # Event handlers #
    ##################

    def _on_size(self, _):
        # We need to check if the frame still exists, because this event
        # can be triggered during the destruction of the frame.
        if self:
            wx.adv.LayoutAlgorithm().LayoutMDIFrame(self)

    def _on_sash_drag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return

        if event.GetId() == self._ID_WINDOW_LEFT:
            new_width = max(event.GetDragRect().width, self._LEFT_WINDOW_MIN_WIDTH)
            self.left_win.SetDefaultSize((new_width, -1))

        wx.adv.LayoutAlgorithm().LayoutMDIFrame(self)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
