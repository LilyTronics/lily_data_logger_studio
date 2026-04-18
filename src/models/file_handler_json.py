"""
Handles JSON export and import.
"""

import json


class JsonHandler:

    @classmethod
    def export_test_runs(cls, data_filename, test_runs):
        with open(data_filename, "w", encoding="utf-8") as fp:
            json.dump(test_runs, fp, indent=2)

    @classmethod
    def import_test_runs(cls, data_filename):
        test_runs = []
        with open(data_filename, "r", encoding="utf-8") as fp:
            test_runs = json.load(fp)
        return test_runs


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run(True)
