"""
Panel that can displays multiple graphs.
Maximum of 12 graphs are supported.
"""

import wx

from src.views.view_plot_canvas import ViewPlotCanvas


class ViewPanelGraphs(wx.Panel):

    _SPACING = 2

    def __init__(self, parent):
        super().__init__(parent)
        self._graphs = []
        self._grid = wx.GridBagSizer(self._SPACING, self._SPACING)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._grid, 1, wx.EXPAND | wx.ALL, self._SPACING)
        self.SetSizer(box)

    ###########
    # Private #
    ###########

    def _show_graphs(self):
        for c in self._grid.GetChildren():
            self._grid.Detach(c.GetWindow())
        self._grid.Clear()

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

    ##########
    # Public #
    ##########

    def update(self, configuration):
        for g in self._graphs:
            g.Destroy()
        del self._graphs[:]
        graphs = configuration.get_graphs()
        for graph in graphs:
            labels = []
            for m in graph["measurements"]:
                meas = configuration.get_measurement(m)
                if meas is not None:
                    labels.append(f"{meas['name']} [{meas['unit']}]")
            self._graphs.append(ViewPlotCanvas(self, graph["name"], labels))
        self._show_graphs()


if __name__ == "__main__":

    import src.app_data as AppData

    from src.models.configuration import Configuration


    class TestFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="Test ViewPanelGraphs", size=(800, 600))
            panel = wx.Panel(self)

            self._config = Configuration()

            self.spin_count = wx.SpinCtrl(panel, value="0", min=0, max=12)
            self.graphs_view = ViewPanelGraphs(panel)
            btn_load = wx.Button(panel, wx.ID_ANY, "Load from config")

            grid = wx.GridBagSizer(5, 5)
            grid.Add(wx.StaticText(panel, label="Number of Graphs:"), (0, 0),
                                   flag=wx.ALIGN_CENTER_VERTICAL)
            grid.Add(self.spin_count, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
            grid.Add(btn_load, (0, 3), flag=wx.ALIGN_CENTER_VERTICAL)

            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(grid, 0, wx.EXPAND | wx.ALL, 5)
            box.Add(self.graphs_view, 1, wx.EXPAND | wx.ALL, 5)

            panel.SetSizer(box)

            self.spin_count.Bind(wx.EVT_SPINCTRL, self.on_spin)
            btn_load.Bind(wx.EVT_BUTTON, self.on_load)

        def on_spin(self, _event):
            graphs = self._config.get_graphs()
            diff = self.spin_count.GetValue() - len(graphs)
            if diff == 1:
                self._config.add_graph(f"Graph {len(graphs) + 1}", ["Voltage [V]"], {})
            elif diff == -1:
                self._config.delete_graph(len(graphs) - 1)
            self.graphs_view.update(self._config)

        def on_load(self, _event):
            config = Configuration()
            config.load(AppData.TEST_CONFIGURATION)
            self.graphs_view.update(config)
            self.spin_count.SetValue(len(config.get_graphs()))


    app = wx.App(False)
    frame = TestFrame()
    frame.Show()

    app.MainLoop()
