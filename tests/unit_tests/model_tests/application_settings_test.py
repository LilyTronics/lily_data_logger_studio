"""
Unit test for the application settings.
"""

import os

import src.app_data as AppData

from src.models.application_settings import ApplicationSettings
from tests.lib.test_suite import TestSuite


class ApplicationSettingsTest(TestSuite):

    _settings = ApplicationSettings()

    def _remove_settings_file(self):
        if os.path.isfile(AppData.SETTINGS_FILE):
            self.log.debug(f"Delete settings file: {AppData.SETTINGS_FILE}")
            os.remove(AppData.SETTINGS_FILE)

    def setup(self):
        self._remove_settings_file()

    def teardown(self):
        self._remove_settings_file()

    def test_main_window_size(self):
        test_value = self._settings.get_main_window_size()
        self.log.debug(f"Current size: {test_value}")
        self.fail_if(test_value != (-1, -1), "Initial value is not correct")
        new_value = (1000, 650)
        self._settings.store_main_window_size(*new_value)
        test_value = self._settings.get_main_window_size()
        self.log.debug(f"New size: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_main_window_position(self):
        test_value = self._settings.get_main_window_position()
        self.log.debug(f"Current position: {test_value}")
        self.fail_if(test_value != (-1, -1), "Initial value is not correct")
        new_value = (50, 75)
        self._settings.store_main_window_position(*new_value)
        test_value = self._settings.get_main_window_position()
        self.log.debug(f"New position: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_main_window_maximized(self):
        test_value = self._settings.get_main_window_maximized()
        self.log.debug(f"Current maximized: {test_value}")
        self.fail_if(test_value, "Initial value is not correct")
        new_value = not test_value
        self._settings.store_main_window_maximized(new_value)
        test_value = self._settings.get_main_window_maximized()
        self.log.debug(f"New maximized: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_main_window_tree_width(self):
        test_value = self._settings.get_main_window_tree_width()
        self.log.debug(f"Current tree width: {test_value}")
        self.fail_if(test_value != -1, "Initial value is not correct")
        new_value = 200
        self._settings.store_main_window_tree_width(new_value)
        test_value = self._settings.get_main_window_tree_width()
        self.log.debug(f"New tree width: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_main_window_log_height(self):
        test_value = self._settings.get_main_window_log_height()
        self.log.debug(f"Current log height: {test_value}")
        self.fail_if(test_value != -1, "Initial value is not correct")
        new_value = 150
        self._settings.store_main_window_log_height(new_value)
        test_value = self._settings.get_main_window_log_height()
        self.log.debug(f"New log height: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_driver_test_window_size(self):
        test_value = self._settings.get_driver_test_window_size()
        self.log.debug(f"Current size: {test_value}")
        self.fail_if(test_value != (-1, -1), "Initial value is not correct")
        new_value = (1000, 650)
        self._settings.store_driver_test_window_size(*new_value)
        test_value = self._settings.get_driver_test_window_size()
        self.log.debug(f"New size: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_driver_test_window_position(self):
        test_value = self._settings.get_driver_test_window_position()
        self.log.debug(f"Current position: {test_value}")
        self.fail_if(test_value != (-1, -1), "Initial value is not correct")
        new_value = (50, 75)
        self._settings.store_driver_test_window_position(*new_value)
        test_value = self._settings.get_driver_test_window_position()
        self.log.debug(f"New position: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_driver_test_window_maximized(self):
        test_value = self._settings.get_driver_test_window_maximized()
        self.log.debug(f"Current maximized: {test_value}")
        self.fail_if(test_value, "Initial value is not correct")
        new_value = not test_value
        self._settings.store_driver_test_window_maximized(new_value)
        test_value = self._settings.get_driver_test_window_maximized()
        self.log.debug(f"New maximized: {test_value}")
        self.fail_if(test_value != new_value, "Stored value is not correct")

    def test_recent_fonfigurations(self):
        configs = self._settings.get_recent_configurations()
        self.log.debug(configs)
        self.fail_if(len(configs) != 0, "There should be no recent configurations")
        self.log.debug("Add configurations up to the max")
        for i in range(self._settings.MAX_RECENT_CONFIGS):
            self._settings.store_recent_configuration(f"file_{i}")
            configs = self._settings.get_recent_configurations()
            self.fail_if(len(configs) != i + 1,
                         f"Expected {i + 1} configurations, have {len(configs)}")
            self.log.debug(configs)
        self.log.debug("Add extra")
        while i < 12:
            i += 1
            self._settings.store_recent_configuration(f"file_{i}")
            configs = self._settings.get_recent_configurations()
            self.fail_if(len(configs) != self._settings.MAX_RECENT_CONFIGS,
                         f"Expected {self._settings.MAX_RECENT_CONFIGS} configurations, "
                         f"have {len(configs)}")
            self.log.debug(configs)
        self.log.debug("Add existing one")
        filename = configs[2]
        self._settings.store_recent_configuration(filename)
        configs = self._settings.get_recent_configurations()
        self.log.debug(configs)
        self.fail_if(configs.count(filename) > 1, "filename more than one time in the list")
        filename = configs[2]
        self.log.debug(f"Remove {filename}")
        self._settings.remove_recent_configuration(filename)
        configs = self._settings.get_recent_configurations()
        self.log.debug(configs)
        self.fail_if(filename in configs, "Recent configuration was not removed")


if __name__ == "__main__":

    ApplicationSettingsTest().run()
