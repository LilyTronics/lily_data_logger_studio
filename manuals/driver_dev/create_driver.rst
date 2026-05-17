Create a driver
---------------

For creating a driver the template from the `_templates` folder can be used.

* Create a folder for the mannufacturer: `arduino`
* Copy the driver_template.py ot that folder and rename the file: `arduino_daq.py`

Now open the file in your Python development environment.

First thing to change is the doc string at the top.
Also we need to have the correct imports. For the transport we import the serial transport.
For the protocol we import the ascii protocol.

We rename the class to `ArduinoDaq`

Next we set the properties for the driver. First we generate a new ID. In the drivers folder is
a script called `driver_id.py`. If we run that script we get a new ID. We drivers are loaded,
The IDs are checked for doubles, so if the ID already exists (chance is really low), just
generate a new one. Next we set the properties:

* manufacturer: Arduino
* model: "DAQ"
* description: "Basic DAQ using the Arduino platform"

Then set the transport and the protocol properties. Now the first part of the driver should look
like this:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :start-at: """
    :end-at: protocol =

Now lets create the driver settings. The Arduino communicates with standard serial port settings.
Even the speed is fixed. So actually there is only one setting: the port name (COM4, /dev/ttyUSB2).
This should be a string. We add the following setting:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :start-at: driver_settings =
    :end-before: # End settings

Now we can define the channels. The Arduino DAQ firmware has the following channels:

* Get the ID. This gets the ID string. This is an input channel.
* Get the value from an analog input. This is an input channel.
* Get the value from a digital input. This is an input channel.
* Set the value for a digital output. This is an output channel.
* Set a digital pin as input. This is an output channel.

For getting and settings values, we need set a channel number. This will be a parameter
for the channel. This parameter will be exposed in the application.
Getting the ID will not have any parameters.

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :start-at: channels =
    :end-before: # End channels

The channels for reading analog inputs, digital inputs and writing digital outputs all have an extra
paramater called 'channel'. This will be exposed in the application. There you can enter the
number of the analog input or digital IO according to the IO numbering of the Arduino board.
The name is arbirtary and can be chosen as you wish.

When the application processes a channel, the driver needs to supply the proper commands for each channel.
This is done in a method called `build_command`:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :pyobject: ArduinoDaq.build_command

The build command has two parameters, the channel and the params.
The channel is one of the driver channels as defined before. The params is a dictionary
with the parameters for that channel (if any).
For a set command, the params always have a value property. In this case we also get the channel
property. This command is passed to the protocol layer. The command must be bytes (b'').
The protocol layer sends the command in the proper format to the instrument using the transport layer
and the reponse is send back to the driver. The driver needs to process the response and extract the
value from the data. This is done in a method called `parse_response`:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :pyobject: ArduinoDaq.parse_response

Basically the response from the Arduino can be a stirng (for the ID string), an integer
(for the digital channels) or a float (for the analog channels).
The type is defined in the channel object.

There s one other method that needs to be implemented and that is the method called `test_driver`:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :pyobject: ArduinoDaq.test_driver

This method is used when the application tests if the instrument is available.
In this case we simply request the ID string and test if it is correct.

Finally there is an optional method that can be implemented and is called `init_driver`.
This is not always required. In case of the Arduino board, it is required.

When the driver is initialized from the application, the transport layer is not active.
It will be active when the frist command is issued and stays active after that. In this casegy
our transport is a serial port. At the first command, the serial port is opened. When the serial port
is opened the Arduino will reset because of activity on the DTR pin. This reset causes a small delay before
we can actually communicate with the Arduino. Right after opening the serial port, the command is send
and will fail because of the small delay. After that the serial port stays open and the commands following
will be handeled correct. To prevent this we use the `init_driver`` method:

.. literalinclude:: ../../instruments/drivers/arduino/arduino_daq.py
    :language: python
    :pyobject: ArduinoDaq.init_driver

This is called when the driver is initilized. We do the driver test until is succeeds. The driver test
will get the ID string. The first time it will fail because of the reset. The second time it probably will
pass already. So within 4 tries it should pass. This way we are sure the Arduino is ready.

This finishes the driver for the Arduino. Now to test the driver we simply start the driver test application:

.. image:: images/driver_test.png
   :align: center

|

In the driver test applucation, select the Arduino driver and a channel to test. In this case we test
reading an analog channel. We enter the correct port number (this will be different on your system)
and the channel parameter (3). This reads analog input A3. The result is presented in the text box
at the botoom. The analog input reads: 2.151 (volt). Of course the value depends on what is connected
to that input. We connected a resistor network to create a specific voltage. Of course anything can
be connected as long as the voltage is within 0 to 5V (the range of the analog input).

Be aware that the Arduino inputs and outputs are unprotected. To interface with various voltages or
other components, extra circuitry is required to prevent damage to the Arduino pins.
