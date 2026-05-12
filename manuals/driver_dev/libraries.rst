Adding libraries
----------------

If you wish to include a library you cannot install this using `pip`.
Simply because we run the application from a compiled executable with Python libraries included.
When a library is installed on your system using pip it will not be available for the application.
Even the Python version of the application can be different from the Python version of your system.
From the lib folder of the application you can retrieve the Python version used.
Look for the DLL called: pythonxxx.dll where xxx indicates the Python version.
This is the Python version of the application.

Let's say you have an instrument that uses HTTP to connect and you want to use the
`requests` library. Of course you could use the build in Python HTTP libraries, but the
`requests` library may be more convenient to use.

First we need to download the library from `pip`. Go to the `requests` page on `pip`
(http://pypi.org/project/requests). Go to `download files` and find the source distribution.
When the download is finished, extract the files.

The requests library is a Python only library. Meaning the complete source code is Python
and does not require any compilation.
If the library requires any compilation, you need to do that first and then add the
library. If the library has any dependencies those need to be added too.

To add and use a library we simply create a folder `libraries` in the instument package.
In that folder add the usual `__init__.py` file to make it a Python package.

Now we can copy the library. The library for the `requests` is located in the folder
`src/requests` of the downloaded package. Copy the folder `requests` to the libraries folder.
The library files should now be in: `instruments/libraries/requests`.

Now create a Python file in the instrument package to test the library
(e.g.: instruments/test_requests.py).
Add the import to the library and try to make a HTTP request:

.. code-block:: python

    import instruments.libraries.requests as requests

    r = requests.get('https://lilytronics.nl')
    print(r.status_code)

The value of the status code should be printed in the console (200).
The library is succesfully added and can be used now in your driver, transport and protocol.
