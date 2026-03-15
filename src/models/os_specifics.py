"""
OS Specifics.
"""

import os
import sys

from pathlib import Path


def get_user_data_dir():
    extend_path = []
    match sys.platform:
        case "win32":
            extend_path = ["AppData", "Roaming"]
        case "darwin":
            extend_path = ["Library", "Application Support"]
        case _:  # Linux and others
            extend_path = [".local", "share"]
    return os.path.join(Path.home(), *extend_path)

def get_display_session_type():
    match sys.platform:
        case "win32":
            return "Desktop Window Manager (DWM)"
        case "darwin":
            return "Cocoa"
        case _:   # Linux and others
            return (os.environ.get("XDG_SESSION_TYPE") or "Unknown display session type")

def get_platform_info():
    return f"{sys.platform}, {get_display_session_type()}"


if __name__ =="__main__":
    print("User data dir:", get_user_data_dir())
    print("Platform info:", get_platform_info())
