"""
Storage for the test runs.
"""

import uuid

from copy import deepcopy

from src.models.file_handler_ctsv import CtsvHandler
from src.models.file_handler_json import JsonHandler
from src.models.file_handler_sqlite import SQLiteHandler


class TestRuns:

    _TEST_RUNS = []

    _TEST_RUN = {
        "id": "",
        "timestamps": [],
        "measurements": []
    }

    _MEASUREMENT = {
        "id": "",
        "name": "",
        "unit": "",
        "values": []
    }

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ###########
    # Private #
    ###########

    @classmethod
    def _get_test_run_ref(cls, run_id):
        matches = [x for x in cls._TEST_RUNS if x["id"] == run_id]
        return None if len(matches) != 1 else matches[0]

    ##########
    # Public #
    ##########

    @classmethod
    def clear(cls):
        del cls._TEST_RUNS[:]

    @classmethod
    def get_test_runs(cls):
        return deepcopy(cls._TEST_RUNS)

    @classmethod
    def get_test_run(cls, run_id):
        matches = [x for x in cls._TEST_RUNS if x["id"] == run_id]
        return None if len(matches) != 1 else deepcopy(matches[0])

    @classmethod
    def new_test_run(cls, measurements):
        test_run = deepcopy(cls._TEST_RUN)
        test_run["id"] = str(uuid.uuid4())
        for measurement in measurements:
            m = deepcopy(cls._MEASUREMENT)
            m["id"] = measurement["id"]
            m["name"] = measurement["name"]
            m["unit"] = measurement["unit"]
            test_run["measurements"].append(m)
        cls._TEST_RUNS.append(test_run)
        return test_run["id"]

    @classmethod
    def init_cycle(cls, run_id, timestamp):
        test_run = cls._get_test_run_ref(run_id)
        test_run["timestamps"].append(timestamp)
        for measurement in test_run["measurements"]:
            measurement["values"].append(None)

    @classmethod
    def store_measurement(cls, run_id, timestamp, measurement_id, value):
        test_run = cls._get_test_run_ref(run_id)
        index = test_run["timestamps"].index(timestamp)
        matches = [x for x in test_run["measurements"] if x["id"] == measurement_id]
        if len(matches) == 1:
            if index < len(matches[0]["values"]):
                matches[0]["values"][index] = value

    @classmethod
    def delete(cls, run_id):
        index = next(
            (i for i, d in enumerate(cls._TEST_RUNS)
                if d["id"] == run_id),
            -1
        )
        if 0 <= index < len(cls._TEST_RUNS):
            cls._TEST_RUNS.pop(index)

    @classmethod
    def export_test_runs(cls, test_runs, data_filename):
        if data_filename.endswith(".sqlite"):
            SQLiteHandler.export_test_runs(data_filename, test_runs)
        elif data_filename.endswith(".json"):
            JsonHandler.export_test_runs(data_filename, test_runs)
        elif data_filename.endswith(".csv") or data_filename.endswith(".tsv"):
            CtsvHandler.export_test_runs(data_filename, test_runs)

    @classmethod
    def import_test_runs(cls, data_filename):
        test_runs = []
        if data_filename.endswith(".sqlite"):
            test_runs = SQLiteHandler.import_test_runs(data_filename)
        elif data_filename.endswith(".json"):
            test_runs = JsonHandler.import_test_runs(data_filename)
        for test_run in test_runs:
            # Make sure we have unique IDs
            test_run["id"] = str(uuid.uuid4())
            cls._TEST_RUNS.append(test_run)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run()
