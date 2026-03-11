"""
Test for imports
"""

import os

import src.app_data as AppData

from tests.lib.test_suite import TestSuite


class ImportTest(TestSuite):

    _IGNORE_FOLDERS = [
        os.path.join(AppData.APP_PATH, ".venv"),
        os.path.join(AppData.APP_PATH, "build", "build_output"),
        os.path.join(AppData.APP_PATH, "temp")
    ]

    # from query... import, import query...

    _INSTRUMENTS_IMPORTS = [
        " instruments"
    ]

    _SOURCE_IMPORTS = [
        " build",
        " src",
        " tests"
    ]

    def test_import_instruments(self):
        # We are not allowed to directly import from the instruments package.
        # The driver model must be used for that.
        for current_path, sub_folders, filenames in os.walk(AppData.APP_PATH):
            ignore = False
            for path in self._IGNORE_FOLDERS:
                if current_path.startswith(path):
                    ignore = True
                    break
            if ignore:
                continue

            sub_folders.sort()
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                full_path = os.path.join(current_path, filename)
                self.log.debug(f"Check file: {full_path}")
                lines = []
                with open(full_path, "r", encoding="utf-8") as fp:
                    for line in fp.readlines():
                        if line.strip().startswith("if __name__ == \"__main__\""):
                            break
                        if line.strip().startswith("from ") or line.strip().startswith("import "):
                            lines.append(line.strip())

                queries = self._INSTRUMENTS_IMPORTS
                if current_path.startswith(os.path.join(AppData.APP_PATH, "instruments")):
                    queries = self._SOURCE_IMPORTS

                for line in lines:
                    for query in queries:
                        self.fail_if(query in line, f"Found illegal import: {line}")


if __name__ == "__main__":

    ImportTest().run(True)
