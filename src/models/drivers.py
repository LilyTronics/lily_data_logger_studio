"""
Provide access to the instrument drivers.
"""

import inspect
import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData


class Drivers:

    _drivers = []

    @classmethod
    def load(cls, progress_callback):
        driver_files = []
        progress_callback(-1, f"Load drivers from: {AppData.DRIVERS_PATH}")
        for current_path, subfolders, filenames in os.walk(AppData.DRIVERS_PATH):
            subfolders.sort()
            for filename in filenames:
                if filename == "driver_base.py" or filename.startswith("_"):
                    continue
                full_path = os.path.join(current_path, filename)
                if filename.endswith(".py"):
                    driver_files.append(full_path)
        total = len(driver_files)
        progress_callback(-1, f"Load {total} drivers", total)
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


if __name__ == "__main__":

    from tests.unit_tests.model_tests.drivers_test import DriversTest

    DriversTest().run(True)
