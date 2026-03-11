"""
Report messages from pylint.
"""

import json
import os

from io import StringIO
from pylint.lint import Run
from pylint.reporters.json_reporter import JSON2Reporter

import src.app_data as AppData

from tests.lib.test_suite import TestSuite


class TestSuiteTest(TestSuite):

    def test_pylint(self):
        targets = [
            os.path.join(AppData.APP_PATH, "src"),
        ]
        self.log.debug("Running pylint on targets:")
        for target in targets:
            self.log.debug(f"{target}")

        output = StringIO()  # Custom open stream
        Run([*targets], reporter=JSON2Reporter(output), exit=False)
        result = json.loads(output.getvalue())

        for message in result["messages"]:
            self.log.debug(f"File: {message["path"]}")
            self.log.debug(f"  - {message["message"]} ({message["symbol"]})")
            self.log.debug(f"  - line: {message["line"]}, column: {message["column"]}")

        self.log.debug(f"Pylint results:")
        for key, value in result["statistics"]["messageTypeCount"].items():
            self.log.debug(f"  - {key}: {value}")
        self.log.debug(f"  - modules: {result["statistics"]["modulesLinted"]}")
        self.log.debug(f"  - score: {result["statistics"]["score"]}")
        self.fail_if(result["statistics"]["score"] < 10.0, f"Pylint score is below 10.0")


if __name__ == "__main__":

    TestSuiteTest().run()
