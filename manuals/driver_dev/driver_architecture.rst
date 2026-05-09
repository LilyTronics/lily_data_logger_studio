Driver architecture
-------------------

It is important to understand the basic architecture for a driver.
A driver consists of 3 layers:

* driver abstraction layer
* protocol layer
* transport layer

The driver abstraction layer exposes the setting for the driver and the channels.
The settings can be settings for the driver self, protocol or transport.
The settings are exposed in the application and can be set in the instrument properties.
The channels can be two kind, input or output.
Input channels represent measurements like measuring voltage, temperature etc.
Output channels represent settings in the instrument like setting output voltage on a
power supply or setting the temperature in a temperature chamber.
Those channels are exposed in the application and can be used in measurements and process steps.
It is also possible to have internal channels that are not exposed in the application but can
be used by the driver.

The protocol layer is resposible for putting the data from the channels into the proper format
(packet) before sending it to the instrument. The protocol layer is also responsible for
parsing the received date from the instrument to data suitable for the driver.

The transport layer is responisble for transferring data beteen the PC and the instrument.
The transport layer sets up the connection and sends the bytes from the protocol layer.
The transport layer passes the received bytes to the protocol layer.
The transport layer has no knowledge if the received data is valid or not.
This is determined by the protocol layer.
