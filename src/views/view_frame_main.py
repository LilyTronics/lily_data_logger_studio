"""
Main view
"""

import wx.adv

from wx.lib.agw import aui

import src.models.id_manager as IdManager
import src.models.images as Images

from src.models.time_converter import TimeConverter
from src.views.view_panel_configuration import ViewPanelConfiguration
from src.views.view_panel_data_table import ViewPanelDataTable
from src.views.view_panel_graphs import ViewPanelGraphs
from src.views.view_panel_log_messages import ViewPanelLogMessages
from src.views.view_panel_process import ViewPanelProcess


class ViewFrameMain(wx.Frame):

    # Minimum screen resolution: 1366×768 / 1280x720 (still used on older laptops, anno 2026)
    _MIN_WINDOW_SIZE = (1200, 700)
    _ID_WINDOW_BOT = wx.NewIdRef()
    _ID_WINDOW_LEFT = wx.NewIdRef()
    _DEFAULT_TREE_WIDTH = 250
    _DEFAULT_LOG_HEIGHT = 80
    _AUI_MANAGER_FLAGS = (aui.AUI_MGR_ALLOW_FLOATING | aui.AUI_MGR_LIVE_RESIZE |
                          aui.AUI_MGR_USE_NATIVE_MINIFRAMES)
    _DOCK_MIN_SIZE = (200, 100)
    _DEFAULT_GRAPH_SIZE = (600, 400)
    _DEFAULT_TABLE_SIZE = (300, 200)
    _DEFAULT_PROCESS_SIZE = (500, 200)
    _STATUS_SIZE = 170
    _SB_SAMPLE_TIME = 1
    _SB_END_TIME = 2
    _SB_TOTAL_SAMPLES = 3
    _SB_ELAPSED_TIME = 4
    _SB_NR_OF_SAMPLES = 5
    _SB_STATUS = 6
    _LED_SIZE = (16, 16)
    _COLOR_LED_OFF = "#060"
    _COLOR_LED_ON = "#0f0"
    _BLINK_SPEED = 500

    def __init__(self, title, allow_docking):
        self._title = title
        super().__init__(None, title=title, style=wx.DEFAULT_FRAME_STYLE)
        self._allow_docking = allow_docking
        self._default_layout = ""

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.graphs_24.GetBitmap())
        self.SetIcon(icon)

        self._create_toolbar()
        self._create_status_bar()
        self._create_layout()
        self._create_panes()

        self._blink_timer = wx.Timer(self)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self._on_sash_drag)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_TIMER, self._on_blink_timer, self._blink_timer)
        self.Bind(wx.EVT_TOOL, self._on_restore_layout, id=IdManager.ID_RESTORE_LAYOUT)

        self.SetInitialSize(self._MIN_WINDOW_SIZE)

        # Must be called after to make the sizes work
        wx.CallAfter(self._update_layout)

    ###########
    # Private #
    ###########

    def _create_toolbar(self):
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tb.AddTool(IdManager.ID_NEW_CONFIG, "", Images.new_24.GetBitmap(),
                   "New configuration")
        tb.AddTool(IdManager.ID_OPEN_CONFIG, "", Images.open_24.GetBitmap(),
                   "Open configuration")
        tb.AddTool(IdManager.ID_SAVE_CONFIG, "", Images.save_24.GetBitmap(),
                   "Save configuration")
        tb.AddSeparator()
        tb.AddTool(IdManager.ID_RELOAD_DRIVERS, "", Images.refresh_24.GetBitmap(),
                   "Reload drivers")
        tb.AddSeparator()
        tb.AddTool(IdManager.ID_SHOW_EDIT_SETTINGS, "", Images.settings_24.GetBitmap(),
                   "Edit settings")
        tb.AddTool(IdManager.ID_SHOW_EDIT_INSTRUMENTS, "", Images.instruments_24.GetBitmap(),
                   "Edit instruments")
        tb.AddTool(IdManager.ID_SHOW_EDIT_MEASUREMENTS, "", Images.data_table_24.GetBitmap(),
                   "Edit measurements")
        tb.AddTool(IdManager.ID_SHOW_EDIT_PROCESS, "", Images.process_24.GetBitmap(),
                   "Edit process")
        tb.AddTool(IdManager.ID_SHOW_EDIT_GRAPHS, "", Images.graphs_24.GetBitmap(),
                   "Edit graphs")
        tb.AddSeparator()
        tb.AddTool(IdManager.ID_START_LOGGER, "", Images.start_24.GetBitmap(),
                   "Start data logger")
        tb.AddTool(IdManager.ID_STOP_LOGGER, "", Images.stop_24.GetBitmap(),
                   "Stop data logger")
        tb.AddSeparator()
        tb.AddTool(IdManager.ID_RESTORE_LAYOUT, "", Images.restore_layout_24.GetBitmap(),
                   "Restore layout")
        tb.Realize()

    def _create_status_bar(self):
        self._sb = self.CreateStatusBar()
        self._sb.SetFieldsCount(7)
        # First text field is for the long help text of the toolbar
        # We don't use it so we make a small empty space
        self._sb.SetStatusWidths([0, self._STATUS_SIZE, self._STATUS_SIZE,
                                  self._STATUS_SIZE, self._STATUS_SIZE,
                                  self._STATUS_SIZE, -1])

        self._sb.SetStatusText("Sample time: -", self._SB_SAMPLE_TIME)
        self._sb.SetStatusText("End time: -", self._SB_END_TIME)
        self._sb.SetStatusText("Total samples: -", self._SB_TOTAL_SAMPLES)
        self._sb.SetStatusText("Elapsed time: -", self._SB_ELAPSED_TIME)
        self._sb.SetStatusText("Number of samples: 0", self._SB_NR_OF_SAMPLES)
        self._sb.SetStatusText("Status: idle", self._SB_STATUS)

        # This will positioned correct using the on size event
        self._activity_led = wx.Panel(self._sb, wx.ID_ANY, size=self._LED_SIZE,
                                      style=wx.BORDER_SIMPLE)
        self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)

    def _create_layout(self):
        self._bot_win = wx.adv.SashLayoutWindow(self, self._ID_WINDOW_BOT,
                                                style=wx.NO_BORDER|wx.adv.SW_3D)
        self._bot_win.SetDefaultSize((-1, self._DEFAULT_LOG_HEIGHT))
        self._bot_win.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self._bot_win.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        self._bot_win.SetSashVisible(wx.adv.SASH_TOP, True)
        ViewPanelLogMessages(self._bot_win)

        self._left_win =  wx.adv.SashLayoutWindow(self, self._ID_WINDOW_LEFT,
                                                 style=wx.NO_BORDER|wx.adv.SW_3D)
        self._left_win.SetDefaultSize((self._DEFAULT_TREE_WIDTH, -1))
        self._left_win.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._left_win.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._left_win.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._configuration_panel = ViewPanelConfiguration(self._left_win)

        self._main_win = wx.Panel(self, wx.ID_ANY)

    def _create_panes(self):
        self._graphs_panel = ViewPanelGraphs(self._main_win)
        self._process_panel = ViewPanelProcess(self._main_win)
        self._data_table_panel = ViewPanelDataTable(self._main_win)

        panels = [
            {
                "panel": self._graphs_panel,
                "name": "graphs",
                "caption": "Graphs",
                "size": self._DEFAULT_GRAPH_SIZE,
                "dock": "centerpane"
            },
            {
                "panel": self._process_panel,
                "name": "process",
                "caption": "Process",
                "size": self._DEFAULT_PROCESS_SIZE,
                "dock": aui.AUI_DOCK_BOTTOM
            },
            {
                "panel": self._data_table_panel,
                "name": "data_table",
                "caption": "Measurements",
                "size": self._DEFAULT_TABLE_SIZE,
                "dock": aui.AUI_DOCK_BOTTOM
            }
        ]

        flags = self._AUI_MANAGER_FLAGS
        if not self._allow_docking:
            flags &= ~aui.AUI_MGR_ALLOW_FLOATING
            flags &= ~aui.AUI_MGR_ALLOW_ACTIVE_PANE
        self._aui_manager = aui.AuiManager()
        self._aui_manager.SetManagedWindow(self._main_win)
        self._aui_manager.SetAGWFlags(flags)
        art = self._aui_manager.GetArtProvider()
        art.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, aui.AUI_GRADIENT_NONE)

        for panel in panels:
            pane_info = (
                aui.AuiPaneInfo()
                .Name(panel["name"])
                .Caption(panel["caption"])
                .CloseButton(False)
                .MaximizeButton(True)
                .Dockable(self._allow_docking)
                .Floatable(self._allow_docking)
                .Movable(self._allow_docking)
            )
            if panel["dock"] == "centerpane":
                pane_info = pane_info.CenterPane()
            else:
                pane_info = pane_info.Direction(panel["dock"])
            # Must be last.
            pane_info = (
                pane_info.CaptionVisible(True)
                .MinSize(self._DOCK_MIN_SIZE)
                .BestSize(panel["size"])
            )
            self._aui_manager.AddPane(panel["panel"], pane_info)

    def _update_layout(self):
        self._aui_manager.Update()
        # Store default layout for the resore layout button
        self._default_layout = self._aui_manager.SavePerspective()

    ##################
    # Event handlers #
    ##################

    def _on_sash_drag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return

        if event.GetId() == self._ID_WINDOW_LEFT:
            new_width = max(event.GetDragRect().width, self._DEFAULT_TREE_WIDTH)
            self._left_win.SetDefaultSize((new_width, -1))

        if event.GetId() == self._ID_WINDOW_BOT:
            new_height = max(event.GetDragRect().height, self._DEFAULT_LOG_HEIGHT)
            self._bot_win.SetDefaultSize((-1, new_height))

        wx.adv.LayoutAlgorithm().LayoutFrame(self, self._main_win)

    def _on_size(self, _):
        # We need to check if the frame still exists, because this event
        # can be triggered during the destruction of the frame.
        if self:
            wx.adv.LayoutAlgorithm().LayoutFrame(self, self._main_win)
            # Place the LED in the correct position
            rect = self._sb.GetFieldRect(self._SB_STATUS)
            rect.x += 100
            rect.y += 2
            self._activity_led.SetPosition((rect.x, rect.y))

    def _on_blink_timer(self, event):
        if self._activity_led.GetBackgroundColour() == self._COLOR_LED_ON:
            self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)
        else:
            self._activity_led.SetBackgroundColour(self._COLOR_LED_ON)
        self._activity_led.Refresh()
        event.Skip()

    def _on_restore_layout(self, event):
        self._aui_manager.LoadPerspective(self._default_layout)
        event.Skip()

    ##########
    # Public #
    ##########
    def get_tree_width(self):
        return self._left_win.GetSize()[0]

    def set_tree_width(self, width):
        if width > self._DEFAULT_TREE_WIDTH:
            self._left_win.SetDefaultSize((width, -1))

    def get_log_height(self):
        return self._bot_win.GetSize()[1]

    def set_log_height(self, height):
        if height > self._DEFAULT_LOG_HEIGHT:
            self._bot_win.SetDefaultSize((-1, height))

    def update_configuration(self, configuration):
        self._configuration_panel.update_tree(configuration)

        settings = configuration.get_settings()
        sample_time = settings["sample_time"]
        end_time = "-"
        total_samples = "-"
        if not settings["continuous_mode"]:
            end_time = settings["end_time"]
            total_samples = int(end_time / sample_time) + 1
            end_time = TimeConverter.create_duration_time_string(end_time)
        sample_time = TimeConverter.create_duration_time_string(sample_time)
        self._sb.SetStatusText(f"Sample time: {sample_time}", self._SB_SAMPLE_TIME)
        self._sb.SetStatusText(f"End time: {end_time}", self._SB_END_TIME)
        self._sb.SetStatusText(f"Total samples: {total_samples}", self._SB_TOTAL_SAMPLES)

        title = f"{self._title} - {configuration.get_filename()}"
        title += "*" if configuration.is_changed() else ""
        self.SetTitle(title)

    def update_status(self, status):
        self._sb.SetStatusText(f"Status: {status}", self._SB_STATUS)
        if status == "running":
            self._activity_led.SetBackgroundColour(self._COLOR_LED_ON)
            self._blink_timer.Start(self._BLINK_SPEED)
        else:
            self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)
            self._blink_timer.Stop()
        self._activity_led.Refresh()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
