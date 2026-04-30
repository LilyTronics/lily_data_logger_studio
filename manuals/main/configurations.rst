Configurations
--------------

Configurations are JSON files that contains the following items:

* Settings of the data logger
* Instruments and their settings.
* Measurments and their settings.
* Process control steps and their settings.
* Graphs and their settings.

With the following toolbar buttons the configuration can be created, opened and saved:

.. image:: images/configuration_buttons.png

The first button creates a new configuration. The second button opens an exsiting configuration.
The third button saves the current configuration. A configuration is saved in a single JSON file.
There is no limit on the size of the configuration (e.g.: number of instruments or measurements, etc.).

Next to the open configuration button is a small arrow. Clicking this arrow will show a
dropdown menu with the most recent opened configurations:

.. image:: images/recent_configurations.png

This makes it convenient to quickly open previous saved configuration.

New configurations are created with default settings:

* Sample time: 3 seconds
* End time: 1 minute
* Continuous mode: disabled

The settings can be changes with the following toolbar button:

.. image:: images/settings_button.png

A settings dialog will be shown:

.. image:: images/settings_window.png
    :align: center

|

In this window you can set the sample time and how the data logger must end.
The data logger can be stopped in the following ways:

* Fixed end time: the data logger is stopped at the given end time,
  whether the process or measurements are finished or not.
* Process end: the data logger stops when the process ends, measurements are also stopped.
* Continuous mode: the data logger must be stopped manually.
  If a process has ended, the measurements continue.

The total samples is an indication when fixed end time is used. In the other modes,
the number of samples depends on when the data logger stops.
