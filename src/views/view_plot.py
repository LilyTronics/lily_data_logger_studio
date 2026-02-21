"""
Plot view.
"""

import wx.lib.plot


class ViewPlot(wx.lib.plot.PlotCanvas):

    def __init__(self, parent, title):
        self.title = title
        super().__init__(parent)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.fontSizeLegend = 8
        self.fontSizeAxis = 8
        self.fontSizeTitle = 10
        self.enableLegend = True
        self.enableTicks = (True, True, False, False)
        self.enableAntiAliasing = True
        self.xSpec = "auto"
        self.ySpec = "auto"

        gc = wx.lib.plot.PlotGraphics([wx.lib.plot.PolyLine([])], title)
        self.Draw(gc, xAxis=(0, 1), yAxis=(0, 1))


if __name__ == "__main__":

    app = wx.App(False)
    frame = wx.Frame(None, title="Test ViewPlot", size=(800, 600))
    plot_view = ViewPlot(frame, "Sample Plot")
    frame.Show()
    app.MainLoop()
