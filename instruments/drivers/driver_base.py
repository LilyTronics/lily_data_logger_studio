"""
Base class for all driver classes.
"""

from abc import ABC

from instruments.drivers.driver_channel import DriverChannel
from instruments.drivers.driver_settings import DriverSetting


class DriverBase(ABC):

    name = "base class"
    driver_settings = None
    channels = None
    is_simulator = False

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
        # Channels
        assert cls.channels is not None, f"The channels is not set in driver {cls.__name__}"
        assert isinstance(cls.channels, list), \
            f"The channels is not a list in driver {cls.__name__}"
        assert len(cls.channels) > 0, f"The channels is empty in driver {cls.__name__}"
        for channel in cls.channels:
            assert isinstance(channel, DriverChannel), \
                f"The channels is not a type DriverChannel in driver {cls.__name__}"

    @classmethod
    def get_class_name(cls):
        return cls.__name__
