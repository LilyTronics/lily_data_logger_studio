Introduction
============

In this manual we will make a driver for communicating with an Arduino.
The Arduino will be used as a simple data acquisition module (DAQ).
It will be able to read the states of the digital pins and set the states of the digital pins.
It will also be able to read the values of the analog pins.
A sketch for the Arduino is provided in the folder `arduino_daq`.
We assume that you are able to upload this sketch into your Arduino board.
Any Arduino board should work. The sketch is created for the Arduino UNO, but with
some small modifications it should be able to run on any Arduino board.

For testing the driver a test application is provided.
The name of the executable is: `LilyDataLoggerStudioDriverTest`.
Below is a screenshot of the test application.

.. image:: images/driver_test.png

More about this application later when we will use it to test our driver.
