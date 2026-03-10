"""
Driver channel object.
"""

import re


class DriverChannel:

    DIR_INPUT = "input"
    DIR_OUTPUT = "output"

    def __init__(self, channel_id, name, expect_response=True):
        if not isinstance(channel_id, str):
            raise TypeError("Channel ID must be a string")
        if not channel_id:
            raise ValueError("Channel ID cannot be empty")
        if re.fullmatch(r"[a-zA-Z0-9_-]+", channel_id)  is None:
            raise ValueError(
                "Channel ID must be alphanumeric and may contain underscores and hyphens"
            )
        if not isinstance(name, str):
            raise TypeError("Channel name must be a string")
        if not name:
            raise ValueError("Channel name cannot be empty")
        if not (name.startswith("get ") or name.startswith("set ")):
            raise ValueError(
                "Channel name must start with 'get ' or 'set '"
            )
        if not isinstance(expect_response, bool):
            raise TypeError("Expect response must be a boolean")

        self.channel_id = channel_id
        self.name = name
        self.expect_response = expect_response
        self.direction = self.DIR_INPUT if name.startswith("get ") else self.DIR_OUTPUT
