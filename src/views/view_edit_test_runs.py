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
        self._lst_test_runs.InsertColumn(0, "Test runs", width=self._COL_WIDTH)
        self._lst_test_runs.EnableCheckBoxes(True)
        self._lst_test_runs.id_map = {}
        return self._lst_test_runs

    def _create_controls(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_general_controls(), 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_buttons(), 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        return box

    def _create_general_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        lbl_start = wx.StaticText(self, wx.ID_ANY, "Start time:")
        lbl_end = wx.StaticText(self, wx.ID_ANY, "End time:")
        lbl_duration = wx.StaticText(self, wx.ID_ANY, "Duration:")
        lbl_samples = wx.StaticText(self, wx.ID_ANY, "Number of samples:")
        lbl_measurements = wx.StaticText(self, wx.ID_ANY, "Measurements:")

        self._txt_name = wx.TextCtrl(self, size=GuiSizes.WIDTH_LARGE)
        self._lbl_start = wx.StaticText(self)
        self._lbl_end = wx.StaticText(self)
        self._lbl_duration = wx.StaticText(self)
        self._lbl_samples = wx.StaticText(self)
        self._lst_measurements = wx.ListBox(self, size=GuiSizes.WIDTH_LARGE)

        btn_update = wx.Button(self, IdManager.ID_TEST_RUNS_UPDATE, "Update")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(btn_update, (0, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_start, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_start, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_end, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_end, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_duration, (3, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_duration, (3, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_samples, (4, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_samples, (4, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_measurements, (5, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(self._lst_measurements, (5, 1), wx.DefaultSpan, wx.ALIGN_TOP | wx.EXPAND)
        grid.AddGrowableRow(5)

        return grid

    def _create_buttons(self):
        btn_delete = wx.Button(self, IdManager.ID_TEST_RUNS_DELETE, "Delete")
        btn_load = wx.Button(self, IdManager.ID_TEST_RUNS_LOAD, "Load")
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
        self._txt_name.SetValue("")
        self._lbl_start.SetLabel("")
        self._lbl_end.SetLabel("")
        self._lbl_duration.SetLabel("")
        self._lbl_samples.SetLabel("")
        self._lst_measurements.Clear()
        for test_run in test_runs:
            index = self._lst_test_runs.InsertItem(self._lst_test_runs.GetItemCount(),
                                                   test_run["name"])
            self._lst_test_runs.id_map[index] = test_run["id"]

    def show_test_run(self, test_run):
        timestamps = test_run["timestamps"]
        self._txt_name.SetValue(test_run["name"])
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
        index = next((k for k, v in self._lst_test_runs.id_map.items() if v == test_run["id"]), -1)
        if index >= 0:
            self._lst_test_runs.Select(index)
            self._lst_test_runs.EnsureVisible(2)

    def get_name(self):
        return self._txt_name.GetValue().strip()

    def get_selected_test_run(self):
        index = self._lst_test_runs.GetFirstSelected()
        if index >= 0:
            return self._lst_test_runs.id_map[index]
        return None

    def get_checked_test_runs(self):
        test_runs = [self._lst_test_runs.id_map[i]
                     for i in range(self._lst_test_runs.GetItemCount())
                     if self._lst_test_runs.IsItemChecked(i)]
        return test_runs


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.suppress_loading_drivers = True
    TestOptions.show_edit_test_runs = True

    run_data_logger(TestOptions)
