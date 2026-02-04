"""
Logger.
"""

import os
import sys

from datetime import datetime

import src.app_data as AppData


class Logger:

    TYPE_INFO = "INFO"
    TYPE_DEBUG = "DEBUG"
    TYPE_ERROR = "ERROR"
    TYPE_STDOUT = "STDOUT"
    TYPE_STDERR = "STDERR"

    _TIME_STAMP_FORMAT = "%Y%m%d %H:%M:%S.%f"
    _LOG_FORMAT = "{} | {:6} | {}\n"

    class _StdLogger:

        def __init__(self, logger, std_type):
            self._logger = logger
            self._type = std_type

        def write(self, message):
            self._logger.handle_message(self._type, message)

        def flush(self):
            pass

    def __init__(self, log_to_stdout=False, redirect_stdout=True):
        self._filename = AppData.APP_LOG_FILE
        path = os.path.dirname(self._filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        self._log_to_stdout = log_to_stdout
        with open(self._filename, "w", encoding="utf-8") as fp:
            fp.close()
        self._output = ""

        self._org_stdout = sys.stdout
        self._org_stderr = sys.stderr
        if redirect_stdout:
            sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
            sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    def shut_down(self):
        sys.stdout = self._org_stdout
        sys.stderr = self._org_stderr

    def info(self, message):
        self.handle_message(self.TYPE_INFO, f"{message}\n")

    def debug(self, message):
        self.handle_message(self.TYPE_DEBUG, f"{message}\n")

    def error(self, message):
        self.handle_message(self.TYPE_ERROR, f"{message}\n")

    def handle_message(self, message_type, message_text):
        timestamp = datetime.now().strftime(self._TIME_STAMP_FORMAT)[:-3]
        self._output += message_text
        while "\n" in self._output:
            index = self._output.find("\n")
            message = self._LOG_FORMAT.format(timestamp, message_type, self._output[:index])
            self._output = self._output[index + 1:]
            with open(self._filename, "a", encoding="utf-8") as fp:
                fp.write(message)
            if self._log_to_stdout:
                self._org_stdout.write(message)


if __name__ == "__main__":

    import threading
    import time


    def _remove_log_file():
        if os.path.isfile(AppData.APP_LOG_FILE):
            os.remove(AppData.APP_LOG_FILE)

    def _generate_error():
        a = 1 / 0

    _remove_log_file()

    log = Logger(True)
    log.info("This is an info message")
    log.debug("This is a debug message")
    log.error("This is an error message")
    log.info("This is a\nmulti line\nmessage")
    print("This is a standard output message")
    # Generate an error in a thread
    threading.Thread(target=_generate_error).start()
    # Give thread some time
    time.sleep(0.5)

    log.shut_down()

    with open(AppData.APP_LOG_FILE, "r") as fp:
        content = fp.read()
    print("\nLog file content:")
    print(content)

    _remove_log_file()
