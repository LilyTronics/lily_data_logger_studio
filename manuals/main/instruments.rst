Instruments
-----------

Instruments represent your physical instrument.

This manual uses the build in simulators. This way you can try out all the steps from This
manual without the actual need of real instruments.

For managing the instruments, click the following toolbar button:

.. image:: images/instruments_button.png

The following dialog appears:

.. image:: images/instruments_window.png
   :align: center

|

To add an instrument, enter a name for the instrument, select a driver and enter the driver settings.
Instrument names must be unique. Below is a screenshot for adding the temperature chamber simulator:

.. image:: images/instruments_add.png
   :align: center

|

The settings like host and port depends on which settings are exposed by the driver.
If settings are not exposed, default settings are used.

If there is no driver for your instrument, you can create one.
A separate manual for developing drivers is available.

Before saving you can test the settings by clicking the Test button.
This will run a test provided by the driver to check if the instrument responds correct.
Information about the test results will be shown in the text box.

Once the instrument is saved, they will show in the list.
The instrument settings can be updated by double clicking the instrument in the list.

.. image:: images/instruments_edit.png
   :align: center

|

When the Cancel button is pressed all changes are reverted.

Instruments can only be deleted when they are not used in process steps or measurments.
