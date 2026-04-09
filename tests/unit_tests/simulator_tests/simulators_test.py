"""
Unit test for the simulators.
"""

import threading

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from tests.lib.test_suite import TestSuite


class SimulatorsTest(TestSuite):

    _THREADS_TO_CHECK = ["Multi channel analog IO", "Temperature chamber"]

    def _get_running_simulators(self):
        return [x.name for x in threading.enumerate() if x.name in self._THREADS_TO_CHECK]

    def test_start_simulators(self):
        start_simulators()
        self.sleep(1)
        simulators = self._get_running_simulators()
        self.log.debug(f"Simulators running: {simulators}")
        self.fail_if(len(simulators) == 0, "No simulators are running")
        self.fail_if(len(simulators) != len(self._THREADS_TO_CHECK),
                     f"Not all simulators are running. Expected: {self._THREADS_TO_CHECK}")

    def test_start_simulators_while_running(self):
        before_simulators = self._get_running_simulators()
        start_simulators()
        self.sleep(1)
        after_simulators = self._get_running_simulators()
        self.log.debug(f"Simulators running: {after_simulators}")
        self.fail_if(len(after_simulators) != len(before_simulators),
                     f"Invaid number of simulators running. Expected: {before_simulators}")

    def test_stop_simulators(self):
        stop_simulators()
        self.sleep(1)
        simulators = self._get_running_simulators()
        self.log.debug(f"Simulators running: {simulators}")
        self.fail_if(len(simulators) != 0, f"Some simulators are still running: {simulators}")


if __name__ == "__main__":

    SimulatorsTest().run()
