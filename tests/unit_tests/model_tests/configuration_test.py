"""
Unit test for the configuration.
"""

from src.models.configuration import Configuration
from tests.lib.test_suite import TestSuite


class ConfigurationTest(TestSuite):

    _EXPECTED_GROUPS = ["settings", "instruments", "process", "measurements", "graphs"]
    _configuration = Configuration()

    def test_default_config(self):
        groups = self._configuration.get_main_groups()
        self.log.debug(f"Main groups: {groups}")
        self.fail_if(list(groups) != self._EXPECTED_GROUPS,
                     f"Invalid main groups. Expected: {self._EXPECTED_GROUPS}")
        for group in groups:
            sub_items = self._configuration.get_sub_items(group)
            self.log.debug(f"Sub items for group '{group}': {sub_items}")


if __name__ == "__main__":

    ConfigurationTest().run(True)
