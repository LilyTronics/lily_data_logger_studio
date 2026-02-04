"""
Run the data logger.
"""

import src.app_data as AppData

from src.controllers.controller_main import MainController


def run_data_logger():
    MainController(f"{AppData.APP_NAME} V{AppData.VERSION}")
    AppData.wxApp.MainLoop()


if __name__ == "__main__":

    run_data_logger()
