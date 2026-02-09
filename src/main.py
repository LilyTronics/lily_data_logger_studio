"""
Run the data logger.
"""

import src.app_data as AppData

from src.controllers.controller_main import MainController
from src.models.logger import Logger
from src.models.test_options import TestOptions


def run_data_logger(options=TestOptions):
    log = Logger(options.log_to_stdout)
    log.info("Start application")
    MainController(f"{AppData.APP_NAME} V{AppData.VERSION}", log)
    AppData.wxApp.MainLoop()
    log.info("Application terminated")
    log.shut_down()


if __name__ == "__main__":

    run_data_logger()
