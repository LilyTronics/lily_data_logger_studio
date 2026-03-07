"""
Unit test for the configuration.
"""

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class ConfigurationTest(TestSuite):

    _EXPECTED_GROUPS = ["settings", "instruments", "process", "measurements", "graphs"]
    _configuration = Configuration()

    def setup(self):
        Drivers.load()
        drivers = Drivers.get_drivers()
        self.fail_if(len(drivers) == 0, "No driver available, test cannot run")

    def test_default_config(self):
        groups = self._configuration.get_main_groups()
        self.log.debug(f"Main groups: {groups}")
        self.fail_if(list(groups) != self._EXPECTED_GROUPS,
                     f"Invalid main groups. Expected: {self._EXPECTED_GROUPS}")
        for group in groups:
            sub_items = self._configuration.get_sub_items(group)
            self.log.debug(f"Sub items for group '{group}': {sub_items}")

    ###############
    # Instruments #
    ###############

    def test_add_instrument(self):
        drivers = Drivers.get_drivers()
        driver_name = drivers[0].get_class_name()
        settings = {"ip": "1.2.3.4"}
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != 0, "There should be no instruments")

        self.log.debug("Add instrument")
        self._configuration.add_instrument("test instrument 1", driver_name, settings)
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != 1, "Instrument was not added")

        self.log.debug("Add instrument with same name")
        try:
            self._configuration.add_instrument("test instrument 1", driver_name, settings)
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "An instrument with this name already exists",
                         "Invalid exception message")
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != 1, "There should be one instrument")

    def test_edit_instrument(self):
        drivers = Drivers.get_drivers()
        driver_name = drivers[0].get_class_name()
        settings = {"ip": "1.2.3.4"}
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != 1, "There should be one instrument")

        self.log.debug("Add another instrument")
        self._configuration.add_instrument("test instrument 2", driver_name, settings)
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != 2, "Instrument was not added")

        self.log.debug("Update instrument name")
        instrument = instruments[0]
        self._configuration.update_instrument(instrument["id"], "Test instrument 3",
                                              instrument["driver"], instrument["settings"])
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")

        self.log.debug("Update setting")
        instrument = instruments[0]
        settings = {"ip": "5.6.7.8"}
        self._configuration.update_instrument(instrument["id"], instrument["name"],
                                              instrument["driver"], settings)
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")

        self.log.debug("Update with an existing name")
        instrument = instruments[0]
        try:
            self._configuration.update_instrument(instrument["id"], instruments[1]["name"],
                                                instrument["driver"], instrument["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "An instrument with this name already exists",
                         "Invalid exception message")
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")

        self.log.debug("Update with an invallid ID")
        instrument = instruments[0]
        try:
            self._configuration.update_instrument("invalid ID", instrument["name"],
                                                instrument["driver"], instrument["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No instrument found for this ID",
                         "Invalid exception message")

    def test_delete_instrument(self):
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        n_instruments = len(instruments)
        self.fail_if(n_instruments < 1, "There should be at least one instrument")

        self.log.debug("Delete instrument")
        self._configuration.delete_instrument(instruments[0]["id"])
        instruments = self._configuration.get_instruments()
        self.log.debug(f"Instruments: {instruments}")
        self.fail_if(len(instruments) != n_instruments - 1, "Instrument was not deleted")

        self.log.debug("Delete instrument with invalid ID")
        try:
            self._configuration.delete_instrument("invalid ID")
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No instrument found for this ID",
                         "Invalid exception message")


if __name__ == "__main__":

    ConfigurationTest().run(True)
