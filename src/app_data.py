"""
Application data.
"""

import os
import wx


wxApp = wx.App(redirect=False)

APP_NAME = "Lily Data Logger Studio\u2122"   # \u2122 is the trademark symbol
VERSION = "0.1"
EXE_NAME = "LilyDataLoggerStudio"

wxApp.SetAppName(EXE_NAME)
_sp = wx.StandardPaths.Get()

SETTINGS_FILE = os.path.join(_sp.GetUserDataDir(), f"{EXE_NAME}.json")
APP_LOG_FILE = os.path.join(_sp.GetUserDataDir(), f"{EXE_NAME}.log")


if __name__ == "__main__":

    print(f"{APP_NAME} V{VERSION}")
    print("Settings file:", SETTINGS_FILE)
    print("App log file:", APP_LOG_FILE)
