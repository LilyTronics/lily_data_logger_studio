"""
Controller for the driver test application.
"""

import wx

from copy import deepcopy

import src.app_data as AppData
import src.models.id_manager as IdManager

from src.controllers.controller_drivers import ControllerDrivers
from src.models.application_settings import ApplicationSettings
from src.models.drivers import Drivers
from src.models.test_options import TestOptions
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialogs import ViewDialogs
from src.views.view_frame_driver_test import ViewFrameDriverTest


class ControllerDriverTest:

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start driver test controller")
        self._app_settings = ApplicationSettings()
        self._driver_class = None

        self._logger.debug("Load driver test view")
        self._view = ViewFrameDriverTest(title, AppData.DRIVER_TEST_LOG_FILE)

        value = self._app_settings.get_driver_test_window_position()
        if -1 not in value:
            self._view.SetPosition(value)
        value = self._app_settings.get_driver_test_window_size()
        if -1 not in value:
            self._view.SetSize(value)
        self._view.Maximize(self._app_settings.get_driver_test_window_maximized())

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_BUTTON, self._on_reload_drivers,
                        id=IdManager.ID_DRIVER_TEST_RELOAD_DRIVERS)
        self._view.Bind(wx.EVT_LISTBOX, self._on_driver_select,
                        id=IdManager.ID_DRIVER_TEST_LIST_DRIVERS)
        self._view.Bind(wx.EVT_LISTBOX, self._on_channel_select,
                        id=IdManager.ID_DRIVER_TEST_LIST_CHANNELS)
        self._view.Bind(wx.EVT_BUTTON, self._on_test_driver,
                        id=IdManager.ID_DRIVER_TEST_TEST)

        self._logger.debug("Show driver test view")
        self._view.Show()

        self._controller_drivers = ControllerDrivers(self._view, self._logger,
                                                     test_options.suppress_loading_drivers)

        # Invoke loading drivers
        event = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, IdManager.ID_DRIVER_TEST_RELOAD_DRIVERS)
        wx.PostEvent(self._view.GetEventHandler(), event)

    ###########
    # Private #
    ###########

    def _test_driver(self, settings):
        driver = None
        try:
            driver_name = settings.get("driver", {}).get("name", None)
            driver_settings = settings.get("driver", {}).get("settings", {})
            self._logger.debug(f"Driver: '{driver_name}'")
            self._logger.debug(f"Driver settings: {driver_settings}")
            channel_name = settings.get("channel", {}).get("name", None)
            channel_params = settings.get("channel", {}).get("params", {})
            self._logger.debug(f"Channel: '{channel_name}'")
            self._logger.debug(f"Channel parameters: {channel_params}")
            driver_class = Drivers.get_driver(driver_name)
            if driver_class is None:
                raise Exception(f"Driver '{driver_name}' not found")
            driver = driver_class(driver_settings)
            channel = driver.get_channel(channel_name)
            if channel is None:
                raise Exception(f"Channel '{channel_name}' not found in driver '{driver_name}'")
            if driver.is_simulator:
                start_simulators()
            self._logger.debug("Process channel")
            result = driver.process_channel(channel_name, channel_params)
            self._logger.debug(f"Result: {result}")
        finally:
            if driver is not None:
                driver.close()
            stop_simulators()

    ##################
    # Event handlers #
    ##################

    def _on_reload_drivers(self, event):
        self._logger.debug("Load drivers")
        self._controller_drivers.load()
        self._view.update_drivers(Drivers.get_drivers())
        self._view.update_channels([])
        self._view.show_driver_settings(None)
        self._view.show_channel_settings(None)
        event.Skip()

    def _on_driver_select(self, event):
        driver_class = Drivers.get_driver(event.GetString())
        self._driver_class = driver_class
        try:
            if self._driver_class is None:
                raise Exception(f"Driver '{event.GetString()}' not found")
            channels = self._driver_class.channels
            self._view.update_channels(channels)
            settings = self._driver_class.driver_settings
            self._view.show_driver_settings(settings)
        except Exception as e:
            self._logger.error(f"Error loading driver: {e}")
            ViewDialogs.show_message(self._view, f"Error loading driver: {e}",
                                     "Select driver", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_channel_select(self, event):
        channel_name = event.GetString()
        if self._driver_class is not None:
            try:
                channel = self._driver_class.get_channel(channel_name)
                if channel is None:
                    raise Exception(f"Channel '{event.GetString()}' not found")
                params = deepcopy(channel.parameters)
                if channel.direction == channel.DIR_OUTPUT:
                    setting_class = self._driver_class.get_driver_setting_class()
                    params.append(setting_class(
                        "value", channel.value_type, None, setting_class.CTRL_TEXT
                    ))
                self._view.show_channel_settings(params)
            except Exception as e:
                self._logger.error(f"Error loading channel: {e}")
                ViewDialogs.show_message(self._view, f"Error loading channel: {e}",
                                        "Select channel", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_test_driver(self, event):
        self._logger.empty_line()
        self._logger.info("Test driver")
        try:
            settings = self._view.get_settings()
            self._test_driver(settings)
        except Exception as e:
            self._logger.error(f"Error testing driver: {e}")
            ViewDialogs.show_message(self._view, f"Error testing driver: {e}",
                                        "Test driver", wx.ICON_EXCLAMATION)
        self._logger.info("Driver test completed")
        event.Skip()

    def _on_view_close(self, event):
        self._app_settings.store_driver_test_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_driver_test_window_position(*self._view.GetPosition())
            self._app_settings.store_driver_test_window_size(*self._view.GetSize())
        event.Skip()


if __name__ == "__main__":

    from src.driver_test import run_driver_test

    TestOptions.log_to_stdout = True

    run_driver_test(TestOptions)
