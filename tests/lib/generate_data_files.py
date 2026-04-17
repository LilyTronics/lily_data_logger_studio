"""
Generate data files with test run data.
"""

import os
import random
import time

import src.app_data as AppData

from src.models.configuration import Configuration
from src.models.test_runs import TestRuns


def create_data_file(configuration, t_start, n_samples):
    measurements = configuration.get_measurements()

    TestRuns.clear()
    run_id = TestRuns.new_test_run(measurements)

    print("Generate test run")
    t = t_start
    for _ in range(n_samples):
        TestRuns.init_cycle(run_id, t)
        for m in measurements:
            value = round(random.uniform(25, 30), 1)
            TestRuns.store_measurement(run_id, t, m["id"], value)
        t += 3
    export_filename = os.path.join(AppData.TEST_CONFIG_PATH, f"test_run_{n_samples}.sqlite")
    print("Export to file")
    TestRuns.export_test_runs(
        [TestRuns.get_test_run(run_id)],
        export_filename
    )
    return t


if __name__ == "__main__":

    config = Configuration()
    config.load(os.path.join(AppData.TEST_CONFIG_PATH, "manual_test.json"))

    start_time = time.time()
    for n in (1000, 5000, 10000, 20000):
        start = time.time()
        print(f"Generate data file with {n} samples")
        start_time = create_data_file(config, start_time, n)
        print(f"{time.time() - start}")
