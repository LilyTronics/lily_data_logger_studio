"""
Main controller.
"""

import wx

import src.app_data as AppData
import src.models.id_manager as IdManager

from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_data_logger import ControllerDataLogger
from src.controllers.controller_drivers import ControllerDrivers
from src.controllers.controller_edit_instruments import ControllerEditInstruments
from src.controllers.controller_edit_settings import ControllerEditSettings
from src.models.application_settings import ApplicationSettings
from src.models.configuration import Configuration
from src.models.os_specifics import get_platform_info
from src.models.os_specifics import is_valid_display_session
from src.models.test_options import TestOptions
from src.views.view_frame_main import ViewFrameMain
from src.views.view_dialogs import ViewDialogs


class MainController:

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start main controller")
        self._app_settings = ApplicationSettings()
        self._configuration = Configuration()
        self._view_progress = None

        self._logger.debug("Load main view")
        self._view = ViewFrameMain(title, is_valid_display_session)
        self._prepare_view()
        self._logger.debug("Show main view")
        self._view.Show()

        self._check_display_session()

        self._controller_drivers = ControllerDrivers(self._view, self._logger,
                                                     TestOptions.suppress_loading_drivers)
        self._controller_data_logger = ControllerDataLogger(self._view, self._configuration,
                                                            self._logger)

        wx.CallAfter(self._view.update_configuration, self._configuration)

        # Invloke loading drivers
        event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_RELOAD_DRIVERS)
        wx.PostEvent(self._view.GetEventHandler(), event)

        self._process_test_options(test_options)

    ###########
    # Private #
    ###########

    def _check_display_session(self):
        if not self._app_settings.get_check_display_session() or is_valid_display_session():
            return

        msg = (
            f"You are running on: {get_platform_info()}.\n"
            "Some window docking/undocking features (AUI panes) may not work reliably "
            "unless you are using Xorg (X11).\n"
            "You can continue, but docking will be switched off."
        )
        is_checked = ViewDialogs.show_message(self._view, msg, "Display session notice",
                                              wx.ICON_WARNING, "Don't show this again")
        self._app_settings.store_check_display_session(not is_checked)


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
        self._view.Bind(wx.EVT_TOOL, self._on_reload_drivers, id=IdManager.ID_RELOAD_DRIVERS)
        self._view.Bind(wx.EVT_TOOL, self._show_settings, id=IdManager.ID_SHOW_EDIT_SETTINGS)
        self._view.Bind(wx.EVT_TOOL, self._show_instruments, id=IdManager.ID_SHOW_EDIT_INSTRUMENTS)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_start, id=IdManager.ID_START_LOGGER)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_stop, id=IdManager.ID_STOP_LOGGER)


    def _process_test_options(self, test_options):
        if test_options.load_test_configuration:
            self._logger.debug("Test option: load test configuration")
            self._configuration.load(AppData.TEST_CONFIGURATION)

        if test_options.show_view_settings:
            self._logger.debug("Test option: show view settings")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_SETTINGS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_view_instruments:
            self._logger.debug("Test option: show view instruments")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_INSTRUMENTS)
            wx.PostEvent(self._view.GetEventHandler(), event)

    def _show_settings(self, event):
        ControllerEditSettings(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_instruments(self, event):
        ControllerEditInstruments(self._view, self._logger, self._configuration)
        self._view.update_configuration(self._configuration)
        event.Skip()

    ##################
    # Event handlers #
    ##################

    def _on_reload_drivers(self, event):
        self._controller_drivers.load()
        event.Skip()

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
