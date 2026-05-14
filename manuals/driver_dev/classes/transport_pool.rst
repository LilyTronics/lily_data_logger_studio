Transport pool
--------------

The purpose of the transport pool is to prevent creating duplicate transport layers.
Lets say there are two instruments on a RS485 bus. Those instruments are physically connected
to the same transport layer. Since the transport layer cannot be created twice, we use the
transport pool to create one instance of the transport layer that can be used in multiple
instruments. The transport pool is a singleton class.

.. currentmodule:: transport.transport_pool

.. autoclass:: TransportPool
    :members:
