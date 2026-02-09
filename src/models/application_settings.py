"""
Model for storing and recalling the application settings.
"""

import json
import os

import src.app_data as AppData


class ApplicationSettings:

    def __init__(self):
        self._filename = AppData.SETTINGS_FILE
        path = os.path.dirname(self._filename)
        if not os.path.isdir(path):
            os.makedirs(path)

    ###########
    # Private #
    ###########

    def _read_settings(self):
        d = {}
        try:
            with open(self._filename, "r", encoding="utf-8") as fp:
                d = json.load(fp)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

        return d

    def _write_settings(self, settings):
        with open(self._filename, "w", encoding="utf-8") as fp:
            json.dump(settings, fp, indent=2)

    def _get_property(self, main_key, sub_key, default=None):
        d = self._read_settings()
        return d.get(main_key, {}).get(sub_key, default)

    def _store_property(self, main_key, sub_key, value):
        d = self._read_settings()
        if main_key not in d.keys():
            d[main_key] = {}
        d[main_key][sub_key] = value
        self._write_settings(d)

    ########################
    # Main window settings #
    ########################

    def get_main_window_size(self):
        return (self._get_property("main_window", "width", -1),
                self._get_property("main_window", "height", -1))

    def store_main_window_size(self, width, height):
        self._store_property("main_window", "width", width)
        self._store_property("main_window", "height", height)

    def get_main_window_position(self):
        return (self._get_property("main_window", "left", -1),
                self._get_property("main_window", "top", -1))

    def store_main_window_position(self, left, top):
        self._store_property("main_window", "left", left)
        self._store_property("main_window", "top", top)

    def get_main_window_maximized(self):
        return self._get_property("main_window", "maximized", False)

    def store_main_window_maximized(self, is_maximized):
        self._store_property("main_window", "maximized", is_maximized)

    def get_main_window_tree_width(self):
        return self._get_property("main_window", "tree_width", -1)

    def store_main_window_tree_width(self, width):
        return self._store_property("main_window", "tree_width", width)


if __name__ == "__main__":

    def _remove_settings_file():
        # Start with no setting file
        if os.path.isfile(AppData.SETTINGS_FILE):
            os.remove(AppData.SETTINGS_FILE)

    _remove_settings_file()
    s = ApplicationSettings()

    print("Main window size")
    test_value = s.get_main_window_size()
    print("Current window size:", test_value)
    assert test_value == (-1, -1)
    new_value = (1000, 650)
    s.store_main_window_size(*new_value)
    test_value = s.get_main_window_size()
    print("New main window size:", test_value)
    assert test_value == new_value

    print("\nMain window position")
    test_value = s.get_main_window_position()
    print("Current window position:", test_value)
    assert test_value == (-1, -1)
    new_value = (50, 50)
    s.store_main_window_position(*new_value)
    test_value = s.get_main_window_position()
    print("New main window position:", test_value)
    assert test_value == new_value

    print("\nMain window maximized")
    test_value = s.get_main_window_maximized()
    print("Current window maximized:", test_value)
    assert not test_value
    new_value = not test_value
    s.store_main_window_maximized(new_value)
    test_value = s.get_main_window_maximized()
    print("New main window position:", test_value)
    assert test_value

    print("\nMain window tree width")
    test_value = s.get_main_window_tree_width()
    print("Current tree width:", test_value)
    assert test_value == -1
    new_value = 200
    s.store_main_window_tree_width(new_value)
    test_value = s.get_main_window_tree_width()
    print("New tree width:", test_value)
    assert test_value == 200

    _remove_settings_file()
