# Lily Data Logger Studio

Log data and control electronics instruments.
* Log measurement from electronic instruments (voltage, current, temperature, etc.)
* Control electronic instruments (temperature chambers, power supplies, signal generators, etc.)
* Output to table, graph and CSV file
* Write your own drivers using Python for any instrument

![main window](manual/images/main_window.png)


# Installation

Download the zip file from the releases. This contains the compiled executable, libraries and instruments
package. It is a portable applicationa and doesn't require any installation.
Just unpack the zip file into a folder and run the executable.
Two manuals are included in PDF format. One about using the application and
one about adding instruments to the instruments package.

# Instruments package

The application uses a separate instruments package containing all Python code for communicating with
the instruments. This package can be updated seperately from the application.
This way any instrument can be integrated with the application even after installing the application.

# Disclamer

This software is provided as is. LilyTronics is not accepting any liabilites for damages that may be
cause bu this software.

(c) LilyTronics by Danny van der Pol
