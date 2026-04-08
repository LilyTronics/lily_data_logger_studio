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

    def close(self):
        # Close the transport channel
        pass


if __name__ =="__main__":

    # Test code imports only
    import time

    # Transport test settings
    transport_test_settings = {
    }
    transport = TransportTemplate(transport_test_settings)

    # Test

    # Should be False because connect() is not called yet
    print(transport.is_connection_ready())

    transport.connect()

    # Should be True because connect() is called
    print(transport.is_connection_ready())

    # Send some data
    transport.send(b"test data")

    # Receive some data, with a time out
    timeout = 5   # seconds timout
    while timeout > 0:
        print(transport.receive())
        time.sleep(1)
        timeout -= 1

    transport.close()
