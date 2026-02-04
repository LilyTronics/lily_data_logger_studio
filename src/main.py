"""
Run the data logger.
"""

import src.app_data as AppData

from src.controllers.controller_main import MainController
from src.models.logger import Logger


def run_data_logger(test_mode=False):
    log = Logger(log_to_stdout=test_mode)
    log.info("Start application")
    MainController(f"{AppData.APP_NAME} V{AppData.VERSION}", log)
    AppData.wxApp.MainLoop()
    log.info("Application terminated")
    log.shut_down()


if __name__ == "__main__":

    run_data_logger()
