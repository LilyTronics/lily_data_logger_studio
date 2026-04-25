"""
Unit test for the drivers model only (not the drivers itself).
"""

import os

import src.app_data as AppData

from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class DriversTest(TestSuite):

    expected_nr_of_drivers = 0

    def setup(self):
        for item in os.listdir(AppData.DRIVERS_PATH):
            folder = os.path.join(AppData.DRIVERS_PATH, item)
            if os.path.isdir(folder):
                for current_folder, sub_folders, filenames in os.walk(folder):
                    sub_folders.sort()
                    if "__pycache__" in current_folder:
                        continue
                    for filename in filenames:
                        if filename == "__init__.py" or not filename.endswith(".py"):
                            continue
                        fullname = os.path.join(current_folder, filename)
                        self.expected_nr_of_drivers += self.get_driver_count(fullname)
        self.log.debug(f"Expected number of drivers: {self.expected_nr_of_drivers}")

    def get_driver_count(self, filename):
        n_drivers = 0
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                if "if __name__ == \"__main__\":" in line:
                    break
                if line.startswith("class ") and "DriverBase" in line:
                    n_drivers += 1
        return n_drivers

    def on_progress(self, count, message):
        self.log.debug(f"(Progress): {count} - {message}")

    def test_list_drivers(self):
        Drivers.load(self.on_progress)
        drivers = Drivers.get_drivers()
        self.log.debug("Drivers:")
        for d in drivers:
            self.log.debug(f"{d}")
        self.fail_if(len(drivers) != self.expected_nr_of_drivers,
            f"The numbers of drivers is not correct. Expected: {self.expected_nr_of_drivers}")

    def test_reload_drivers(self):
        self.log.debug("Reload drivers")
        Drivers.load(self.on_progress)
        drivers = Drivers.get_drivers()
        for d in drivers:
            self.log.debug(f"{d}")

    def test_get_driver(self):
        drivers = Drivers.get_drivers()
        self.fail_if(len(drivers) == 0, "Drivers required for this test")
        for query in (drivers[0].id, drivers[0].get_class_name(), drivers[0].name):
            self.log.debug(f"Get driver for {query}")
            driver_class = Drivers.get_driver(query)
            self.log.debug(f"Driver class: {driver_class}")
            self.fail_if(driver_class is None, "No driver found")


if __name__ == "__main__":

    DriversTest().run(True)
