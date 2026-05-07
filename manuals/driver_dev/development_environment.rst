Development environment
-----------------------

Any development environment suitable for Python development will do.
For convenience a VS Code workspace is included for developing your driver.

When your driver requires specific Python libraries, these cannot be installed as usual using pip.
The application is a precompiled executable with Python libraries included.
When a library is installed on your system using pip it will not be available for the application.
Even the Python version of the application can be different from the Python version of your system.
From the lib folder of the application you can retrieve the Python version used.
Look for the DLL called: `pythonxxx.dll` where `xxx` indicated the Python version.

Libraries can be added by adding the source code of the library to a folder in the instrument package.
Then the library can be imported from that folder using the source code.
This is the only way to include specific libraries for your driver.
