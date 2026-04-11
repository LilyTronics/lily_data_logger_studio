"""
Driver channel object.
"""

import re

from instruments.drivers.driver_settings import DriverSetting


class DriverChannel:

    DIR_INPUT = "input"
    DIR_OUTPUT = "output"
    SUPPORTED_TYPES = [float, int, str]

    def __init__(self, channel_id, name, value_type, response_type,
                 expect_response=True, parameters=None):
        parameters = [] if parameters is None else parameters
        if not isinstance(channel_id, str):
            raise TypeError("(Channel) Channel ID must be a string")
        if channel_id == "":
            raise ValueError("(Channel) Channel ID cannot be empty")
        if re.fullmatch(r"[a-zA-Z0-9_-]+", channel_id)  is None:
            raise ValueError(
                "(Channel) Channel ID must be alphanumeric and may contain underscores and hyphens"
            )
        if not isinstance(name, str):
            raise TypeError("(Channel) Channel name must be a string")
        if name == "":
            raise ValueError("(Channel) Channel name cannot be empty")
        if not (name.startswith("get ") or name.startswith("set ")):
            raise ValueError(
                "(Channel) Channel name must start with 'get ' or 'set '"
            )
        if not isinstance(parameters, list):
            raise TypeError("(Channel) Parameter must be a list")
        for p in parameters:
            if not isinstance(p, DriverSetting):
                raise TypeError("(Channel) Parameters must be a list of driver setting")
        if value_type is not None and value_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"(Channel) Value type {value_type} is not supported")
        if response_type is not None and response_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"(Channel) Response type {response_type} is not supported")
        if not isinstance(expect_response, bool):
            raise TypeError("(Channel) Expect response must be a boolean")
        if response_type is None and expect_response:
            raise TypeError("(Channel) Response type must be set if expect response is true")

        self.channel_id = channel_id
        self.name = name
        self.parameters = parameters
        self.value_type = value_type
        self.response_type = response_type
        self.expect_response = expect_response
        self.direction = self.DIR_INPUT if name.startswith("get ") else self.DIR_OUTPUT


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
