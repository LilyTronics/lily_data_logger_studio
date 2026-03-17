"""
Unit test for the configuration.
"""

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class ConfigurationTest(TestSuite):

    _EXPECTED_GROUPS = ["settings", "instruments", "measurements", "process", "graphs"]
    _configuration = Configuration()

    def setup(self):
        Drivers.load()
        drivers = Drivers.get_drivers()
        self.fail_if(len(drivers) == 0, "No driver available, test cannot run")

    def test_default_config(self):
        groups = self._configuration.get_main_groups()
        self.log.debug(f"Main groups: {groups}")
        self.fail_if(sorted(list(groups)) != sorted(self._EXPECTED_GROUPS),
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

    ################
    # Measurements #
    ################

    def test_add_measurement(self):
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 0, "There should be no measurements")

        self.log.debug("Add measurement")
        self._configuration.add_measurement("test measurement 1", "instr-1234", "ch-1",
                                            "V", 1.0, 0.0)
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 1, "Measurement was not added")

        self.log.debug("Add measurement with same name")
        try:
            self._configuration.add_measurement("test measurement 1", "instr-1234", "ch-1",
                                                "V", 1.0, 0.0)
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A measurement with this name already exists",
                         "Invalid exception message")
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 1, "There should be one measurement")

    def test_edit_measurements(self):
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 1, "There should be one measurement")

        self.log.debug("Add another measurement")
        self._configuration.add_measurement("test measurement 2", "instr-1234", "ch-2",
                                            "V", 1.0, 0.0)
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 2, "Measurement was not added")

        self.log.debug("Update measurement name")
        measurement = measurements[0]
        self._configuration.update_measurement(measurement["id"], "Test measurement 3",
                                               measurement["instrument_id"],
                                               measurement["channel_id"], measurement["unit"],
                                               measurement["gain"], measurement["offset"])
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")

        self.log.debug("Update with an existing name")
        measurement = measurements[0]
        try:
            self._configuration.update_measurement(measurement["id"], measurements[1]["name"],
                                                   measurement["instrument_id"],
                                                   measurement["channel_id"], measurement["unit"],
                                                   measurement["gain"], measurement["offset"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A measurement with this name already exists",
                         "Invalid exception message")
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")

        self.log.debug("Update with an invallid ID")
        measurement = measurements[0]
        try:
            self._configuration.update_measurement("invalid ID", measurement["name"],
                                                   measurement["instrument_id"],
                                                   measurement["channel_id"], measurement["unit"],
                                                   measurement["gain"], measurement["offset"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No measurement found for this ID",
                         "Invalid exception message")

    def test_delete_measurement(self):
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        n_measurements = len(measurements)
        self.fail_if(n_measurements < 1, "There should be at least one measurement")

        self.log.debug("Delete measurement")
        self._configuration.delete_measurement(measurements[0]["id"])
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != n_measurements - 1, "Measurement was not deleted")

        self.log.debug("Delete measurement with invalid ID")
        try:
            self._configuration.delete_measurement("invalid ID")
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No measurement found for this ID",
                         "Invalid exception message")


if __name__ == "__main__":

    ConfigurationTest().run(True)
