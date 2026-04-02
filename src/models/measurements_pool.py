"""
Contains the measurements.
Every measurement is processed by this class.
"""

from src.models.instrument_pool import InstrumentPool


class MeasurementsPool:

    _MEASUREMENTS = {}

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def clear(cls):
        cls._MEASUREMENTS = {}

    @classmethod
    def get_measurements(cls):
        return cls._MEASUREMENTS

    @classmethod
    def add_measurements(cls, measurements):
        for measurement in measurements:
            if InstrumentPool.get_instrument(measurement["instrument_id"]) is not None:
                cls._MEASUREMENTS[measurement["id"]] = measurement

    @classmethod
    def process_measurement(cls, measurement_id, callback=None, callback_params=None):
        measurement = cls._MEASUREMENTS.get(measurement_id, None)
        if measurement is None:
            return None
        instrument = InstrumentPool.get_instrument(measurement["instrument_id"])
        if instrument is None:
            return None
        value = instrument.process_channel(measurement["channel_id"], callback=callback,
                                           callback_params=callback_params)
        if isinstance(value, (int, float)):
            gain = measurement.get("gain", 1.0)
            offset = measurement.get("offset", 0.0)
            value = type(value)(value * gain + offset)
        return value


if __name__ == "__main__":

    from tests.unit_tests.model_tests.measurements_pool_test import MeasurementsPoolTest

    MeasurementsPoolTest().run()
