"""
Storage for the test runs.
"""

import uuid

from copy import deepcopy


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
    def get_test_run(cls, run_id):
        matches = [x for x in cls._TEST_RUNS if x["id"] == run_id]
        return None if len(matches) != 1 else deepcopy(matches[0])

    @classmethod
    def new_test_run(cls, measurements):
        test_run = deepcopy(cls._TEST_RUN)
        test_run["id"] = uuid.uuid4()
        for measurement in measurements:
            m = deepcopy(cls._MEASUREMENT)
            m["id"] = measurement["id"]
            m["name"] = measurement["name"]
            m["unit"] = measurement["unit"]
            test_run["measurements"].append(m)
        cls._TEST_RUNS.append(test_run)
        return test_run["id"]

    @classmethod
    def add_measurement_value(cls, run_id, timestamp, measurement_id, value):
        test_run = cls._get_test_run_ref(run_id)
        if test_run is None:
            return
        test_run["timestamps"].append(timestamp)
        matches = [x for x in test_run["measurements"] if x["id"] == measurement_id]
        if len(matches) != 1:
            return
        matches[0]["values"].append(value)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run()
