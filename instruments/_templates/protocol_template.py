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
        # Check if the response is correct to indicate that the response is valid
        return True


if __name__ == "__main__":

    from instruments._templates.transport_template import TransportTemplate

    # Test code for the protocol functions

    # The protocol requires a transport, with settings
    transport_test_settings = {
    }
    transport = TransportTemplate(transport_test_settings)

    # Protocol test settings
    protocol_test_settings = {
    }
    protocol = ProtocolTemplate(transport, protocol_test_settings)

    # Test
    tx_data = b"test data"
    print(protocol.build_packet(tx_data))

    rx_data = b"test data"
    print(protocol.parse_packet(rx_data))

    response = b"test data"
    print(protocol.validate_response(response))
