"""
Panel that can displays multiple graphs.
Maximum of 12 graphs are supported.
"""

import wx

from src.views.view_plot import ViewPlot


class ViewGraphsPanel(wx.Panel):

    _SPACING = 2

    def __init__(self, parent):
        super().__init__(parent)
        self._graphs = []
        self._grid = wx.GridBagSizer(self._SPACING, self._SPACING)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._grid, 1, wx.EXPAND | wx.ALL, self._SPACING)
        self.SetSizer(box)

    def _show_graphs(self):
        # Clear grid, remove children and clear sizer
        for c in self._grid.GetChildren():
            self._grid.Detach(c.GetWindow())
        self._grid.Clear(True)

        col = 0
        row = 0
        n_graphs = len(self._graphs)
        max_cols = 3 if n_graphs >= 7 else 2
        for graph in self._graphs:
            self._grid.Add(graph, (row, col), flag=wx.EXPAND)
            if n_graphs < 4:
                row += 1
            else:
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        # Make all rows and columns growable
        for i in range(self._grid.GetCols()):
            if not self._grid.IsColGrowable(i):
                self._grid.AddGrowableCol(i)
        for i in range(self._grid.GetRows()):
            if not self._grid.IsRowGrowable(i):
                self._grid.AddGrowableRow(i)

        self.Layout()

    def add_graph(self, graph_name):
        self._graphs.append(ViewPlot(self, graph_name))
        self._show_graphs()

    def remove_graph(self, graph_name):
        for graph in self._graphs:
            if graph.title == graph_name:
                self._graphs.remove(graph)
                graph.Destroy()
                break
        self._show_graphs()


if __name__ == "__main__":

    class TestFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="Test ViewGraphs", size=(800, 600))
            panel = wx.Panel(self)

            self._n_graphs = 0
            self.spinCount = wx.SpinCtrl(panel, value="0", min=0, max=12)
            self.graphs_view = ViewGraphsPanel(panel)

            grid = wx.GridBagSizer(5, 5)
            grid.Add(wx.StaticText(panel, label="Number of Graphs:"), (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            grid.Add(self.spinCount, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)

            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(grid, 0, wx.EXPAND | wx.ALL, 5)
            box.Add(self.graphs_view, 1, wx.EXPAND | wx.ALL, 5)

            panel.SetSizer(box)

            self.spinCount.Bind(wx.EVT_SPINCTRL, self.on_spin)

        def on_spin(self, event):
            diff = self.spinCount.GetValue() - self._n_graphs
            if diff > 0:
                for i in range(diff):
                    self.graphs_view.add_graph(f"Graph {self._n_graphs + 1 + i}")
            elif diff < 0:
                for i in range(-diff):
                    self.graphs_view.remove_graph(f"Graph {self._n_graphs}")
            self._n_graphs = self.spinCount.GetValue()


    app = wx.App(False)
    frame = TestFrame()
    frame.Show()

    app.MainLoop()
