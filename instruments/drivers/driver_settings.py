"""
Driver settings object.
"""

class DriverSetting:

    CTRL_TEXT = "TextCtrl"

    _VALID_TYPES = [str, int, float]
    _VALID_CONTROLS = [CTRL_TEXT]

    def __init__(self, name, setting_type, default_value, gui_control):
        assert setting_type in self._VALID_TYPES, \
            f"The type {setting_type} for {name} is not supported"
        assert isinstance(default_value, setting_type), \
            f"The default value for {name} has the wrong type"
        assert gui_control in self._VALID_CONTROLS, \
            f"The control {gui_control} for {name} is not supported"

        self.name = name
        self.type = setting_type
        self.default_value = default_value
        self.gui_control = gui_control
