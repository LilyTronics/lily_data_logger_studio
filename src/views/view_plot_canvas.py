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

    def __init__(self, parent, title, labels, init_data=[]):
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
        self.xSpec = "auto"
        self.ySpec = "auto"
        # pylint: enable=invalid-name

        lines = []
        for i, label in enumerate(self.labels):
            lines.append(wx.lib.plot.PolyLine(
                init_data[i] if i < len(init_data) else [],
                legend=label,
                colour=wx.Colour(self._LINE_COLORS[i % len(self._LINE_COLORS)]),
                width=2
            ))
        gc = wx.lib.plot.PlotGraphics(lines, title)
        x_axis = None if len(init_data) > 0 else (0, 1)
        y_axis = None if len(init_data) > 0 else (0, 1)
        self.Draw(gc, xAxis=x_axis, yAxis=y_axis)


if __name__ == "__main__":

    import random

    labels = []
    init_data = []
    for i in range(8):
        labels.append(f"Label {i + 1}")
        init_data.append(
            [(x, y) for x in range(50) for y in random.sample(range(10), 1)]
        )
    app = wx.App(False)
    frame = wx.Frame(None, title="Test ViewPlot", size=(800, 600))
    plot_view = ViewPlotCanvas(frame, "Sample Plot", labels, init_data)
    frame.Show()
    app.MainLoop()
