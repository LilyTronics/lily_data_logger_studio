"""
Main view
"""

import wx.adv

import src.models.id_manager as IdManager
import src.models.images as Images


class MainView(wx.MDIParentFrame):

    _MIN_WINDOW_SIZE = (900, 600)
    _ID_WINDOW_LEFT = wx.NewIdRef()
    _LEFT_WINDOW_MIN_WIDTH = 50
    _LEFT_WINDOW_WIDTH = 150
    _STATUS_SIZE = 170

    def __init__(self, title):
        super().__init__(None, title=title, style=wx.DEFAULT_FRAME_STYLE)

        self._create_menu()
        self._create_toolbar()
        self._create_layout()
        self._create_status_bar()

        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self._on_sash_drag)

        self.SetInitialSize(self._MIN_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_menu(self):
        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)

    def _create_toolbar(self):
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tb.AddTool(IdManager.ID_SHOW_LOG, "", Images.log_messages_24.GetBitmap(),
                   "Show log messages")
        tb.Realize()

    def _create_layout(self):
        self._left_win =  wx.adv.SashLayoutWindow(self, self._ID_WINDOW_LEFT,
                                                 style=wx.NO_BORDER|wx.adv.SW_3D)
        self._left_win.SetDefaultSize((self._LEFT_WINDOW_WIDTH, -1))
        self._left_win.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._left_win.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._left_win.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._tree = wx.TreeCtrl(self._left_win, style=wx.TR_HIDE_ROOT)

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
            self._left_win.SetDefaultSize((new_width, -1))

        wx.adv.LayoutAlgorithm().LayoutMDIFrame(self)

    ##########
    # Public #
    ##########

    def get_tree_width(self):
        return self._left_win.GetSize()[0]

    def set_tree_width(self, width):
        if width > self._LEFT_WINDOW_MIN_WIDTH:
            self._left_win.SetDefaultSize((width, -1))


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
