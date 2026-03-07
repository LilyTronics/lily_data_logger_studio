"""
Base class for all driver classes.
"""

from abc import ABC, abstractmethod


class DriverBase(ABC):

    name = "base class"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.name is DriverBase.name:
            raise ValueError(f"The name is not set in driver {cls.__name__}")
