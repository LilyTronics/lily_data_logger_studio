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


if __name__ == "__main__":

    ApplicationSettingsTest().run(True)
