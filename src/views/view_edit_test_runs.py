"""
View for the test runs.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as GuiSizes

from src.models.time_converter import TimeConverter


class ViewEditTestRuns(wx.Dialog):

    _TITLE = "Test runs"
    _WINDOW_SIZE = (700, 500)
    _COL_WIDTH = 180
    _MEASUREMENTS_WIDTH = 200

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.database_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(), 2, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_controls(), 5, wx.EXPAND)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self):
        self._lst_test_runs = wx.ListCtrl(self, IdManager.ID_TEST_RUNS_LIST,
                                          style=wx.LC_SINGLE_SEL | wx.LC_REPORT |
                                          wx.LC_NO_SORT_HEADER)
        self._lst_test_runs.InsertColumn(0, "Test runs:", width=self._COL_WIDTH)
        self._lst_test_runs.id_map = {}
        return self._lst_test_runs

    def _create_controls(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_general_controls(), 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_buttons(), 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        return box

    def _create_general_controls(self):
        lbl_start = wx.StaticText(self, wx.ID_ANY, "Start time:")
        lbl_end = wx.StaticText(self, wx.ID_ANY, "End time:")
        lbl_duration = wx.StaticText(self, wx.ID_ANY, "Duration:")
        lbl_samples = wx.StaticText(self, wx.ID_ANY, "Number of samples:")
        lbl_measurements = wx.StaticText(self, wx.ID_ANY, "Measurements:")

        self._lbl_start = wx.StaticText(self)
        self._lbl_end = wx.StaticText(self)
        self._lbl_duration = wx.StaticText(self)
        self._lbl_samples = wx.StaticText(self)
        self._lst_measurements = wx.ListBox(self, size=(self._MEASUREMENTS_WIDTH, -1))

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_start, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_start, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_end, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_end, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_duration, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_duration, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_samples, (3, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_samples, (3, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_measurements, (4, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(self._lst_measurements, (4, 1), wx.DefaultSpan, wx.ALIGN_TOP | wx.EXPAND)
        grid.AddGrowableRow(4)

        return grid

    def _create_buttons(self):
        btn_delete = wx.Button(self, IdManager.ID_TEST_RUNS_DELETE, "Delete")
        btn_load = wx.Button(self, IdManager.ID_TEST_RUNS_DELETE, "Load")
        btn_export = wx.Button(self, IdManager.ID_TEST_RUNS_EXPORT, "Export")
        btn_import = wx.Button(self, IdManager.ID_TEST_RUNS_IMPORT, "Import")
        btn_close = wx.Button(self, IdManager.ID_TEST_RUNS_CLOSE, "Close")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(btn_delete, (0, 0), wx.DefaultSpan)
        grid.Add(btn_load, (0, 1), wx.DefaultSpan)
        grid.Add(btn_export, (0, 2), wx.DefaultSpan)
        grid.Add(btn_import, (0, 3), wx.DefaultSpan)
        grid.Add(btn_close, (0, 4), wx.DefaultSpan, wx.ALIGN_RIGHT)
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(4)

        return grid

    ##########
    # Public #
    ##########

    def update_test_runs(self, test_runs):
        self._lst_test_runs.DeleteAllItems()
        self._lst_test_runs.id_map.clear()
        self._lbl_start.SetLabel("")
        self._lbl_end.SetLabel("")
        self._lbl_duration.SetLabel("")
        self._lbl_samples.SetLabel("")
        self._lst_measurements.Clear()
        for test_run in test_runs:
            timestamps = test_run["timestamps"]
            if len(timestamps) > 0:
                timestamp = TimeConverter.get_time_string(timestamps[0])
                index = self._lst_test_runs.InsertItem(self._lst_test_runs.GetItemCount(),
                                                       timestamp)
                self._lst_test_runs.id_map[index] = test_run["id"]

    def show_test_run(self, test_run):
        timestamps = test_run["timestamps"]
        self._lbl_start.SetLabel(TimeConverter.get_time_string(timestamps[0]))
        self._lbl_end.SetLabel(TimeConverter.get_time_string(timestamps[-1]))
        self._lbl_duration.SetLabel(
            TimeConverter.create_duration_time_string(timestamps[-1] - timestamps[0])
        )
        self._lbl_samples.SetLabel(str(len(timestamps)))
        self._lst_measurements.Clear()
        for measurement in test_run["measurements"]:
            self._lst_measurements.Append(
                f"{measurement["name"]} [{measurement["unit"]}] "
                f"({len(measurement["values"])} values)"
            )


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
