"""
Driver channel object.
"""

class DriverChannel:

    DIR_INPUT = "input"
    DIR_OUTPUT = "output"

    def __init__(self, name, expect_response=True):
        assert isinstance(name, str), "The channel name must be a string"
        assert name != "", "The channel name cannot be empty"
        assert name.startswith("get ") or name.startswith("set "), \
            "The channel name must start with 'get' or 'set'"
        assert isinstance(expect_response, bool), "The expect_response must be a boolean"

        self.name = name
        self.expect_response = expect_response
        self.direction = self.DIR_INPUT if name.startswith("get ") else self.DIR_OUTPUT
