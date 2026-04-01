"""
Common view code.
"""

import wx

import src.views.gui_sizes as GuiSizes


def create_settings_grid(settings, grid, parent, controls_dict):
    controls_dict.clear()
    grid.Clear(True)
    if settings is None or len(settings) == 0:
        grid.Add(wx.Panel(parent), (0, 0))
    else:
        try:
            for i, setting in enumerate(settings):
                lbl = wx.StaticText(parent, wx.ID_ANY, f"{setting.name}:")
                ctrl_class = getattr(wx, setting.gui_control)
                ctrl = ctrl_class(parent, wx.ID_ANY, size=GuiSizes.WIDTH_MEDIUM)
                ctrl.SetValue("" if setting.default_value is None else str(setting.default_value))
                grid.Add(lbl, (i, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                grid.Add(ctrl, (i, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                controls_dict[setting.name] = (ctrl, setting.type)
        except:
            # Restore layout
            grid.Add(wx.Panel(parent), (0, 0))
            parent.Layout()
            raise
