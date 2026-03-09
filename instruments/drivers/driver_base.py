"""
Base class for all driver classes.
"""

from abc import ABC

from instruments.drivers.driver_settings import DriverSetting


class DriverBase(ABC):

    name = "base class"
    driver_settings = None

    def __init__(self, settings):
        self.user_settings = settings

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Driver name
        assert cls.name is not DriverBase.name, f"The name is not set in driver {cls.__name__}"
        assert cls.name != "", f"The name is not set in driver {cls.__name__}"
        # Driver settings
        assert cls.driver_settings is not None, f"The settings is not set in driver {cls.__name__}"
        assert isinstance(cls.driver_settings, list), \
            f"The settings is not a list in driver {cls.__name__}"
        assert len(cls.driver_settings) > 0, f"The settings is empty in driver {cls.__name__}"
        for setting in cls.driver_settings:
            assert isinstance(setting, DriverSetting), \
                f"The settings is not a type DriverSetting in driver {cls.__name__}"

    @classmethod
    def get_class_name(cls):
        return cls.__name__
