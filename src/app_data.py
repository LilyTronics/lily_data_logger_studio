"""
Application data.
"""

import os
import sys
import wx


wxApp = wx.App(redirect=False)

APP_NAME = "Lily Data Logger Studio\u2122"   # \u2122 is the trademark symbol
VERSION = "0.1"
EXE_NAME = "LilyDataLoggerStudio"
COMPANY = "LilyTronics"

wxApp.SetAppName(EXE_NAME)
_sp = wx.StandardPaths.Get()

SETTINGS_FILE = os.path.join(_sp.GetUserDataDir(), f"{EXE_NAME}.json")
APP_LOG_FILE = os.path.join(_sp.GetUserDataDir(), f"{EXE_NAME}.log")

# Application path depends on if run from script or from the executable
if EXE_NAME in sys.executable:
    APP_PATH = os.path.dirname(sys.executable)
else:
    APP_PATH = os.path.dirname(os.path.dirname(__file__))

INSTRUMENTS_PATH = os.path.join(APP_PATH, "instruments")


if __name__ == "__main__":

    print(f"{APP_NAME} V{VERSION}")
    print("Settings file:", SETTINGS_FILE)
    print("App log file:", APP_LOG_FILE)
    print("App path:", APP_PATH)
    print("Instruments path:", INSTRUMENTS_PATH)
