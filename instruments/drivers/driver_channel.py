"""
Driver channel object.
"""

import re


class DriverChannel:

    DIR_INPUT = "input"
    DIR_OUTPUT = "output"

    def __init__(self, channel_id, name, expect_response=True):
        assert isinstance(channel_id, str), "The channel ID must be a string"
        assert channel_id != "", "The channel ID cannot be empty"
        assert re.fullmatch(r"[a-zA-Z0-9_-]+", channel_id) is not None, \
            "The channel ID must be alphanumeric and can contain underscores and hyphens"
        assert isinstance(name, str), "The channel name must be a string"
        assert name != "", "The channel name cannot be empty"
        assert name.startswith("get ") or name.startswith("set "), \
            "The channel name must start with 'get' or 'set'"
        assert isinstance(expect_response, bool), "The expect_response must be a boolean"

        self.channel_id = channel_id
        self.name = name
        self.expect_response = expect_response
        self.direction = self.DIR_INPUT if name.startswith("get ") else self.DIR_OUTPUT
