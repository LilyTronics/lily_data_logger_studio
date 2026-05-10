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
