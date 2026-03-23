"""
Controller for the data logger.
"""

import threading
import time
import wx

from src.models.instrument_pool import InstrumentPool
from src.models.measurements_runner import MeasurementsRunner
from src.models.process_runner import ProcessRunner
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialog_check_instruments import ViewDialogCheckInstruments
from src.views.view_dialogs import ViewDialogs


class ControllerDataLogger:

    def __init__(self, parent_view, configuration, logger):
        self._parent_view = parent_view
        self._configuration = configuration
        self._logger = logger
        self._measurements_runner = MeasurementsRunner(
            self._configuration, self._logger, self._measurements_callback
        )
        self._process_runner = ProcessRunner(
            self._configuration, self._logger
        )
        self._check_result = False

        threading.Thread(target=self._data_logger_monitor, daemon=True).start()

    ###########
    # Private #
    ###########

    def _data_logger_monitor(self):
        # This thread never stops, unless the application stops
        status= "idle"
        update_main = True
        while True:
            try:
                # Detect state change
                if self.is_running() and status == "idle":
                    status = "running"
                    update_main = True
                    self._logger.info("Data logger started")
                elif not self.is_running() and status == "running":
                    status = "idle"
                    update_main = True
                    self._logger.info("Data logger stopped")

                if update_main:
                    wx.CallAfter(self._parent_view.update_status, status)
                    update_main = False

            except Exception as e:
                self._logger.error("Error in data logger monitor thread:")
                self._logger.error(str(e))

            time.sleep(0.01)

    def _create_and_check_instruments(self):
        instruments = self._configuration.get_instruments()
        InstrumentPool.clear()
        try:
            InstrumentPool.add_instruments(instruments)
        except Exception as e:
            ViewDialogs.show_message(
                self._parent_view, f"Error initializing instruments:\n{e}.", "Check instruments",
                wx.ICON_EXCLAMATION
            )
        dlg = ViewDialogCheckInstruments(self._parent_view)
        dlg.add_instruments(instruments)
        threading.Thread(
            target=self._check_instruments, args=(dlg,), daemon=True
        ).start()
        dlg.ShowModal()
        dlg.Destroy()

    def _check_instruments(self, dlg):
        if InstrumentPool.has_simulators():
            start_simulators()
        self._check_result = True
        for key, instrument in InstrumentPool.get_instruments().items():
            result = False
            message = ""
            try:
                instrument.test_driver()
                result = True
                message = "Instrument OK"
            except Exception as e:
                result = False
                message = str(e)
                self._check_result = False
            # Dialog could be closed by the user
            if not dlg:
                self._check_result = False
                return
            wx.CallAfter(dlg.update_instrument, key, result, message)
        wx.Sleep(1)
        if dlg:
            wx.CallAfter(dlg.Close)

    def _measurements_callback(self, *params):
        print(params)

    ##########
    # Public #
    ##########

    def start(self):
        if self.is_running():
            return

        dlg_title = "Start data logger"
        has_instruments = len(self._configuration.get_instruments()) > 0
        if not has_instruments:
            ViewDialogs.show_message(
                self._parent_view, "No instruments in the configuration.", dlg_title
            )
            return

        has_measurements = len(self._configuration.get_measurements()) > 0
        has_steps = len(self._configuration.get_process_steps()) > 0

        if not (has_measurements or has_steps):
            ViewDialogs.show_message(
                self._parent_view, "No measurments or steps in the configuration.", dlg_title
            )
            return

        self._create_and_check_instruments()
        if not self._check_result:
            ViewDialogs.show_message(
                self._parent_view, "One or more instruments are not available.", dlg_title
            )
            return

        if has_measurements:
            self._measurements_runner.start()
        if has_steps:
            self._process_runner.start()

    def stop(self):
        self._measurements_runner.stop()
        self._process_runner.stop()
        stop_simulators()

    def is_running(self):
        return self._measurements_runner.is_running() or self._process_runner.is_running()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
