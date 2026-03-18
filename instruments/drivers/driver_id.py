"""
Each driver must have a unique driver ID.
This ID is used to idetify the driver.
This way class names and driver names can change without affecting exsiting configurations.

Run this script to generate a new driver ID.
Then coopy the generated ID to the driver class.
"""

import uuid


def generate_driver_id():
    print("New driver ID:", uuid.uuid4())


if __name__ == "__main__":

    generate_driver_id()
