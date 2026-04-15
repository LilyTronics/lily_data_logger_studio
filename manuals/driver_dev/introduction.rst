Lily Data Logger Studio Driver Development
==========================================

Lily Data Logger Studio relies on drivers to be able to communicate with different electronics instruments.
It is impossible to create drivers for all the different instruments that are out there.
This manual will help you create your own driver for your instrument.

In this manual we will make a driver for communicating with an Arduino.
The Arduino will be used as a simple data acquisition device.
It will be able to read the states of the digital pins and set the states of the digital pins.
It will also be able to read the values of the analog pins.
A sketch for the Arduino is provided in the folder `TODO`.
We assume that you are able to upload this sketch into your Arduino board.
Any Arduino board should work. In this manual we use an Arduino Uno.

For testing the driver a test application is provided.
The name of the executable is: `LilyDataLoggerStudioDriverTest`.
Below is a screenshot of the test application.

.. image:: images/driver_test.png

More about this application later when we will use it to test our driver.
