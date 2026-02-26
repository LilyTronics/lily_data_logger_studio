"""
Simulator base class.
"""

import threading
import time


class SimulatorBase:

    NAME = "Simulator base class"
    LOOP_INTERVAL = 0.1

    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()

    ###########
    # Private #
    ###########

    def _run(self):
        self.init()
        while not self._stop_event.is_set():
            self.run_handler()
            time.sleep(self.LOOP_INTERVAL)
        self.cleanup()

    #############
    # Overrides #
    #############

    def init(self):
        raise NotImplementedError("The init method must be impemented in the derived class")

    def run_handler(self):
        raise NotImplementedError("The run handler method must be impemented in the derived class")

    def cleanup(self):
        raise NotImplementedError("The cleanup method must be impemented in the derived class")

    ##########
    # Public #
    ##########

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, name=self.NAME)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        if self.is_running():
            self._stop_event.set()
            self._thread.join()

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()


if __name__ == "__main__":

    from src.simulators.test_simulators import test_simulators

    test_simulators()
