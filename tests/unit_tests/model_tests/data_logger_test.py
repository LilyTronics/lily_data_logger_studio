"""
Unit test for the ID managers.
"""

from src.models.configuration import Configuration
from src.models.data_logger import DataLogger
from tests.lib.test_suite import TestSuite


class DataLoggerTest(TestSuite):

    _configuration = None
    _data_logger = None
    _message = None

    def setup(self):
        self._configuration = Configuration()
        self._data_logger = DataLogger(self._configuration, self._on_status_update)

    def test_start_data_logger(self):
        self._message = None
        self.log.debug("Start data logger")
        self._data_logger.start()
        self.log.debug("Check message")
        self.fail_if(self._message is None, "No status update")
        self.fail_if(self._message["status"] != "running", "Invalid status message")

    def test_stop_data_logger(self):
        self._message = None
        self.log.debug("Stop data logger")
        self._data_logger.stop()
        self.log.debug("Check message")
        self.fail_if(self._message is None, "No status update")
        self.fail_if(self._message["status"] != "idle", "Invalid status message")

    def _on_status_update(self, data):
        self.log.debug(f"Status update: {data}")
        self._message = data


if __name__ == "__main__":

    DataLoggerTest().run(True)
