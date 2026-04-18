"""
Handles CSV and TSV export.
"""

import csv
import os

from src.models.time_converter import TimeConverter

class CtsvHandler:

    @classmethod
    def export_test_runs(cls, data_filename, test_runs):
        # Each test run is stored in a separate file with the index and start time in the name.
        for i, test_run in enumerate(test_runs):
            start = test_run["timestamps"][0]
            # Split file in extension and rest
            filename, ext = os.path.splitext(data_filename)
            filename += f"_{TimeConverter.get_time_string(start, True)}_{i + 1}{ext}"
            delimiter = "\t" if ext == ".tsv" else ","
            # Add timestamps
            records = []
            for timestamp in test_run["timestamps"]:
                # Add timestamp as absolute date and time and as relative time in seconds
                records.append({
                    "Timestamp": TimeConverter.get_time_string(timestamp),
                    "Time [s]": timestamp - start
                })
            # Add measurements
            for measurement in test_run["measurements"]:
                col_name = f"{measurement["name"]} [{measurement["unit"]}]"
                for i, value in enumerate(measurement["values"]):
                    records[i][col_name] = value
            # Export data
            with open(filename, "w", newline="", encoding="utf-8") as fp:
                writer = csv.DictWriter(
                    fp,
                    fieldnames=records[0].keys(),
                    delimiter=delimiter
                )
                writer.writeheader()
                writer.writerows(records)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run(True)
