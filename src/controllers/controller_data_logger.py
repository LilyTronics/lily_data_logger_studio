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
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.views.view_dialog_check_instruments import ViewDialogCheckInstruments
from src.views.view_dialogs import ViewDialogs


class ControllerDataLogger:

    def __init__(self, parent_view, configuration, logger):
        self._parent_view = parent_view
        self._configuration = configuration
        self._logger = logger
        self._measurements_runner = MeasurementsRunner(self._configuration, self._logger)
        self._process_runner = ProcessRunner(self._configuration, self._logger,
                                             self._process_update)
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
                    wx.CallAfter(self._parent_view.update_process, 0)

                if update_main:
                    wx.CallAfter(self._parent_view.update_status, status)
                    update_main = False

            except Exception as e:
                self._logger.error("Error in data logger monitor thread:")
                self._logger.error(str(e))

            time.sleep(0.01)

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
            target=self._run_check_instruments, args=(dlg,), daemon=True
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
        if dlg:
            wx.CallAfter(dlg.Close)

    def _measurements_update(self, *params):
        print(params)

    def _process_update(self, *params):
        wx.CallAfter(self._parent_view.update_process, *params)

    ##########
    # Public #
    ##########

    def start(self):
        if self.is_running():
            return
        if not self._check_configuration():
            return
        if not self._setup_instruments_pool():
            return
        if not self._setup_measurements_pool():
            return
        if not self._check_instruments():
            return

        if len(self._configuration.get_measurements()) > 0:
            self._measurements_runner.start()
        if len(self._configuration.get_process_steps()) > 0:
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
