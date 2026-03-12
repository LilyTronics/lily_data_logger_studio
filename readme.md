# Lily Data Logger Studio

Log data and control electronics instruments.
* Log measurement from electronic instruments (voltage, current, temperature, etc.)
* Control electronic instruments (temperature chambers, power supplies, signal generators, etc.)
* Output to table, graph and CSV file
* Write your own drivers using Python for any instrument

![main window](manual/images/main_window.png)

## Road map

Release 1.0:
* Read and save configuration files ✅
* Change configuration settings ✅
* Load and reload drivers from the instruments package ✅
* Edit instruments in the configuration ✅
* Edit process for controlling instruments ≫
* Start/stop data logger
* Show measurements in the data table
* Edit graphs in the configuration
* Show measurements in one or more graphs
* Write mearurement to a CSV file
* Show live updates on the process

For now the application is tested on Windows 11. But since it is all Python code, it could be
running on other OS as well.

Issues or feature requests can be submitted in the issue tracker: https://github.com/LilyTronics/lily_data_logger_studio/issues

## Contributing

If you find the Lily Data Logger Studio usefull and want to support it you can support in the following ways:
* Sponsor us, so we can spend more time on maintaining this software (https://github.com/sponsors/LilyTronics)
* Write instrument drivers. With more drivers the software becomes more usefull.
* If you cannot write instrument drivers yourself, we can do it for you.
  * We need access to the instrument (remote connection to a PC that is connected with the instrument).
  * You can send the instrument to us for borrowing and we can create a driver, then we send it back.
* Promote this software using your social channels.

## Installation

Download the zip file from the releases. This contains the compiled executable, libraries and instruments
package. It is a portable applicationa and doesn't require any installation.
Just unpack the zip file into a folder and run the executable.
Two manuals are included in PDF format. One about using the application and
one about adding instruments to the instruments package.

## Instruments package

The application uses a separate instruments package containing all Python code for communicating with
the instruments. This package can be updated seperately from the application.
This way any instrument can be integrated with the application even after installing the application.

---

© LilyTronics by Danny van der Pol

This software is provided as is. LilyTronics is not accepting any liabilites for damages that may be
cause bu this software.


