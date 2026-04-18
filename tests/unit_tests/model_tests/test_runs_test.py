"""
Unit test for the test runs model.
"""

import os
import random
import time

import src.app_data as AppData

from src.models.configuration import Configuration
from src.models.test_runs import TestRuns
from tests.lib.test_suite import TestSuite


class TestRunsTest(TestSuite):

    run_id = None
    config = Configuration()
    data_filenames = []

    def setup(self):
        self.config.load(AppData.TEST_CONFIGURATION)

    def teardown(self):
        for filename in self.data_filenames:
            if os.path.isfile(filename):
                os.remove(filename)
        # Remove any CSV or TSV files
        for item in os.listdir("."):
            if item.endswith(".csv") or item.endswith(".tsv"):
                os.remove(item)

    def add_test_run(self, start_time):
        measurements = self.config.get_measurements()
        self.run_id = TestRuns.new_test_run(measurements)
        self.log.debug(f"Test run ID: {self.run_id}")
        t = start_time
        for _ in range(10):
            self.log.debug("Initialize cycle")
            TestRuns.init_cycle(self.run_id, t)
            test_run = TestRuns.get_test_run(self.run_id)
            self.fail_if(test_run["timestamps"][-1] != t, "Sample time not added")
            for m in test_run["measurements"]:
                self.fail_if(m["values"][-1] is not None, "Value is not initialized")
            self.log.debug("Add measurements")
            for m in measurements:
                value = round(random.uniform(25, 30), 1)
                self.log.debug(f"Add value: {t}: {value}")
                TestRuns.store_measurement(self.run_id, t, m["id"], value)
            t += 3
        test_run = TestRuns.get_test_run(self.run_id)
        self.fail_if(len(test_run["timestamps"]) != 10, "Timestampes were not added")
        for m in measurements:
            matches = [x for x in test_run["measurements"] if x["id"] == m["id"]]
            self.fail_if(len(matches) != 1, "Measurement not in test runs")
            self.fail_if(len(matches[0]["values"]) != 10, "Values were not added")
        return t

    def export_import_test_runs(self, filename):
        self.data_filenames.append(filename)
        self.log.debug("Create test runs")
        TestRuns.clear()
        start_time = int(time.time())
        while len(TestRuns.get_test_runs()) < 2:
            start_time = self.add_test_run(start_time)
        test_runs = TestRuns.get_test_runs()
        n_test_runs = len(test_runs)
        self.fail_if(n_test_runs < 2, "There must be at least two test runs")
        self.log.debug(f"Export test runs to: {filename}")
        TestRuns.export_test_runs(test_runs, filename)
        # We can only import from SQLite or JSON
        if filename.endswith(".sqlite") or filename.endswith(".json"):
            self.log.debug(f"Import test run from: {filename}")
            TestRuns.import_test_runs(filename)
            test_runs = TestRuns.get_test_runs()
            self.fail_if(len(test_runs) != n_test_runs + 2, "Test runs were not imported")
            # Check if test runs are equal
            for i, run_i in enumerate(test_runs):
                for _, run_j in enumerate(test_runs[i + 1:], start=i + 1):
                    self.fail_if(run_i["id"] == run_j["id"], "The IDs are the same")
            # Remove ID, or else the compare will not work
            for run in test_runs:
                run["id"] = ""
            # Check for equal 0 and 1 must match with 2 and 3
            # But we not sure if 0 matches with 2 or 3 and 1 matches with 2 or 3
            matches = []
            for i in range(2):
                for j in range(2, 4):
                    if test_runs[i] == test_runs[j]:
                        matches.append((i, j))
            self.fail_if(len(matches) != 2, "Data is not the same")
            self.fail_if(matches[0] not in [(0, 2), (0, 3)], "Data is not the same")
            self.fail_if(matches[1] not in [(1, 2), (1, 3)], "Data is not the same")

    def test_export_import_sqlite(self):
        self.export_import_test_runs("data_file.sqlite")

    def test_export_import_json(self):
        self.export_import_test_runs("data_file.json")

    def test_export_to_csv(self):
        self.export_import_test_runs("data_file.csv")

    def test_export_to_tsv(self):
        self.export_import_test_runs("data_file.tsv")

    def test_delete_test_run(self):
        test_runs = TestRuns.get_test_runs()
        n_test_runs = len(test_runs)
        self.fail_if(n_test_runs == 0, "No test runs available")
        TestRuns.delete(test_runs[0]["id"])
        test_runs = TestRuns.get_test_runs()
        self.fail_if(len(test_runs) != n_test_runs - 1, "Test run was not deleted")


if __name__ == "__main__":

    TestRunsTest().run()
