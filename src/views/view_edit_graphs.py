"""
View for the graphs.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as GuiSizes


class ViewEditGraphs(wx.Dialog):

    _TITLE = "Graphs"
    _WINDOW_SIZE = (800, 500)
    _COL_WIDTH = 180
    _COLOR_DEFAULT = "#000"
    _COLOR_ERROR = "#f60"

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.graphs_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_list(), 2, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_controls(), 5, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self):
        self._lst_graphs = wx.ListCtrl(self, IdManager.ID_GRAPH_LIST,
                                       style=wx.LC_SINGLE_SEL | wx.LC_REPORT |
                                       wx.LC_NO_SORT_HEADER)
        self._lst_graphs.InsertColumn(0, "Graphs:", width=self._COL_WIDTH)

        btn_new = wx.Button(self, IdManager.ID_GRAPH_NEW, "New")
        btn_down = wx.Button(self, IdManager.ID_GRAPH_DOWN, "Down")
        btn_up = wx.Button(self, IdManager.ID_GRAPH_UP, "Up")
        btn_delete = wx.Button(self, IdManager.ID_GRAPH_DELETE,"Delete")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(self._lst_graphs, (0, 0), (1, 2), wx.EXPAND)
        grid.Add(btn_down, (1, 0), wx.DefaultSpan)
        grid.Add(btn_up, (1, 1), wx.DefaultSpan)
        grid.Add(btn_new, (2, 0), wx.DefaultSpan)
        grid.Add(btn_delete, (2, 1), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, wx.ID_ANY)
        lbl_measurements = wx.StaticText(self, wx.ID_ANY, "Measurements:")
        self._lst_measurements = wx.CheckListBox(self, wx.ID_ANY)
        lbl_log_scale = wx.StaticText(self, wx.ID_ANY, "Y-axis log scale:")
        self._ckh_log_scale = wx.CheckBox(self, wx.ID_ANY,)
        lbl_y_scale = wx.StaticText(self, wx.ID_ANY,
                                    "Y-axis scale, leave empty for automatic scale:")
        lbl_y_min = wx.StaticText(self, wx.ID_ANY, "Y-axis min scale:")
        self._txt_y_min = wx.TextCtrl(self, wx.ID_ANY)
        lbl_y_max = wx.StaticText(self, wx.ID_ANY, "Y-axis max scale:")
        self._txt_y_max = wx.TextCtrl(self, wx.ID_ANY)
        btn_save = wx.Button(self, IdManager.ID_GRAPH_SAVE, "Save")
        btn_cancel = wx.Button(self, IdManager.ID_GRAPH_CANCEL, "Cancel")
        btn_close = wx.Button(self, IdManager.ID_GRAPH_CLOSE, "Close")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), (1, 4), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(lbl_measurements, (1, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(self._lst_measurements, (1, 1), wx.DefaultSpan, wx.ALIGN_TOP | wx.EXPAND)
        grid.Add(lbl_log_scale, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._ckh_log_scale, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_y_scale, (3, 0), (1, 4), wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_y_min, (4, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_y_min, (4, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_y_max, (5, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_y_max, (5, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(btn_save, (7, 2), wx.DefaultSpan)
        grid.Add(btn_cancel, (7, 3), wx.DefaultSpan)
        grid.Add(btn_close, (7, 4), wx.DefaultSpan)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(1)

        return grid

    ##########
    # Public #
    ##########

    def get_selected_index(self):
        return self._lst_graphs.GetFirstSelected()

    def set_measurements(self, measurements):
        items = [x["name"] for x in measurements]
        self._lst_measurements.Set(sorted(items))

    def set_graphs(self, graphs, selected_index):
        self._lst_graphs.DeleteAllItems()
        for graph in graphs:
            self._lst_graphs.InsertItem(self._lst_graphs.GetItemCount(), graph["name"])
        self._lst_graphs.Select(selected_index)

    def get_settings(self):
        y_min = self._txt_y_min.GetValue().strip()
        y_max = self._txt_y_max.GetValue().strip()
        return {
            "name": self._txt_name.GetValue().strip(),
            "measurements": list(self._lst_measurements.GetCheckedStrings()),
            "settings": {
                "log_scale": self._ckh_log_scale.GetValue(),
                "min_scale": None if y_min == "" else float(y_min),
                "max_scale": None if y_min == "" else float(y_max)
            }
        }

    def update_settings(self, settings):
        self._txt_name.SetValue(settings["name"])
        self._lst_measurements.SetCheckedStrings(settings["measurements"])
        self._ckh_log_scale.SetValue(settings["settings"].get("log_scale", False))
        self._txt_y_min.SetValue(str(settings["settings"].get("min_scale", "")))
        self._txt_y_max.SetValue(str(settings["settings"].get("max_scale", "")))


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.show_edit_graphs = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
