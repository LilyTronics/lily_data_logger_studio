"""
Transport over serial port.
"""

import serial

from instruments.transport.transport_base import TransportBase


class TransportSerial(TransportBase):

    serial = serial.Serial()

    def is_connection_ready(self):
        try:
            return self.serial.is_open
        except:
            return False

    def connect(self):
        self.serial.port = self.transport_settings.get("port", None)
        self.serial.baudrate = self.transport_settings.get("baudrate", 9600)
        self.serial.bytesize = self.transport_settings.get("bytesize", serial.EIGHTBITS)
        self.serial.parity = self.transport_settings.get("parity", serial.PARITY_NONE)
        self.serial.stopbits = self.transport_settings.get("stopbits", serial.STOPBITS_ONE)
        self.serial.open()
        self.serial.rts = self.transport_settings.get("rts", self.serial.rts)
        self.serial.dtr = self.transport_settings.get("dtr", self.serial.dtr)

    def send(self, data):
        self.serial.write(data)

    def receive(self):
        data = b""
        if self.serial.in_waiting > 0:
            return self.serial.read_all()
        return data

    def close(self):
        if self.serial.is_open:
            self.serial.close()


if __name__ =="__main__":

    # Test code imports only
    import time

    # Transport test settings
    transport_test_settings = {
        "port": "COM8",
        "baudrate": 115200
    }
    transport = TransportSerial(transport_test_settings)

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
