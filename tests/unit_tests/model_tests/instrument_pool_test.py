"""
Unit tests for the instrument pool.
"""

import os

import src.app_data as AppData

from src.models.drivers import Drivers
from src.models.instrument_pool import InstrumentPool
from src.models.configuration import Configuration
from tests.lib.test_suite import TestSuite


class InstrumentPoolTest(TestSuite):

    config = None

    def setup(self):
        self.config = Configuration()
        self.config.load(os.path.join(AppData.TEST_CONFIG_PATH, "test_instruments.json"))
        Drivers.load()

    def test_add_instruments_from_config(self):
        InstrumentPool.clear()
        instruments = self.config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        InstrumentPool.add_instruments(instruments)
        self.fail_if(len(InstrumentPool.get_instruments()) == 0,
                     "No instruments added to the pool")

    def test_get_instrument(self):
        instruments = self.config.get_instruments()
        self.fail_if(len(instruments) == 0, "No instruments in the configuration")
        instrument = InstrumentPool.get_instrument("non_existent_id")
        self.fail_if(instrument is not None, "Should return None for non-existent ID")
        instrument = InstrumentPool.get_instrument(instruments[0]["id"])
        self.fail_if(instrument is None, "Should return the instrument for existing ID")

    def test_has_simulators(self):
        has_simulators = InstrumentPool.has_simulators()
        self.log.debug(f"Has simulators: {has_simulators}")
        # We expect simulators to be present in the test configuration
        self.fail_if(not has_simulators, "Should have simulators in the test configuration")


if __name__ == "__main__":

    InstrumentPoolTest().run()
