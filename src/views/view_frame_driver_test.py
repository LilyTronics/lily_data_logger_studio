"""
View for the driver test.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as GuiSizes
import src.views.view_common as ViewCommon

from src.views.view_panel_log_messages import ViewPanelLogMessages


class ViewFrameDriverTest(wx.Frame):

    _MIN_WINDOW_SIZE = (950, 700)

    def __init__(self, title, log_filename):
        super().__init__(None, title=title, style=wx.DEFAULT_FRAME_STYLE)
        self._log_filename = log_filename
        self._driver_settings = {}
        self._channel_settings = {}

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.instruments_24.GetBitmap())
        self.SetIcon(icon)

        self._view_panel = wx.Panel(self)
        btn_reload = wx.Button(self._view_panel, IdManager.ID_DRIVER_TEST_RELOAD_DRIVERS,
                               "Reload Drivers")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(btn_reload, 0, wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_controls(self._view_panel), 3, wx.EXPAND)
        box.Add(ViewPanelLogMessages(self._view_panel, self._log_filename), 2, wx.EXPAND | wx.ALL,
                GuiSizes.BOX_SPACING)

        self._view_panel.SetSizer(box)
        self.SetInitialSize(self._MIN_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_controls(self, parent):
        lbl_drivers = wx.StaticText(parent, wx.ID_ANY, "Drivers:")
        lbl_channels = wx.StaticText(parent, wx.ID_ANY, "Channels:")
        self._lst_drivers = wx.ListBox(parent, IdManager.ID_DRIVER_TEST_LIST_DRIVERS,
                                       style=wx.LB_SINGLE)
        self._lst_channels = wx.ListBox(parent, IdManager.ID_DRIVER_TEST_LIST_CHANNELS,
                                        style=wx.LB_SINGLE)

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_drivers, (0, 0), wx.DefaultSpan)
        grid.Add(lbl_channels, (0, 1), wx.DefaultSpan)
        grid.Add(self._lst_drivers, (1, 0), wx.DefaultSpan, wx.EXPAND)
        grid.Add(self._lst_channels, (1, 1), wx.DefaultSpan, wx.EXPAND)
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(1)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(grid, 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_settings_controls(parent), 1, wx.EXPAND | wx.ALL,
                GuiSizes.BOX_SPACING)

        return box

    def _create_settings_controls(self, parent):
        lbl_driver_settings = wx.StaticText(parent, wx.ID_ANY, "Driver Settings:")
        lbl_channel_settings = wx.StaticText(parent, wx.ID_ANY, "Channel Settings:")

        # Placeholder for driver settings
        self._driver_grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        self._driver_grid.Add(wx.Panel(parent), (0, 0))
        # Placeholder for channel settings
        self._channel_grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        self._channel_grid.Add(wx.Panel(parent), (0, 0))

        btn_test = wx.Button(parent, IdManager.ID_DRIVER_TEST_TEST, "Test")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(lbl_driver_settings, 0, wx.EXPAND)
        box.Add(self._driver_grid, 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(lbl_channel_settings, 0, wx.EXPAND)
        box.Add(self._channel_grid, 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(btn_test, 0)

        return box

    ##########
    # Public #
    ##########

    def update_drivers(self, drivers):
        names = [driver.name for driver in drivers]
        self._lst_drivers.Set(names)

    def update_channels(self, channels):
        names = [channel.name for channel in channels]
        self._lst_channels.Set(names)

    def show_driver_settings(self, settings):
        ViewCommon.create_settings_grid(settings, self._driver_grid,
                                        self._view_panel, self._driver_settings)
        self._view_panel.Layout()

    def show_channel_settings(self, settings):
        ViewCommon.create_settings_grid(settings, self._channel_grid,
                                        self._view_panel, self._channel_settings)
        self._view_panel.Layout()

    def get_settings(self):
        return {
            "driver": {
                "name": self._lst_drivers.GetStringSelection(),
                "settings": {
                    name: ctrl[1](ctrl[0].GetValue())
                            for name, ctrl in self._driver_settings.items()
                }
            },
            "channel": {
                "name": self._lst_channels.GetStringSelection(),
                "params": {
                    name: ctrl[1](ctrl[0].GetValue())
                        for name, ctrl in self._channel_settings.items()
                }
            }
        }


if __name__ == "__main__":

    from src.driver_test import run_driver_test
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_driver_test(TestOptions)
