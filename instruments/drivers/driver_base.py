"""
Base class for all driver classes.
"""

from abc import ABC
from abc import abstractmethod

from instruments.drivers.driver_settings import DriverSetting


class DriverBase(ABC):

    name = "base class"
    driver_settings = None

    def __init__(self, settings):
        self.user_settings = settings
        self.init()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.name is DriverBase.name:
            raise NotImplementedError(f"The name is not set in driver {cls.__name__}")
        if cls.driver_settings is None:
            raise NotImplementedError(f"The settings is not set in driver {cls.__name__}")
        if not isinstance(cls.driver_settings, list):
            raise NotImplementedError(f"The settings is not a list in driver {cls.__name__}")
        for setting in cls.driver_settings:
            if not isinstance(setting, DriverSetting):
                raise NotImplementedError(
                    f"The settings is not a type DriverSetting in driver {cls.__name__}")

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def shut_down(self):
        pass

    @abstractmethod
    def test_driver(self):
        pass
