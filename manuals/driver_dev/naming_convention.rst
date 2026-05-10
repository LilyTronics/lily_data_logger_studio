Naming convention
-----------------

To keep the instrument package consistent we use the following naming convention:

=========== ================================================== ===========================
Item        Naming convention                                      Example
=========== ================================================== ===========================
Folder name Manufacturer name, snake_case                      aim_tti
File name   Instrument type and model or series, snake_case    oscilloscope_tds200.py
File name   When using a base class the file must end with     oscilloscope_tds_base.py

            `_base`
Class name  Manufacturer, instrument type and model or series, TektronixOscilloscopeTds200

            PascalCase
=========== ================================================== ===========================
