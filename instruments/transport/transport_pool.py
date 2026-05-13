"""
Contains all the transport instances.
Prevents creating double transport objects.
"""


class TransportPool:

    _TRANSPORTS = {}

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ##########
    # Public #
    ##########

    @classmethod
    def create_transport(cls, transport_class, settings, debug):
        tp = transport_class(settings, debug)
        tp_id = tp.get_id()
        if tp_id not in cls._TRANSPORTS:
            cls._TRANSPORTS[tp_id] = tp
        return cls._TRANSPORTS[tp_id]


if __name__ == "__main__":

    from instruments.transport.transport_serial import TransportSerial
    from instruments.transport.transport_tcp import TransportTcp
    from instruments.transport.transport_udp import TransportUdp

    tp1 = TransportPool.create_transport(TransportSerial, {"port": "COM3"}, "")
    print(tp1)
    tp2 = TransportPool.create_transport(TransportSerial, {"port": "COM3"}, "")
    print(tp2)
    assert tp1 is tp2, "Transport must be the same"
    tp3 = TransportPool.create_transport(TransportSerial, {"port": "COM4"}, "")
    print(tp3)
    assert tp2 is not tp3, "Transport must be different"
    tp4 = TransportPool.create_transport(TransportTcp, {"host": "localhost", "port": 1234}, "")
    print(tp4)
    tp5 = TransportPool.create_transport(TransportTcp, {"host": "127.0.0.1", "port": 1234}, "")
    print(tp5)
    assert tp4 is tp5, "Transport must be the same"
    tp6 = TransportPool.create_transport(TransportUdp, {"host": "127.0.0.1", "port": 1234}, "")
    assert tp5 is not tp6, "Transport must be different"
