"""
Unit test for the drivers model only (not the drivers itself).
"""

from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class DriversTest(TestSuite):

    _EXPECTED_NR_FOF_DRIVERS = 1

    def _on_progress(self, *params):
        self.log.debug(f"Loading: {params}")

    def test_list_drivers(self):
        self.log.debug("List drivers, before load")
        drivers = Drivers.get_drivers()
        self.log.debug(f"Drivers: {drivers}")
        self.fail_if(len(drivers) > 0, "There should not be any drivers")
        self.log.debug("List drivers, after load")
        Drivers.load(self._on_progress)
        drivers = Drivers.get_drivers()
        self.log.debug(f"Drivers: {drivers}")
        self.fail_if(len(drivers) != self._EXPECTED_NR_FOF_DRIVERS,
            f"The numbers of drivers is not correct. Expected: {self._EXPECTED_NR_FOF_DRIVERS}")

    def test_reload_drivers(self):
        self.log.debug("Reload drivers")
        Drivers.load(self._on_progress)
        drivers = Drivers.get_drivers()
        self.log.debug(f"Drivers: {drivers}")

    def test_get_settings(self):
        drivers = Drivers.get_drivers()
        self.fail_if(len(drivers) == 0, "Drivers required for this test")
        name = drivers[0].name
        self.log.debug(f"Get settings for {name}")
        settings = Drivers.get_settings(name)
        self.log.debug(f"Settings: {settings}")

        self.log.debug("Get settings for unknown driver")
        try:
            settings = Drivers.get_settings("unknown driver")
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No driver matching 'unknown driver'",
                         "Invalid exception message")


if __name__ == "__main__":

    DriversTest().run(True)
