"""
Controller for the data logger.
"""

import threading
import time
import wx

from src.models.instrument_pool import InstrumentPool
from src.models.measurements_pool import MeasurementsPool
from src.models.measurements_runner import MeasurementsRunner
from src.models.process_runner import ProcessRunner
from src.models.test_runs import TestRuns
from src.models.time_converter import TimeConverter
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialog_check_instruments import ViewDialogCheckInstruments
from src.views.view_dialogs import ViewDialogs


class ControllerDataLogger:

    def __init__(self, parent_view, configuration, logger):
        self._parent_view = parent_view
        self._configuration = configuration
        self._logger = logger
        self._measurements_runner = MeasurementsRunner(self._configuration, self._logger,
                                                       self._parent_view.update_test_run_data)
        self._process_runner = ProcessRunner(self._configuration, self._logger,
                                             self._parent_view.update_process)
        self._check_result = False
        self._data_logger_thread = None
        self._stop_event = threading.Event()

    ###########
    # Private #
    ###########

    def _run_data_logger(self):
        self._logger.debug("Run data logger")
        if len(self._configuration.get_measurements()) > 0:
            self._measurements_runner.start()
        if len(self._configuration.get_process_steps()) > 0:
            self._process_runner.start()

        settings = self._configuration.get_settings()
        mode = settings["mode"]
        end_time = settings["end_time"]
        self._logger.debug(f"Run mode: {mode}")
        if mode == "fixed time":
            self._logger.debug(f"End time: {TimeConverter.create_duration_time_string(end_time)}")
        wx.CallAfter(self._parent_view.update_status, "running")
        start = time.time()
        while not self._stop_event.is_set():
            if mode == "fixed time" and time.time() - start > end_time:
                self._logger.debug("End time reached")
                break
            if mode == "process end" and not self._process_runner.is_running():
                self._logger.debug("Process ended")
                break
            time.sleep(0.1)

        wx.CallAfter(self._parent_view.update_status, "idle")
        wx.CallAfter(self._parent_view.update_process, -1)
        wx.CallAfter(self._parent_view.update_test_runs, TestRuns.get_test_runs())

        self._measurements_runner.stop()
        self._process_runner.stop()
        stop_simulators()
        self._logger.debug("Data logger stopped")

    def _check_configuration(self):
        dlg_title = "Check configuration"
        has_instruments = len(self._configuration.get_instruments()) > 0
        if not has_instruments:
            ViewDialogs.show_message(
                self._parent_view, "No instruments in the configuration.", dlg_title
            )
            return False

        has_measurements = len(self._configuration.get_measurements()) > 0
        has_steps = len(self._configuration.get_process_steps()) > 0

        if not (has_measurements or has_steps):
            ViewDialogs.show_message(
                self._parent_view, "No measurments or steps in the configuration.", dlg_title
            )
            return False
        settings = self._configuration.get_settings()
        if settings["mode"] == "process end" and not has_steps:
            ViewDialogs.show_message(
                self._parent_view, "Mode is set to process end, but no steps in the configuration.",
                dlg_title
            )
            return False
        return True

    def _setup_instruments_pool(self):
        instruments = self._configuration.get_instruments()
        InstrumentPool.clear()
        try:
            InstrumentPool.add_instruments(instruments)
            if InstrumentPool.has_simulators():
                start_simulators()
            return True
        except Exception as e:
            ViewDialogs.show_message(
                self._parent_view, f"Error initializing instruments:\n{e}.", "Setup instruments",
                wx.ICON_EXCLAMATION
            )
        return False

    def _setup_measurements_pool(self):
        measurements = self._configuration.get_measurements()
        MeasurementsPool.clear()
        try:
            MeasurementsPool.add_measurements(measurements)
            return True
        except Exception as e:
            ViewDialogs.show_message(
                self._parent_view, f"Error initializing measurements:\n{e}.", "Setup measurments",
                wx.ICON_EXCLAMATION
            )
        return False

    def _check_instruments(self):
        self._check_result = False
        instruments = self._configuration.get_instruments()
        dlg = ViewDialogCheckInstruments(self._parent_view)
        dlg.add_instruments(instruments)
        threading.Thread(
            target=self._run_check_instruments, name="CheckInstruments", args=(dlg,), daemon=True
        ).start()
        dlg.ShowModal()
        dlg.Destroy()
        return self._check_result

    def _run_check_instruments(self, dlg):
        results = []
        for key, instrument in InstrumentPool.get_instruments().items():
            message = ""
            try:
                instrument.test_driver()
                results.append(True)
                message = "Instrument OK"
            except Exception as e:
                results.append(False)
                message = str(e)
            # Dialog could be closed by the user
            if not dlg:
                self._check_result = False not in results
                return
            wx.CallAfter(dlg.update_instrument, key, results[-1], message)
        self._check_result = False not in results
        wx.Sleep(1)
        if dlg and self._check_result:
            wx.CallAfter(dlg.Close)

    ##########
    # Public #
    ##########

    def start(self):
        if self._data_logger_thread is not None and self._data_logger_thread.is_alive():
            return
        if not self._check_configuration():
            return
        if not self._setup_instruments_pool():
            return
        if not self._setup_measurements_pool():
            return
        if not self._check_instruments():
            return
        if (len(self._configuration.get_measurements()) == 0 and
            len(self._configuration.get_process_steps()) == 0):
            return

        self._stop_event.clear()
        self._data_logger_thread = threading.Thread(name="DataLogger",
                                                    target=self._run_data_logger,
                                                    daemon=True)
        self._data_logger_thread.start()

    def stop(self):
        if self._data_logger_thread is not None:
            if self._data_logger_thread.is_alive():
                self._stop_event.set()
                self._data_logger_thread.join()
            self._data_logger_thread = None

if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
