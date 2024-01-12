"""
This file is automatically generated by the instruments/_generate_instrument_data.py script.
"""

import base64
import json


class InstrumentData(object):

    instrument_simulator_multimeter = base64.b64decode(
        b'eyJuYW1lIjogIlNpbXVsYXRvciBtdWx0aW1ldGVyIn0='
    )

    instrument_simulator_temperature_chamber = base64.b64decode(
        b'eyJuYW1lIjogIlNpbXVsYXRvciB0ZW1wZXJhdHVyZSBjaGFtYmVyIn0='
    )

    @classmethod
    def get_list_of_instrument_names(cls):
        attributes = list(filter(lambda x: x.startswith('instrument_'), vars(cls).keys()))
        names = map(lambda x: json.loads(getattr(cls, x))['name'], attributes)
        return sorted(list(names))

    @classmethod
    def get_instrument_data_by_name(cls, instrument_name):
        attributes = list(filter(lambda x: x.startswith('instrument_'), vars(cls).keys()))
        matches = list(filter(lambda x: json.loads(getattr(cls, x))['name'] == instrument_name, attributes))
        if len(matches) == 1:
            return getattr(cls, matches[0])
        return None


if __name__ == '__main__':

    for name in InstrumentData.get_list_of_instrument_names():
        print(json.loads(InstrumentData.get_instrument_data_by_name(name)))
