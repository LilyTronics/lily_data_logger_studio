"""
Run the data logger.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_main import ControllerMain
from src.models.logger import Logger
from src.models.os_specifics import get_platform_info
from src.models.os_specifics import is_valid_display_session
from src.models.test_options import TestOptions


def run_data_logger(options=TestOptions):
    valid = "valid" if is_valid_display_session() else "not valid"
    log = Logger(AppData.APP_LOG_FILE, options.log_to_stdout)
    log.info(f"Start application: {AppData.APP_NAME} V{AppData.VERSION}")
    log.info(f"Running on: {get_platform_info()} ({valid})")
    log.info(f"Application path: {AppData.APP_PATH}")
    log.info(f"Instruments path: {AppData.INSTRUMENTS_PATH}")

    app = wx.App(redirect=False)
    app.SetAppName(AppData.EXE_NAME)
    ControllerMain(f"{AppData.APP_NAME} V{AppData.VERSION}", log)
    app.MainLoop()

    log.info("Application terminated")
    log.shut_down()


if __name__ == "__main__":

    run_data_logger()
