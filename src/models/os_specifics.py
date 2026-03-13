"""
OS Specifics.
"""

import os
import sys

from pathlib import Path


def get_user_data_dir():
    extend_path = []
    if sys.platform == "win32":
        extend_path = ["AppData", "Roaming"]
    elif sys.platform == "darwin":
        extend_path = ["Library", "Application Support"]
    else:  # Linux and others
        extend_path = [".local", "share"]
    return os.path.join(Path.home(), *extend_path)


if __name__ =="__main__":
    print("User data dir:", get_user_data_dir())
