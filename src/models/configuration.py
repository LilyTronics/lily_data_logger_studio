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

    _STEP = {
        "name": "",
        "label": "",
        "type": "",
        "settings" : {}
    }

    _GRAPH = {
        "name": "",
        "measurements": [],
        "settings": {}
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
        elif main_group in ["instruments", "measurements", "graphs"]:
            for item in collection:
                sub_items.append(item["name"])
        elif main_group == "process":
            if len(collection) > 0:
                sub_items.append(f"process: {len(collection)} steps")
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

    def get_new_process_step(self):
        return deepcopy(self._STEP)

    def get_process_steps(self):
        return deepcopy(self._configuration["process"])

    def get_process_step(self, step_index):
        step = None
        if 0 <= step_index < len(self._configuration["process"]):
            step =  self._configuration["process"][step_index]
        return deepcopy(step)

    def get_process_step_index_for_label(self, label):
        return next(
            (i for i, d in enumerate(self._configuration["process"])
                if label != "" and d["label"] == label),
            -1
        )

    def add_process_step(self, name, label, step_type, settings, position=-1):
        if self.get_process_step_index_for_label(label) >= 0:
            raise Exception("A step with this label already exists")
        step = deepcopy(self._STEP)
        step["name"] = name
        step["label"] = label
        step["type"] = step_type
        step["settings"] = deepcopy(settings)
        if position >= 0:
            self._configuration["process"].insert(position, step)
        else:
            self._configuration["process"].append(step)

    def update_process_step(self, step_index, name, label, step_type, settings):
        if step_index < 0 or step_index >= len(self._configuration["process"]):
            raise Exception("The step index is invalid")
        same_label = self.get_process_step_index_for_label(label)
        if same_label >= 0 and same_label != step_index:
            raise Exception("A step with this label already exists")
        self._configuration["process"][step_index]["name"] = name
        self._configuration["process"][step_index]["label"] = label
        self._configuration["process"][step_index]["type"] = step_type
        self._configuration["process"][step_index]["settings"] = settings

    def move_process_step(self, step_index, direction):
        if ((step_index == 0 and direction < 0) or
            (step_index >= len(self._configuration["process"]) - 1 and direction > 0)):
            return
        new_index = step_index
        if direction > 0:
            new_index = step_index + 1
        elif direction < 0:
            new_index = step_index - 1
        else:
            raise Exception("Invalid value for direction")
        self._configuration["process"].insert(
            new_index, self._configuration["process"].pop(step_index)
        )

    def delete_process_step(self, step_index):
        if step_index < 0 or step_index >= len(self._configuration["process"]):
            raise Exception("The step index is invalid")
        self._configuration["process"].pop(step_index)

    ##########
    # Graphs #
    ##########

    def get_new_graph(self):
        return deepcopy(self._GRAPH)

    def get_graphs(self):
        return deepcopy(self._configuration["graphs"])

    def get_graph_by_name(self, name):
        matches = [x for x in self._configuration["graphs"] if x["name"] == name]
        return None if len(matches) != 1 else matches[0]

    def get_graph_index_for_name(self, name):
        return next(
            (i for i, d in enumerate(self._configuration["graphs"])
                if name != "" and d["name"] == name),
            -1
        )

    def add_graph(self, name, measurements, settings):
        if self.get_graph_by_name(name) is not None:
            raise Exception("A graph with this name already exists")
        graph = deepcopy(self._GRAPH)
        graph["name"] = name
        graph["measurements"] = measurements
        graph["settings"] = settings
        self._configuration["graphs"].append(graph)

    def update_graph(self, graph_index, name, measurements, settings):
        if graph_index < 0 or graph_index >= len(self._configuration["graphs"]):
            raise Exception("The graph index is invalid")
        same_name = self.get_graph_index_for_name(name)
        print(same_name, graph_index)
        if same_name >= 0 and same_name != graph_index:
            raise Exception("A graph with this name already exists")
        self._configuration["graphs"][graph_index]["name"] = name
        self._configuration["graphs"][graph_index]["measurements"] = measurements
        self._configuration["graphs"][graph_index]["settings"] = settings

    def move_graph(self, graph_index, direction):
        if ((graph_index == 0 and direction < 0) or
            (graph_index >= len(self._configuration["graphs"]) - 1 and direction > 0)):
            return
        new_index = graph_index
        if direction > 0:
            new_index = graph_index + 1
        elif direction < 0:
            new_index = graph_index - 1
        else:
            raise Exception("Invalid value for direction")
        self._configuration["graphs"].insert(
            new_index, self._configuration["graphs"].pop(graph_index)
        )

    def delete_graph(self, graph_index):
        if graph_index < 0 or graph_index >= len(self._configuration["graphs"]):
            raise Exception("The graph index is invalid")
        self._configuration["graphs"].pop(graph_index)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.configuration_test import ConfigurationTest

    ConfigurationTest().run()
