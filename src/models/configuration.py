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
import uuid

from copy import deepcopy

from src.models.time_converter import TimeConverter


class Configuration:

    _NO_FILENAME = "<new configuration>"

    _DEFAULT_CONFIGURATION = {
        "settings": {
            "sample_time": 3,
            "end_time": 60,
            "continuous_mode": False
        },
        "instruments": [],
        "measurements": [],
        "process": [],
        "graphs": []
    }

    _INSTRUMENT = {
        "id": "",
        "name": "",
        "driver_id": "",
        "settings": {}
    }

    _MEASUREMENT = {
        "id": "",
        "name": "",
        "instrument_id": "",
        "channel_id": "",
        "unit": "",
        "gain": 1.0,
        "offset": 0.0
    }

    def __init__(self):
        self._filename = None
        self._configuration = deepcopy(self._DEFAULT_CONFIGURATION)
        self._is_changed = False

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

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())

    def _get_index_of_instrument(self, instrument_id):
        for i in range(len(self._configuration["instruments"])):
            if self._configuration["instruments"][i]["id"] == instrument_id:
                return i
        raise Exception("No instrument found for this ID")

    def _get_index_of_measurement(self, measurement_id):
        for i in range(len(self._configuration["measurements"])):
            if self._configuration["measurements"][i]["id"] == measurement_id:
                return i
        raise Exception("No measurement found for this ID")

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
        self._is_changed = False
        self._filename = filename

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(self._configuration, fp, indent=2)
        self._filename = filename
        self._is_changed = False

    def is_changed(self):
        return self._is_changed

    def get_main_groups(self):
        return self._DEFAULT_CONFIGURATION.keys()

    def get_sub_items(self, main_group):
        sub_items = []
        collection = self._configuration[main_group]
        if main_group == "settings":
            for key in collection:
                value = collection[key]
                if key.endswith("_time"):
                    value = TimeConverter.create_duration_time_string(value)
                if isinstance(value, bool):
                    value = "yes" if value else "no"
                key = key.replace("_", " ")
                sub_items.append(f"{key}: {value}")
        elif main_group in ["instruments", "measurements"]:
            for item in collection:
                sub_items.append(item["name"])

        return sub_items

    ############
    # Settings #
    ############

    def get_settings(self):
        return deepcopy(self._configuration["settings"])

    def update_settings(self, settings):
        self._configuration["settings"] = deepcopy(settings)
        self._is_changed = True

    ###############
    # Instruments #
    ###############

    def get_new_instrument(self):
        return deepcopy(self._INSTRUMENT)

    def get_instruments(self):
        return deepcopy(self._configuration["instruments"])

    def get_instrument(self, query):
        # Query can be name or ID. Prio = ID
        matches = [x for x in self.get_instruments() if x["id"] == query]
        if len(matches) == 0:
            matches = [x for x in self.get_instruments() if x["name"] == query]
        return None if len(matches) != 1 else deepcopy(matches[0])

    def add_instrument(self, name, driver_id, settings):
        if self.get_instrument(name) is not None:
            raise Exception("An instrument with this name already exists")
        instrument = deepcopy(self._INSTRUMENT)
        instrument["id"] = self._generate_id()
        instrument["name"] = name
        instrument["driver_id"] = driver_id
        instrument["settings"] = deepcopy(settings)
        self._configuration["instruments"].append(instrument)

    def update_instrument(self, instrument_id, name, driver_id, settings):
        i = self._get_index_of_instrument(instrument_id)
        instrument = self.get_instrument(name)
        if instrument is not None and instrument["id"] != instrument_id:
            raise Exception("An instrument with this name already exists")
        self._configuration["instruments"][i]["name"] = name
        self._configuration["instruments"][i]["driver_id"] = driver_id
        self._configuration["instruments"][i]["settings"] = settings

    def delete_instrument(self, instrument_id):
        i = self._get_index_of_instrument(instrument_id)
        self._configuration["instruments"].pop(i)

    ################
    # Measurements #
    ################

    def get_new_measurement(self):
        return deepcopy(self._MEASUREMENT)

    def get_measurements(self):
        return deepcopy(self._configuration["measurements"])

    def get_measurement(self, query):
        # Query can be name or ID. Prio = ID
        matches = [x for x in self.get_measurements() if x["id"] == query]
        if len(matches) == 0:
            matches = [x for x in self.get_measurements() if x["name"] == query]
        return None if len(matches) != 1 else deepcopy(matches[0])

    def add_measurement(self, name, instrument_id, channel_id, unit, gain, offset):
        if self.get_measurement(name) is not None:
            raise Exception("A measurement with this name already exists")
        measurement = deepcopy(self._MEASUREMENT)
        measurement["id"] = self._generate_id()
        measurement["name"] = name
        measurement["instrument_id"] = instrument_id
        measurement["channel_id"] = channel_id
        measurement["unit"] = unit
        measurement["gain"] = gain
        measurement["offset"] = offset
        self._configuration["measurements"].append(measurement)

    def update_measurement(self, measurement_id, name, instrument_id, channel_id, unit, gain,
                           offset):
        i = self._get_index_of_measurement(measurement_id)
        measurement = self.get_measurement(name)
        if measurement is not None and measurement["id"] != measurement_id:
            raise Exception("A measurement with this name already exists")
        self._configuration["measurements"][i]["name"] = name
        self._configuration["measurements"][i]["instrument_id"] = instrument_id
        self._configuration["measurements"][i]["channel_id"] = channel_id
        self._configuration["measurements"][i]["unit"] = unit
        self._configuration["measurements"][i]["gain"] = gain
        self._configuration["measurements"][i]["offset"] = offset

    def delete_measurement(self, measurement_id):
        i = self._get_index_of_measurement(measurement_id)
        self._configuration["measurements"].pop(i)

    #################
    # Process steps #
    #################

    def get_process_steps(self):
        return deepcopy(self._configuration["process"])


if __name__ == "__main__":

    from tests.unit_tests.model_tests.configuration_test import ConfigurationTest

    ConfigurationTest().run(True)
