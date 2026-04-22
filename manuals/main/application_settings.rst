Application settings
--------------------

Application settings are stored in a folder. The folder depends on your operating system:

* Windows: C:\\Users\\<name>\\AppData\\Roaming\\LilyDataLoggerStudio
* Ubuntu: ~/.local/share/LilyDataLoggerStudio

In this folder you can find the following files:

* LilyDataLoggerStudio.json: settings for the main application and driver test application.
* LilyDataLoggerStudio.log: log file for the main application
* LilyDataLoggerStudioDriverTest.log: log file for the driver test application

The settings file and log files can be deleted. This will not harm the applications.
If the settings file is not present, they will use default settings.
The log files are created when the application starts. The previous log file is
overwritten. If you want to j=keep settings and or a log file, you must copy them
after closing the application and before starting the application again.
