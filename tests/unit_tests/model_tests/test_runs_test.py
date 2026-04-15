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
    data_filename = None

    def setup(self):
        self.config.load(AppData.TEST_CONFIGURATION)
        self.data_filename = "data_file.sqlite"

    def teardown(self):
        if os.path.isfile(self.data_filename):
            os.remove(self.data_filename)

    def test_new_test_run(self):
        self.run_id = TestRuns.new_test_run(self.config.get_measurements())
        self.log.debug(f"Test run ID: {self.run_id}")

    def test_add_measurement_values(self):
        measurements = self.config.get_measurements()
        t = int(time.time())
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

    def test_export_import_sqlite(self):
        test_runs = TestRuns.get_test_runs()
        n_test_runs = len(test_runs)
        self.fail_if(n_test_runs == 0, "No test runs available")
        self.log.debug(f"Export test run to: {self.data_filename}")
        TestRuns.export_test_run(test_runs[0]["id"], self.data_filename)
        self.log.debug(f"Import test run from: {self.data_filename}")
        TestRuns.import_test_run(self.data_filename)
        test_runs = TestRuns.get_test_runs()
        self.fail_if(len(test_runs) != n_test_runs + 1, "Test was not imported")
        # Check if test runs are equal
        org_test = test_runs[0]
        imp_test = test_runs[-1]
        # IDs should not be the same
        self.fail_if(org_test["id"] == imp_test["id"], "The IDs are the same")
        del org_test["id"]
        del imp_test["id"]
        # Now they should be the same
        self.fail_if(org_test != imp_test, "Data is not the same")

    def test_delete_test_run(self):
        test_runs = TestRuns.get_test_runs()
        n_test_runs = len(test_runs)
        self.fail_if(n_test_runs == 0, "No test runs available")
        TestRuns.delete(test_runs[0]["id"])
        test_runs = TestRuns.get_test_runs()
        self.fail_if(len(test_runs) != n_test_runs - 1, "Test run was not deleted")


if __name__ == "__main__":

    TestRunsTest().run()
