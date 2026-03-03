"""
Main controller.
"""

import wx

import src.models.id_manager as IdManager

from src.models.application_settings import ApplicationSettings
from src.models.configuration import Configuration
from src.models.test_options import TestOptions
from src.views.view_data_table import ViewDataTable
from src.views.view_graph import ViewGraph
from src.views.view_instruments import ViewInstruments
from src.views.view_main import MainView
from src.views.view_process import ViewProcess
from src.views.view_settings import ViewSettings


class MainController:

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start main controller")
        self._app_settings = ApplicationSettings()
        self._configuration = Configuration()

        self._logger.debug("Load main view")
        self._view = MainView(title)
        value = self._app_settings.get_main_window_position()
        if -1 not in value:
            self._view.SetPosition(value)
        value = self._app_settings.get_main_window_size()
        if -1 not in value:
            self._view.SetSize(value)
        self._view.Maximize(self._app_settings.get_main_window_maximized())
        self._view.set_tree_width(self._app_settings.get_main_window_tree_width())
        self._view.set_log_height(self._app_settings.get_main_window_log_height())
        self._logger.debug("Show main view")
        self._view.Show()

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_MENU, self._on_menu_exit, id=IdManager.ID_MENU_EXIT)

        self._view.Bind(wx.EVT_TOOL, self._on_open_config, id=IdManager.ID_OPEN_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._on_save_config, id=IdManager.ID_SAVE_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._show_settings, id=IdManager.ID_SHOW_SETTINGS)
        self._view.Bind(wx.EVT_TOOL, self._show_instruments, id=IdManager.ID_SHOW_INSTRUMENTS)
        self._view.Bind(wx.EVT_TOOL, self._show_process, id=IdManager.ID_SHOW_PROCESS)
        self._view.Bind(wx.EVT_TOOL, self._show_data_table, id=IdManager.ID_SHOW_DATA_TABLE)
        self._view.Bind(wx.EVT_TOOL, self._show_graph, id=IdManager.ID_SHOW_GRAPH)

        self._view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_tree_item_activated, id=IdManager.ID_TREE)

        self._process_test_options(test_options)
        wx.CallAfter(self._view.update_configuration, self._configuration)

    ###########
    # Private #
    ###########

    def _process_test_options(self, test_options):
        if test_options.show_view_settings:
            self._logger.debug("Test option: show view settings")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_SETTINGS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_view_instruments:
            self._logger.debug("Test option: show view instruments")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_INSTRUMENTS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_view_process:
            self._logger.debug("Test option: show view process")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_PROCESS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_view_data_table:
            self._logger.debug("Test option: show view data table")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_DATA_TABLE)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_view_graph:
            self._logger.debug("Test option: show view graph")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_GRAPH)
            wx.PostEvent(self._view.GetEventHandler(), event)

    def _show_child_window(self, child_class):
        matches = list(filter(lambda x: isinstance(x, child_class), self._view.GetChildren()))
        if len(matches) == 0:
            cw = child_class(self._view)
            cw.Show()
        else:
            cw = matches[0]
            cw.Restore()
        cw.Activate()

    def _show_settings(self, event):
        dlg = ViewSettings(self._view)
        dlg.ShowModal()
        dlg.Destroy()
        event.Skip()

    def _show_instruments(self, event):
        self._show_child_window(ViewInstruments)
        event.Skip()

    def _show_process(self, event):
        self._show_child_window(ViewProcess)
        event.Skip()

    def _show_data_table(self, event):
        self._show_child_window(ViewDataTable)
        event.Skip()

    def _show_graph(self, event):
        self._show_child_window(ViewGraph)
        event.Skip()

    ##################
    # Event handlers #
    ##################

    def _on_open_config(self, event):
        dlg_title = "Open configuration"
        dlg = wx.FileDialog(self._view, dlg_title,
                            wildcard="Configuration files (JSON)|*.json",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            try:
                self._configuration.load(filename)
                self._logger.debug(f"Configuration loaded from: {filename}")
            except Exception as e:
                self._logger.error(f"Error loading configuration: {e}")
                wx.MessageBox(f"Error loading configuration: {e}", dlg_title,
                              wx.ICON_EXCLAMATION, self._view)
        dlg.Destroy()
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _on_save_config(self, event):
        dlg_title = "Save configuration"
        dlg = wx.FileDialog(self._view, dlg_title,
                            wildcard="Configuration files (JSON)|*.json",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            try:
                self._configuration.save(filename)
                self._logger.debug(f"Configuration saved to: {filename}")
                self._view.update_configuration(self._configuration)
            except Exception as e:
                self._logger.error(f"Error saving configuration: {e}")
                wx.MessageBox(f"Error saving configuration: {e}", dlg_title,
                              wx.ICON_EXCLAMATION, self._view)

        dlg.Destroy()
        event.Skip()

    def _on_tree_item_activated(self, event):
        tree = event.GetEventObject()
        item = event.GetItem()
        if item.IsOk():
            item_text = tree.GetItemText(item)
            if item_text == "settings":
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_SETTINGS)
                wx.PostEvent(self._view.GetEventHandler(), post_event)
            if item_text == "instruments":
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_INSTRUMENTS)
                wx.PostEvent(self._view.GetEventHandler(), post_event)
            if item_text == "process":
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_PROCESS)
                wx.PostEvent(self._view.GetEventHandler(), post_event)
            if item_text == "measurements":
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_DATA_TABLE)
                wx.PostEvent(self._view.GetEventHandler(), post_event)
            if item_text == "graphs":
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_GRAPH)
                wx.PostEvent(self._view.GetEventHandler(), post_event)

        event.Skip()

    def _on_menu_exit(self, event):
        self._view.Close()
        event.Skip()

    def _on_view_close(self, event):
        self._logger.debug("Close main view")
        self._app_settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_main_window_position(*self._view.GetPosition())
            self._app_settings.store_main_window_size(*self._view.GetSize())
        self._app_settings.store_main_window_tree_width(self._view.get_tree_width())
        self._app_settings.store_main_window_log_height(self._view.get_log_height())

        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
