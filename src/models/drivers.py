"""
Provide access to the instrument drivers.
"""

import inspect
import os
import threading

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData


class Drivers:

    _drivers = []
    _lock = threading.Lock()

    _EXCLUDED_FILES = [ "driver_base", "driver_channel", "driver_id", "driver_settings"]

    def __init__(self):
        raise Exception("This class should not be instantiated")

    # Dummy callback in case the progress callback is None
    @staticmethod
    def _callback(*params):
        pass

    @classmethod
    def load(cls, progress_callback=None):
        if progress_callback is None:
            progress_callback = cls._callback
        with cls._lock:
            del cls._drivers[:]
            driver_files = []
            progress_callback(-1, f"Load drivers from: {AppData.DRIVERS_PATH}")
            for current_path, subfolders, filenames in os.walk(AppData.DRIVERS_PATH):
                if "__pycache__" in current_path:
                    continue
                subfolders.sort()
                for filename in filenames:
                    if (os.path.splitext(filename)[0] in cls._EXCLUDED_FILES or
                        filename.startswith("_")):
                        continue
                    full_path = os.path.join(current_path, filename)
                    if filename.endswith(".py") or filename.endswith(".pyc"):
                        driver_files.append(full_path)
            total = len(driver_files)
            progress_callback(-1, f"Load {total} drivers", total)
            i = 0
            for i, filename in enumerate(driver_files):
                rel_path = filename[len(AppData.INSTRUMENTS_PATH) + 1:]
                progress_callback(i, f"Load driver from: {rel_path} ({i + 1}/{total})")
                name = os.path.basename(filename).split(".")[0]
                spec = spec_from_file_location(name, str(filename))
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if inspect.isclass(attribute):
                        classes = [x.__name__ for x in inspect.getmro(attribute)]
                        if "DriverBase" in classes:
                            classes.remove("object")
                            classes.remove("DriverBase")
                            if "ABC" in classes:
                                classes.remove("ABC")
                            if len(classes) > 0:
                                cls._drivers.append(attribute)
            progress_callback(i, f"Drivers loaded ({i + 1}/{total})")

    @classmethod
    def get_drivers(cls):
        return cls._drivers

    @classmethod
    def get_settings(cls, query):
        driver = cls.get_driver(query)
        if driver is None:
            raise Exception(f"No driver matching '{query}'")
        return driver.driver_settings

    @classmethod
    def get_driver(cls, query):
        # Query can be ID, class name or driver name
        # Prio is ID
        matches = [x for x in cls._drivers if x.id == query]
        if len(matches) == 0:
            # Next search class name
            matches = [x for x in cls._drivers if x.get_class_name() == query]
        if len(matches) == 0:
            # Next search driver name
            matches = [x for x in cls._drivers if x.name == query]
        return None if len(matches) != 1 else matches[0]


if __name__ == "__main__":

    from tests.unit_tests.model_tests.drivers_test import DriversTest

    DriversTest().run()
