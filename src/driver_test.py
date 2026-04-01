"""
Application for testing the drivers.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_driver_test import ControllerDriverTest
from src.models.logger import Logger
from src.models.os_specifics import get_platform_info
from src.models.test_options import TestOptions


def run_driver_test(options=TestOptions):
    log = Logger(AppData.DRIVER_TEST_LOG_FILE, options.log_to_stdout)
    log.info(f"Start application: {AppData.DRIVER_TEST_APP_NAME} V{AppData.VERSION}")
    log.info(f"Running on: {get_platform_info()}")
    log.info(f"Application path: {AppData.APP_PATH}")
    log.info(f"Instruments path: {AppData.INSTRUMENTS_PATH}")

    app = wx.App(redirect=False)
    app.SetAppName(AppData.DRIVER_TEST_EXE_NAME)
    ControllerDriverTest(f"{AppData.DRIVER_TEST_APP_NAME} V{AppData.VERSION}", log)
    app.MainLoop()

    log.info("Application terminated")
    log.shut_down()


if __name__ == "__main__":

    run_driver_test()
