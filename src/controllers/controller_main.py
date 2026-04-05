"""
Main controller.
"""

import threading
import time
import wx

import src.app_data as AppData
import src.models.id_manager as IdManager

from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_data_logger import ControllerDataLogger
from src.controllers.controller_drivers import ControllerDrivers
from src.controllers.controller_edit_graphs import ControllerEditGraphs
from src.controllers.controller_edit_instruments import ControllerEditInstruments
from src.controllers.controller_edit_measurements import ControllerEditMeasurements
from src.controllers.controller_edit_process import ControllerEditProcess
from src.controllers.controller_edit_settings import ControllerEditSettings
from src.models.application_settings import ApplicationSettings
from src.models.configuration import Configuration
from src.models.os_specifics import get_platform_info
from src.models.os_specifics import is_valid_display_session
from src.models.test_options import TestOptions
from src.views.view_frame_main import ViewFrameMain
from src.views.view_dialogs import ViewDialogs


class ControllerMain:

    _MONITOR_UPDATE_RATE = 0.5

    def __init__(self, title, logger, test_options=TestOptions):
        self._logger = logger
        self._logger.debug("Start main controller")
        self._app_settings = ApplicationSettings()
        self._configuration = Configuration()
        self._view_progress = None
        self._stop_event = threading.Event()
        self._monitor_thread = None

        self._logger.debug("Load main view")
        self._view = ViewFrameMain(title, AppData.APP_LOG_FILE, is_valid_display_session)
        self._prepare_view()
        self._logger.debug("Show main view")
        self._view.Show()

        self._check_display_session()

        self._controller_drivers = ControllerDrivers(self._view, self._logger,
                                                     test_options.suppress_loading_drivers)
        self._controller_data_logger = ControllerDataLogger(self._view, self._configuration,
                                                            self._logger)

        wx.CallAfter(self._view.update_configuration, self._configuration)

        # Invloke loading drivers
        event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_RELOAD_DRIVERS)
        wx.PostEvent(self._view.GetEventHandler(), event)

        self._process_test_options(test_options)
        wx.CallAfter(self._start_monitor_thread)

    ###########
    # Private #
    ###########

    def _check_display_session(self):
        if not self._app_settings.get_check_display_session() or is_valid_display_session():
            return

        msg = (
            f"You are running on: {get_platform_info()}.\n"
            "Some window docking/undocking features (AUI panes) may not work reliable "
            "unless you are using Xorg (X11).\n"
            "You can continue, but docking will be limited."
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
        self._view.Bind(wx.EVT_TOOL, self._on_new_config, id=IdManager.ID_NEW_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._on_open_config, id=IdManager.ID_OPEN_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._on_save_config, id=IdManager.ID_SAVE_CONFIG)
        self._view.Bind(wx.EVT_TOOL, self._on_reload_drivers, id=IdManager.ID_RELOAD_DRIVERS)
        self._view.Bind(wx.EVT_TOOL, self._show_edit_settings, id=IdManager.ID_SHOW_EDIT_SETTINGS)
        self._view.Bind(wx.EVT_TOOL, self._show_edit_instruments,
                        id=IdManager.ID_SHOW_EDIT_INSTRUMENTS)
        self._view.Bind(wx.EVT_TOOL, self._show_edit_measurements,
                        id=IdManager.ID_SHOW_EDIT_MEASUREMENTS)
        self._view.Bind(wx.EVT_TOOL, self._show_edit_process,
                        id=IdManager.ID_SHOW_EDIT_PROCESS)
        self._view.Bind(wx.EVT_TOOL, self._show_edit_graphs,
                        id=IdManager.ID_SHOW_EDIT_GRAPHS)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_start, id=IdManager.ID_START_LOGGER)
        self._view.Bind(wx.EVT_TOOL, self._on_data_logger_stop, id=IdManager.ID_STOP_LOGGER)


    def _process_test_options(self, test_options):
        if test_options.load_test_configuration:
            self._logger.debug("Test option: load test configuration")
            self._configuration.load(AppData.TEST_CONFIGURATION)

        if test_options.show_edit_settings:
            self._logger.debug("Test option: show edit settings")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_SETTINGS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_edit_instruments:
            self._logger.debug("Test option: show edit instruments")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_INSTRUMENTS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_edit_measurements:
            self._logger.debug("Test option: show edit measurements")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_MEASUREMENTS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_edit_process:
            self._logger.debug("Test option: show edit process")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_PROCESS)
            wx.PostEvent(self._view.GetEventHandler(), event)

        if test_options.show_edit_graphs:
            self._logger.debug("Test option: show edit graphs")
            event = wx.PyCommandEvent(wx.EVT_TOOL.typeId, IdManager.ID_SHOW_EDIT_GRAPHS)
            wx.PostEvent(self._view.GetEventHandler(), event)

    def _start_monitor_thread(self):
        if not (self._monitor_thread is not None and self._monitor_thread.is_alive()):
            self._monitor_thread = threading.Thread(name="Data logger monitor",
                                                    target=self._data_logger_monitor,
                                                    daemon=True)
            self._monitor_thread.start()

    def _stop_monitor_thread(self):
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            self._stop_event.set()
            self._monitor_thread.join()

    def _data_logger_monitor(self):
        self._logger.debug("Data logger monitor started")
        status= "idle"
        update_main = True
        while not self._stop_event.is_set():
            try:
                # Detect change
                if self._controller_data_logger.is_running() and status == "idle":
                    status = "running"
                    update_main = True
                    self._logger.info("Data logger started")
                elif not self._controller_data_logger.is_running() and status == "running":
                    status = "idle"
                    update_main = True
                    self._logger.info("Data logger stopped")
                    self._view.update_process(0)

                if update_main:
                    wx.CallAfter(self._view.update_status, status)
                    update_main = False

                if self._controller_data_logger.is_running():
                    # Update GUI with data
                    self._view.update_process(self._controller_data_logger.get_process_step_index())
                    test_run = self._controller_data_logger.get_test_run()
                    if test_run is not None:
                        wx.CallAfter(self._update_data_table, test_run)
                        wx.CallAfter(self._update_graphs, test_run)

            except Exception as e:
                self._logger.error("Error in data logger monitor thread:")
                self._logger.error(str(e))
            time.sleep(self._MONITOR_UPDATE_RATE)
        self._logger.debug("Data logger monitor stopped")

    def _update_data_table(self, test_run):
        table_data = {
            "timestamps": test_run["timestamps"],
            "measurements": {}
        }
        for m in test_run["measurements"]:
            table_data["measurements"][m["name"]] = m["values"]
        self._view.update_data_table(table_data)

    def _update_graphs(self, test_run):
        # We can only create a graph if we have 2 or more samples
        if len(test_run["timestamps"]) < 2:
            return

        # Create x values for the graph
        x_values = [0]
        for i in range(1, len(test_run["timestamps"])):
            x_values.append(test_run["timestamps"][i] - test_run["timestamps"][0])
        graphs = self._configuration.get_graphs()
        graphs_data = {}
        for graph in graphs:
            lines = []
            for m in graph["measurements"]:
                matches = [x for x in test_run["measurements"] if x["id"] == m]
                if len(matches) != 1:
                    continue
                data = []
                previous_value = 0
                for i, value in enumerate(matches[0]["values"]):
                    # We can only show int or floats in the graph
                    if isinstance(value, (int, float)):
                        previous_value = value
                    else:
                        value = previous_value
                    data.append((x_values[i], value))
                line_data = {
                    "legend": f"{matches[0]['name']} [{matches[0]['unit']}]",
                    "data": data
                }
                lines.append(line_data)
            graphs_data[graph["name"]] = {
                "lines": lines,
                "settings": graph["settings"]
            }
        self._view.update_graphs(graphs_data)

    ##################
    # Event handlers #
    ##################

    def _show_edit_settings(self, event):
        ControllerEditSettings(self._view, self._configuration, self._logger)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_edit_instruments(self, event):
        ControllerEditInstruments(self._view, self._logger, self._configuration)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_edit_measurements(self, event):
        ControllerEditMeasurements(self._view, self._logger, self._configuration)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_edit_process(self, event):
        ControllerEditProcess(self._view, self._logger, self._configuration)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _show_edit_graphs(self, event):
        ControllerEditGraphs(self._view, self._logger, self._configuration)
        self._view.update_configuration(self._configuration)
        event.Skip()

    def _on_reload_drivers(self, event):
        self._controller_drivers.load()
        event.Skip()

    def _on_new_config(self, event):
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
        self._stop_monitor_thread()
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
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
