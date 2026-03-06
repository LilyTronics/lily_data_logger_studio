"""
Unit test for the drivers model only (not the drivers itself).
"""

from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class DriversTest(TestSuite):

    def _on_progress(self, message):
        self.log.debug(f"Loading: {message}")

    def test_list_drivers(self):
        self.log.debug("List drivers, before load")
        print(Drivers.get_drivers())
        self.log.debug("List drivers, after load")
        Drivers.load(self._on_progress)
        print(Drivers.get_drivers())


if __name__ == "__main__":

    DriversTest().run(True)
