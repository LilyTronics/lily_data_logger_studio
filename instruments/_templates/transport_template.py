"""
Transport template.
"""

from instruments.transport.transport_base import TransportBase


class TransportTemplate(TransportBase):


    def is_connection_ready(self):
        try:
            # Test if the connection to the instrument is ready
            return True
        except:
            return False

    def connect(self):
        # Establish a connection to the instrument.
        pass

    def send(self, data):
        # Send data to the instrument
        pass

    def receive(self):
        # Get and return the data from the instrument directly
        # if no data available directly return with an empty byte string
        data = b""
        return data
