"""
Runs all the unit tests
"""

import sys

from tests.unit_tests.run_test_runner import run_test_runner

if not run_test_runner("./unit_tests"):
    sys.exit(1)
