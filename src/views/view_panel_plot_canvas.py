"""
Plot view.
"""

import wx.lib.plot


class ViewPanelPlotCanvas(wx.Panel):

    _LINE_COLORS =[
        "#0000cc",
        "#00cc00",
        "#cc0000",
        "#cccc00",
        "#00cccc",
        "#cc00cc"
    ]
    _SPACING = 5


    def __init__(self, parent, title, labels):
        self.title = title
        self.labels = labels
        super().__init__(parent)

        self._plot = wx.lib.plot.PlotCanvas(self)
        self._plot.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        )
        self._plot.fontSizeLegend = 8
        self._plot.fontSizeAxis = 8
        self._plot.fontSizeTitle = 10
        self._plot.enableLegend = True
        self._plot.enableTicks = (True, True, False, False)
        self._plot.enableAntiAliasing = True
        self._plot.enableYAxisLabel = False
        self._plot.enableXAxisLabel = True
        self._plot.xSpec = "auto"
        self._plot.ySpec = "auto"

        lines = []
        for index, label in enumerate(self.labels):
            lines.append(wx.lib.plot.PolyLine(
                [],
                legend=label,
                colour=wx.Colour(self._LINE_COLORS[index % len(self._LINE_COLORS)]),
                width=2
            ))
        gc = wx.lib.plot.PlotGraphics(lines, title, "Time [s]")
        self._plot.Draw(gc, xAxis=(0, 1), yAxis=(0, 1))

        self.SetBackgroundColour(self._plot.GetBackgroundColour())

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._plot, 1, wx.EXPAND | wx.ALL, self._SPACING)
        self.SetSizer(box)

    ##########
    # Public #
    ##########

    def draw_lines(self, graph_data, x_label):
        lines = []
        for index, graph in enumerate(graph_data):
            lines.append(wx.lib.plot.PolyLine(
                graph["data"],
                legend=graph["legend"],
                colour=wx.Colour(self._LINE_COLORS[index % len(self._LINE_COLORS)]),
                width=2
            ))
        self._plot.Draw(wx.lib.plot.PlotGraphics(lines, self.title, x_label))


if __name__ == "__main__":

    import random

    names = []
    test_data = []
    for i in range(8):
        line_data = {}
        names.append(f"Label {i + 1}")
        line_data["legend"] = names[-1]
        line_data["data"] = [(x, y) for x in range(50) for y in random.sample(range(10), 1)]
        test_data.append(line_data)
    app = wx.App(False)
    frame = wx.Frame(None, title="Test ViewPanelPlotCanvas", size=(800, 600))
    plot_view = ViewPanelPlotCanvas(frame, "Sample Plot", names)
    frame.Show()
    wx.CallAfter(plot_view.draw_lines, test_data, "Time [s]")
    app.MainLoop()
