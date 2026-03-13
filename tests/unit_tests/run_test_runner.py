"""
Generic test runner called by the unit test scripts.
"""

import os

from lily_unit_test import TestRunner


def run_test_runner(path_to_tests):
    path_to_tests = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path_to_tests))
    report_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_reports"))
    exclude_tests = ["TestSuite"]

    if not os.path.isdir(report_folder):
        os.makedirs(report_folder)

    print("\nStarting test runner")
    print(f"Run tests in: {path_to_tests}")
    options = {
        "report_folder": report_folder,
        "create_html_report": True,
        "open_in_browser": True,
        "no_log_files": True,
        "exclude_test_suites": exclude_tests
    }
    return TestRunner.run(path_to_tests, options)


if __name__ == "__main__":

    run_test_runner("./unit_tests")

