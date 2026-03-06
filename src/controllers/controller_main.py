"""
Main controller.
"""

import wx

import src.models.id_manager as IdManager

from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_data_logger import ControllerDataLogger
from src.controllers.controller_data_table import ControllerDataTable
from src.controllers.controller_graphs import ControllerGraphs
from src.controllers.controller_instruments import ControllerInstruments
from src.controllers.controller_process import ControllerProcess
from src.controllers.controller_settings import ControllerSettings
from src.models.application_settings import ApplicationSettings
from src.models.configuration import Configuration
from src.models.drivers import Drivers
from src.models.test_options import TestOptions
from src.views.view_main import MainView
from src.views.view_progress_dialog import ViewProgressDialog


class MainController:

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start main controller")
        self._app_settings = ApplicationSettings()
        self._configuration = Configuration()
        self._view_progress = None

        self._logger.debug("Load main view")
        self._view = MainView(title)
        self._prepare_view()
        self._logger.debug("Show main view")
        self._view.Show()

        self._process_test_options(test_options)

        self._controller_data_logger = ControllerDataLogger(self._view, self._configuration, self._logger)

        wx.CallAfter(self._view.update_configuration, self._configuration)
        wx.CallAfter(self._load_drivers)

    ###########
    # Private #
    ###########

    def _load_drivers(self):
        self._view_progress = ViewProgressDialog(self._view, "Load drivers", 1)
        try:
            Drivers.load(self._update_view_progress)
        except Exception as e:
            self._logger.Error(f"Error loading driver: {e}")
        self._view_progress.destroy()
        self._view_progress = None

    def _prepare_view(self):
        value = self._app_settings.get_main_window_position()
        if -1 not in value:
            self._view.SetPosition(value)
        value = self._app_settings.get_main_window_size()
        if -1 not in value:
            self._view.SetSize(value)
        self._view.Maximize(self._app_settings.get_main_window_maximized())
        self._view.set_tree_width(self._app_settings.get_main_window_tree_width())
        self._view.set_log_height(self._app_settings.get_main_window_log_height())

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_MENU, self._on_menu_new_config, id=IdManager.ID_MENU_NEW_CONFIG)
        self._view.Bind(wx.EVT_MENU, self._on_menu_exit, id=IdManager.ID_MENU_EXIT)

        self._view.Bind(wx.EVT_TOOL, self._on_open_config, id=IdManager.ID_OPEN_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._on_save_config, id=IdManager.ID_SAVE_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._show_settings, id=IdManager.ID_SHOW_SETTINGS)
        self._view.Bind(wx.EVT_TOOL, self._show_instruments, id=IdManager.ID_SHOW_INSTRUMENTS)
        self._view.Bind(wx.EVT_TOOL, self._show_process, id=IdManager.ID_SHOW_PROCESS)
        self._view.Bind(wx.EVT_TOOL, self._show_data_table, id=IdManager.ID_SHOW_DATA_TABLE)
        self._view.Bind(wx.EVT_TOOL, self._show_graphs, id=IdManager.ID_SHOW_GRAPHS)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_start, id=IdManager.ID_START_LOGGER)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_stop, id=IdManager.ID_STOP_LOGGER)

        self._view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_tree_item_activated,
                        id=IdManager.ID_TREE)

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

        if test_options.show_view_graphs:
            self._logger.debug("Test option: show view graphs")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_GRAPHS)
            wx.PostEvent(self._view.GetEventHandler(), event)

    def _show_settings(self, event):
        ControllerSettings(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_instruments(self, event):
        ControllerInstruments(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_process(self, event):
        ControllerProcess(self._view, self._configuration, self._logger)
        event.Skip()

    def _show_data_table(self, event):
        ControllerDataTable(self._view, self._configuration, self._logger)
        event.Skip()

    def _show_graphs(self, event):
        ControllerGraphs(self._view, self._configuration, self._logger)
        event.Skip()

    ##################
    # Event handlers #
    ##################

    def _update_view_progress(self, value, message, new_max=0):
        if self._view_progress is not None:
            if new_max > 0:
                self._view_progress.set_maximum(new_max)
            self._view_progress.update(value, message)
            wx.YieldIfNeeded()

    def _on_menu_new_config(self, event):
        self._configuration = ControllerConfiguration.new(self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _on_open_config(self, event):
        ControllerConfiguration.load(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _on_save_config(self, event):
        ControllerConfiguration.save(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
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
                post_event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_GRAPHS)
                wx.PostEvent(self._view.GetEventHandler(), post_event)

        event.Skip()

    def _on_data_logger_start(self, event):
        self._controller_data_logger.start()
        event.Skip()

    def _on_data_logger_stop(self, event):
        self._controller_data_logger.stop()
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
