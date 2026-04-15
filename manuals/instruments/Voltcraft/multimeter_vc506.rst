Voltcraft Multimeter VC506
==========================

Multimeter VC506 from Voltcraft. This has a serial interface and can retrieve the current measurement.
The multimeter must be setup manually:

* Set the multimeter to the desired measurement mode (e.g. voltage, current, resistance).
* Connect the multimeter to the computer using the serial interface.
* Enable RS232 using the menu button on the multimeter.
* Optionally enable the keep on function to prevent the multimeter from turning off after a certain time.

The multimeter interface hardware is designed for old school serial ports
(sub-D connectors with levels of ±3V up to ±15V).
These voltages are used to power the serial interface in the multimeter.
When using a USB to serial adapter, make sure that the adapter supports the necessary voltage levels
on the RTS and DTR lines to power the serial interface in the multimeter.
In case the communication does not work, check these levels or try an adapter from a different manufacturer.

.. currentmodule:: drivers.voltcraft.multimeter_vc506

Driver settings
---------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :start-at: driver_settings = [
    :end-at: ]
    :dedent:

There is only one setting for this driver, which is the port to which the multimeter is connected.

Channels
--------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :start-at: channels = [
    :end-at: ]
    :dedent:

There is only one channel for doing a measurement.
Which measurement is determined by the mode of the multimeter.

Transport and protocol
----------------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :start-at: transport =
    :end-at: protocol =
    :dedent:

The driver uses a serial transport and ASCII protocol.

Transport settings
------------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :start-at: transport_settings = {
    :end-at: }
    :dedent:

The transport settings are fixed and cannot be changed by the user.
The serial interface in the multimeter is powered by the voltages on the RS232 interface.
Therefore RTS and DTR must have the proper voltage levels to power the interface.

Protocol settings
------------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :start-at: protocol_settings = {
    :end-at: }
    :dedent:

The protocol settings are fixed and cannot be changed by the user.
The multimeter uses the CR character as the end of packet character.

Build command
--------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :pyobject: VoltcraftVC506.build_command
    :dedent:

There is no specific command to do a measurement.

Parse response
--------------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :pyobject: VoltcraftVC506.parse_response
    :dedent:

The response format is: :code:`<measurement><space><value><space><unit>`.
For example: :code:`VDC 12.3 V`.
Only the value part is retrieved and returned as a float.

Test driver
-----------

.. literalinclude:: ../../../instruments/drivers/voltcraft/multimeter_vc506.py
    :pyobject: VoltcraftVC506.test_driver
    :dedent:

There is no specific command for testing the driver. It can only be tested by doing a
measurement.
