"""
Driver settings object.
"""

class DriverSetting:
    """
    Driver setting.

    :param name:            Name of the setting.
    :param setting_type:    Type of the setting (str, int, float).
    :param default_value:   Default value of the setting.
    :param gui_control:     GUI control type for the setting.
    :param gui_params:      Parameters for the GUI control (depending on control).

    The name is displayed in the GUI and is used as key for the settings dictionary.
    The default value is used to intialize the contol in the GUI.
    The GUI control type must be a wxPython GUI control type.

    Supported controls:
    TextCtrl: text box, default value is added to the text box
    ComboBox: drop down box, list items must be in gui_params["items"]
              selected value is the default value
    """

    CTRL_TEXT = "TextCtrl"
    CTRL_CMB = "ComboBox"

    _VALID_TYPES = [str, int, float]
    _VALID_CONTROLS = [CTRL_TEXT, CTRL_CMB]

    def __init__(self, name, setting_type, default_value, gui_control, gui_params=None):
        if setting_type not in self._VALID_TYPES:
            raise ValueError(
                f"(Settings) Setting type {setting_type} for '{name}' is not supported"
            )
        if default_value is not None and not isinstance(default_value, setting_type):
            raise TypeError(
                f"(Settings) Default value for '{name}' must be of type {setting_type.__name__}"
            )
        if gui_control not in self._VALID_CONTROLS:
            raise ValueError(
                f"(Settings) GUI control '{gui_control}' for '{name}' is not supported"
            )

        self.name = name
        self.type = setting_type
        self.default_value = default_value
        self.gui_control = gui_control
        self.gui_params = gui_params

if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
