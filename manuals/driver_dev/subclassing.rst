Subclassing
-----------

When ceating a driver for a series of instruments that look the same, subclassing can be
applied. This is done with the drivers for the Tektronix TDS series oscilloscopes.
The driver for the Tektronix TDS series using a base class:

.. literalinclude:: ../../instruments/drivers/tektronix/oscilloscope_tds_base.py
    :language: python
    :start-at: class
    :end-before: internal_channels =

Not all content is shown, but the base class contains all the attributes that are common
in the series. Also it contains all the logic for building commands and parsing the responses.

Note that the base class is not derived from the driver base class. This is intentional.
This is to prevent that the base class is listed as a driver in the application.

Then for each specific model we create a subclass. The subclasses are derived from the
base class and the driver base class.
The sub class for the TDS200 models:

.. literalinclude:: ../../instruments/drivers/tektronix/oscilloscope_tds200.py
    :language: python
    :pyobject: TektronixOscilloscopeTds200

The sub class for the TDS1000 models:

.. literalinclude:: ../../instruments/drivers/tektronix/oscilloscope_tds1000.py
    :language: python
    :pyobject: TektronixOscilloscopeTds1000

The sub class for the TDS2000 models:

.. literalinclude:: ../../instruments/drivers/tektronix/oscilloscope_tds2000.py
    :language: python
    :pyobject: TektronixOscilloscopeTds2000

The only difference are the ID, model name and description.
