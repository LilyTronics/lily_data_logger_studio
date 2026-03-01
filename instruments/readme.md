# Instrument drivers architecture

The insturment drivers architecture consists of 3 layers:

* transport layer
* protocol layer
* driver layer

## Transport layer

The transport layer is responsible for writing and reading bytes using a physical interface.
Interfaces can be, but not limited to:

* Serial port
* IP/UDP
* IP/TCP

## Protocol layer

The protocol layer is responsible for interpreting the bytes that are written or read using
the transport layer. This handles stuff like termination, CRC, frame formatting, and so on.
The protocol layer work with a message queue. In case the transport layer is a multi instrument
bus system (e.g: RS-485), messages can have small delays due to the availabilitiy of the bus.

## Driver layer

This is the actual instrument dependent layer. This is responsible for exposing the functionality
of the instrument into logical functions that can be called in the application.

# Graphical represtation of the architecture

Below is a graphical representation of the architecture

```

+----------------------------------------------------+
| Application calls:                                 |
| float voltage = driver.get_dc_voltage()            |
+----------------------------------------------------+
                          |
+----------------------------------------------------+
| Driver calls:                                      |
| bytes response = protocol.get_value(command)       |
+----------------------------------------------------+
                          |
+----------------------------------------------------+
| Protocol calls:                                    |
| bytes response = transport.send_and_receive(bytes) |
+----------------------------------------------------+
                          |
+----------------------------------------------------+
| Transport sends and receives bytes.                |
| Returns the received bytes to the protocol.        |
+----------------------------------------------------+

```

1. The applcication has no knowlegde about the protocol and how to get an actual value from
the instrument. It only calls a function to get a DC voltage (e.g. from a multimeter).

2. The driver known only the command that need to be send to the instrument to get a DC voltage
(e.g.: 'VDC?'). The driver passes that command to the protocol handler.

3. The protocol handler formats the command into a proper frame ready to send through the transport
layer (e.g.: 'VDC?' -> 'VDC?\n', added the proper termination).

4. The protocol handler passes the formatted command to the transport layer. The command is send and
the received bytes send back to the protocol handler.

5. The protocol handler removes all frame formatting and send the received bytes back to the driver.

6. The driver interpret the bytes as a voltage and sends the floating point result to the application.
