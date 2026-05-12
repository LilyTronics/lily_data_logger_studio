Development environment
-----------------------

Any development environment suitable for Python development will do.
For convenience a VS Code workspace is included for developing your driver.

When your driver requires specific Python libraries, these cannot be installed as usual using pip.
The chapter about adding libraries can help yo with this.

Note that the Python version used in the application may not be the same as the Python version
on your system.

When developing drivers, it may be good practice to create a special Python environment
with the same Python version of the application.
From the lib folder of the application you can retrieve the Python version used.
Look for the DLL called: pythonxxx.dll where xxx indicates the Python version.
This is the Python version of the application.

More details about Python environments can be found here: https://docs.python.org/library/venv.html
