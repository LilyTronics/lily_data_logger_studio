# Instruments package

This package contains the drivers for various instruments to use with the
Lily Data Logger Studio.

## Adding drivers

You can add driver yourself for your equipment.
See the manual 'Driver Development' for more details.

## Naming convention

The followng naming conventions should be applied to have consistensy for the drivers.

Instruments are categorised by manufacturer.

| Item        | Naming conventions                                            | examples                    |
|-------------|---------------------------------------------------------------|-----------------------------|
| Folder name | Manufacturer name only, snake_case                            | aim_tti                     |
| File name   | Type instrument and model or series, snake_case               | oscilloscope_tds200.py      |
| File name   | When using a base class the file must end with `_base`        | oscilloscope_tds_base.py    |
| Class name  | Manufacturer, instrument type and model or series, PascalCase | TektronixOscilloscopeTds200 |
