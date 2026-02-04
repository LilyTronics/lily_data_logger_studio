"""
Run the data logger.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_main import MainController


def run_data_logger():
    app = wx.App(False)
    MainController(f"{AppData.APP_NAME} V{AppData.VERSION}")
    app.MainLoop()


if __name__ == "__main__":

    run_data_logger()
