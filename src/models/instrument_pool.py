"""
Contains the instances of the instruments.
Redirect processing channels and measurements to the correct instrument.
"""

from copy import deepcopy

from src.models.drivers import Drivers


class InstrumentPool:

    _INSTRUMENTS = {}

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def clear(cls):
        cls._INSTRUMENTS = {}

    @classmethod
    def get_instruments(cls):
        return deepcopy(cls._INSTRUMENTS)

    @classmethod
    def add_instruments(cls, instruments):
        for instrument in instruments:
            if "instance" in instrument:
                cls._INSTRUMENTS[instrument["id"]] = instrument["instance"]
            elif "driver_id" in instrument:
                driver_class = Drivers.get_driver(instrument["driver_id"])
                if driver_class is not None:
                    cls._INSTRUMENTS[instrument["id"]] = driver_class(instrument["settings"])

    @classmethod
    def get_instrument(cls, instrument_id):
        return cls._INSTRUMENTS.get(instrument_id, None)

    @classmethod
    def has_simulators(cls):
        for instrument in cls._INSTRUMENTS.values():
            if instrument.is_simulator:
                return True
        return False


if __name__ == "__main__":

    from tests.unit_tests.model_tests.instrument_pool_test import InstrumentPoolTest

    InstrumentPoolTest().run()
