[![Windows test and build](https://github.com/LilyTronics/lily_data_logger_studio/actions/workflows/windows_ci.yml/badge.svg)](https://github.com/LilyTronics/lily_data_logger_studio/actions/workflows/windows_ci.yml)
[![Ubuntu test and build](https://github.com/LilyTronics/lily_data_logger_studio/actions/workflows/ubuntu_ci.yml/badge.svg)](https://github.com/LilyTronics/lily_data_logger_studio/actions/workflows/ubuntu_ci.yml)

# Lily Data Logger Studio

Universal data logger (acquisition) and process control software.
Log data from electronic instruments and control electronic instruments.

✅ Log measurements from electronic instruments (voltage, current, temperature, etc.). \
✅ Control electronic instruments (temperature chambers, power supplies, signal generators, etc.). \
✅ Create, save and reload configurations \
✅ Setup instruments, measurements and process steps \
✅ Display results in data table and graphs (auto-update) \
✅ Export measurement data to: SQLite, JSON, CSV and TSV \
✅ Import measurement data from: SQLite and JSON \
✅ Backup and restore of your configuration and measurements \
✅ Python development environment for creating drivers for your instruments \
✅ User manual and driver development manual included \
✅ Tested on Windows and Ubuntu (probably can run on others).

Check the releases for the latest release: [releases](https://github.com/LilyTronics/lily_data_logger_studio/releases)

![main window](manuals/main/images/main_window.png)

## Road map

Latest release: V1.0.

No roadmap items planned.

Issues or feature requests can be submitted in the issue tracker: [issues](https://github.com/LilyTronics/lily_data_logger_studio/issues)

## Contributing

If you find the Lily Data Logger Studio usefull and want to support it you can support in the following ways:
* Sponsor us, so we can spend more time on maintaining this software (https://github.com/sponsors/LilyTronics)
* Write instrument drivers. With more drivers the software becomes more usefull.
  * If you cannot write instrument drivers yourself, we can do it for you.
* Promote this software using your social channels.

## Installation

Download the zip file from the releases. This contains the compiled executable, libraries and instruments
package. It is a portable applicationa and doesn't require any installation.
Just extract the zip file into a folder and run the executable.
Two manuals are included in PDF format. One about using the application and
one about adding instruments to the instruments package.

## Instruments package

The application uses a separate instruments package containing all Python code for communicating with
the instruments. This package can be updated seperately from the application.
This way any instrument can be integrated with the application even after installing the application.
Templates and a VS code workspace are included for creating drivers.
A test application is included for testing the drivers.

---

© LilyTronics by Danny van der Pol

This software is provided as is. LilyTronics does not accept any liabilites for damages that may be
caused by this software.
