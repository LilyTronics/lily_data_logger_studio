"""
Driver settings object.
"""

class DriverSetting:

    CTRL_TEXT = "TextCtrl"

    _VALID_TYPES = [str, int, float]
    _VALID_CONTROLS = [CTRL_TEXT]

    def __init__(self, name, setting_type, default_value, gui_control):
        if setting_type not in self._VALID_TYPES:
            raise ValueError(
                f"Setting type {setting_type} for '{name}' is not supported"
            )
        if not isinstance(default_value, setting_type):
            raise TypeError(
                f"Default value for '{name}' must be of type {setting_type.__name__}"
            )
        if gui_control not in self._VALID_CONTROLS:
            raise ValueError(
                f"GUI control '{gui_control}' for '{name}' is not supported"
            )

        self.name = name
        self.type = setting_type
        self.default_value = default_value
        self.gui_control = gui_control


if __name__ == "__main__":

    from tests.unit_tests.driver_tests.driver_temperature_chamber_test import \
        DriverTemperatureChamberTest

    DriverTemperatureChamberTest().run()
