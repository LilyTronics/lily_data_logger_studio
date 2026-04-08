"""
Application data.
"""

import os
import sys

from src.models.os_specifics import get_user_data_dir


APP_NAME = "Lily Data Logger Studio\u2122"   # \u2122 is the trademark symbol
VERSION = "0.10"
EXE_NAME = "LilyDataLoggerStudio"
COMPANY = "LilyTronics"
DRIVER_TEST_APP_NAME = "Lily Data Logger Studio\u2122 Driver Test"
DRIVER_TEST_EXE_NAME = "LilyDataLoggerStudioDriverTest"


# Application path depends on if run from script or from the executable
if EXE_NAME in sys.executable:
    APP_PATH = os.path.dirname(sys.executable)
    # We must add the application path for import instruments in the executable
    sys.path.insert(0, str(APP_PATH))
else:
    APP_PATH = os.path.dirname(os.path.dirname(__file__))

INSTRUMENTS_PATH = os.path.join(APP_PATH, "instruments")
DRIVERS_PATH = os.path.join(INSTRUMENTS_PATH, "drivers")
MANUALS_PATH = os.path.join(APP_PATH, "manuals")
SETTINGS_FILE = os.path.join(get_user_data_dir(), EXE_NAME, f"{EXE_NAME}.json")
APP_LOG_FILE = os.path.join(get_user_data_dir(), EXE_NAME, f"{EXE_NAME}.log")
DRIVER_TEST_LOG_FILE = os.path.join(get_user_data_dir(), EXE_NAME, f"{DRIVER_TEST_EXE_NAME}.log")
TEST_CONFIG_PATH = os.path.join(APP_PATH, "tests", "configurations")
TEST_CONFIGURATION = os.path.join(TEST_CONFIG_PATH, "manual_test.json")


if __name__ == "__main__":

    print(f"{APP_NAME} V{VERSION}")
    print("App path             :", APP_PATH)
    print("Instruments path     :", INSTRUMENTS_PATH)
    print("Drivers path         :", DRIVERS_PATH)
    print("Settings file        :", SETTINGS_FILE)
    print("App log file         :", APP_LOG_FILE)
    print("Driver test log file :", DRIVER_TEST_LOG_FILE)
    print("Test config          :", TEST_CONFIGURATION)
