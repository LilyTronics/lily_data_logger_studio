"""
View for the graph.
"""

import wx

import src.models.id_manager as IdManager

from src.views.view_graphs_panel import ViewGraphsPanel


class ViewGraph(wx.MDIChildFrame):

    _TITLE = "Graph"
    _GAP = 5

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_graph_panel(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    def _create_graph_panel(self):
        self._graphs_view = ViewGraphsPanel(self)

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(self._graphs_view, (0, 0), (1, 7), wx.EXPAND)

        grid.Add(wx.Button(self, IdManager.ID_GRAPH_ADD, "Add"), (1, 0))
        grid.Add(wx.Button(self, IdManager.ID_GRAPH_INSERT, "Insert"), (1, 1))
        grid.Add(wx.Button(self, IdManager.ID_GRAPH_EDIT, "Edit"), (1, 2))
        grid.Add(wx.Button(self, IdManager.ID_GRAPH_UP, "Up"), (1, 3))
        grid.Add(wx.Button(self, IdManager.ID_GRAPH_DOWN, "Down"), (1, 4))
        grid.Add(wx.Button(self, IdManager.ID_GRAPH_DELETE, "Delete"), (1, 6))

        grid.AddGrowableCol(6)
        grid.AddGrowableRow(0)
        return grid


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_graph = True

    run_data_logger(TestOptions)
