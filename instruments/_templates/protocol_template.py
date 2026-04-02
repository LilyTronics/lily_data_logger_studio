"""
Protocol template.
"""

from instruments.protocol.protocol_base import ProtocolBase


class ProtocolTemplate(ProtocolBase):

    def build_packet(self, data):
        # Build a packet from the data so it can be sent to the instrument
        return data

    def parse_packet(self, data):
        # Retrieve the response value from the data received from the instrument
        return data

    def validate_response(self, response):
        # Check if the repsonse is correct to indicate that the response is valid
        return True
