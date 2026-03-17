"""
Driver channel object.
"""

import re


class DriverChannel:

    DIR_INPUT = "input"
    DIR_OUTPUT = "output"
    SUPPORTED_TYPES = [float, int, str]

    def __init__(self, channel_id, name, parameters, response_type, expect_response=True):
        if not isinstance(channel_id, str):
            raise TypeError("Channel ID must be a string")
        if channel_id == "":
            raise ValueError("Channel ID cannot be empty")
        if re.fullmatch(r"[a-zA-Z0-9_-]+", channel_id)  is None:
            raise ValueError(
                "Channel ID must be alphanumeric and may contain underscores and hyphens"
            )
        if not isinstance(name, str):
            raise TypeError("Channel name must be a string")
        if name == "":
            raise ValueError("Channel name cannot be empty")
        if not (name.startswith("get ") or name.startswith("set ")):
            raise ValueError(
                "Channel name must start with 'get ' or 'set '"
            )
        if not isinstance(parameters, list):
            raise TypeError("Parameter must be a list")
        for p in parameters:
            if not isinstance(p, dict):
                raise TypeError("Parameters must be a list of dictionaries")
        if response_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"Value type {response_type} is not supported")
        if not isinstance(expect_response, bool):
            raise TypeError("Expect response must be a boolean")

        self.channel_id = channel_id
        self.name = name
        self.parameters = parameters
        self.response_type = response_type
        self.expect_response = expect_response
        self.direction = self.DIR_INPUT if name.startswith("get ") else self.DIR_OUTPUT


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
