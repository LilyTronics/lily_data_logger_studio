"""
Plot view.
"""

import wx.lib.plot


class ViewPlotCanvas(wx.lib.plot.PlotCanvas):

    _LINE_COLORS =[
        "#0000cc",
        "#00cc00",
        "#cc0000",
        "#cccc00",
        "#00cccc",
        "#cc00cc"
    ]

    def __init__(self, parent, title, labels):
        self.title = title
        self.labels = labels
        super().__init__(parent)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Names from WX python are not conform the Pyhton standard
        # pylint: disable=invalid-name
        self.fontSizeLegend = 8
        self.fontSizeAxis = 8
        self.fontSizeTitle = 10
        self.enableLegend = True
        self.enableTicks = (True, True, False, False)
        self.enableAntiAliasing = True
        self.enableYAxisLabel = False
        self.enableXAxisLabel = True
        self.xSpec = "auto"
        self.ySpec = "auto"
        # pylint: enable=invalid-name

        lines = []
        for index, label in enumerate(self.labels):
            lines.append(wx.lib.plot.PolyLine(
                [],
                legend=label,
                colour=wx.Colour(self._LINE_COLORS[index % len(self._LINE_COLORS)]),
                width=2
            ))
        gc = wx.lib.plot.PlotGraphics(lines, title, "Time [s]")
        self.Draw(gc, xAxis=(0, 1), yAxis=(0, 1))

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
        self.Draw(wx.lib.plot.PlotGraphics(lines, self.title, x_label))


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
    frame = wx.Frame(None, title="Test ViewPlot", size=(800, 600))
    plot_view = ViewPlotCanvas(frame, "Sample Plot", names)
    frame.Show()
    wx.CallAfter(plot_view.draw_lines, test_data, "Time [s]")
    app.MainLoop()
