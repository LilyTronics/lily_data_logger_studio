Lily Data Logger Studio™ Driver Development
===========================================

Lily Data Logger Studio relies on drivers to be able to communicate with different electronic instruments.
It is impossible to create drivers for all the different instruments that are out there.
This manual will help you create your own driver for your instrument.

To create a driver the following knowledge is required:

* Python programming
* Documentation about the protocol and the commands of the electronic instrument.

This manual may not be complete and not covering all possibilities for creating a driver.
It at least will get you started. In case of any issues, feel free to submit an issue
in the `issue tracker`_ on github.

.. toctree::
   :caption: Contents:
   :glob:

   development_environment.rst
   driver_request.rst
   introduction.rst
   driver_architecture.rst
   naming_convention.rst
   create_driver.rst
   subclassing.rst
   libraries.rst
   classes/index.rst

.. _issue tracker: https://github.com/LilyTronics/lily_data_logger_studio/issues
