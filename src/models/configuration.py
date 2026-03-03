"""
Model for storing and recalling the configuration.
Configurations contains:
- Data logging settings
- Instruments and their settings
- Process steps
- Measurements (shows in data table)
- Graphs settings
"""

import json

from copy import deepcopy


class Configuration:

    _NO_FILENAME = "<new configuration>"

    _DEFAULT_CONFIGURATION = {
        "settings": {
            "sample_time": 3,
            "end_time": 60,
            "continuous_mode": False
        },
        "instruments": [],
        "process": [],
        "measurements": [],
        "graphs": []
    }

    def __init__(self):
        self._filename = None
        self._configuration = deepcopy(self._DEFAULT_CONFIGURATION)

    ###########
    # Private #
    ###########

    def _read_configuration(self):
        d = {}
        try:
            with open(self._filename, "r", encoding="utf-8") as fp:
                d = json.load(fp)
            self._configuration = d
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    ##########
    # Public #
    ##########

    def get_filename(self):
        return self._NO_FILENAME if self._filename is None else self._filename

    def load(self, filename):
        self._filename = None
        self._configuration = deepcopy(self._DEFAULT_CONFIGURATION)
        with open(filename, "r", encoding="utf-8") as fp:
            d = json.load(fp)
        self._configuration = d
        self._filename = filename

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(self._configuration, fp, indent=2)
        self._filename = filename

    def get_main_groups(self):
        return self._configuration.keys()

    def get_sub_items(self, main_group):
        return  list(map(lambda x: x["name"],
                         filter(lambda x: isinstance(x, dict) and "name" in x,
                                self._configuration[main_group])))

    def get_settings(self):
        return deepcopy(self._configuration["settings"])

    def update_settings(self, settings):
        self._configuration["settings"] = deepcopy(settings)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.configuration_test import ConfigurationTest

    ConfigurationTest().run(True)
