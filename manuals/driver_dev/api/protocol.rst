Protocol base class
===================

.. currentmodule:: protocol.protocol_base

.. autoclass:: ProtocolBase
    :members:

Protocol ASCII
==============

The ASCII protocol class can be used for all instruments that use communication based on ASCII
characters. All packets have the following format: :code:`<data><EOL>`.
The data is followed by an end of line character. Usually LF, CR or CRLF.
The end of line character is defined in the protocol settings.
If the end of line character is not defined, the protocol will use LF as default.


Build packet
------------

.. literalinclude:: ../../../instruments/protocol/protocol_ascii.py
    :pyobject: ProtocolAscii.build_packet
    :dedent:

The build packet method takes the data as input and adds the end of line character to it.

Parse packet
------------

.. literalinclude:: ../../../instruments/protocol/protocol_ascii.py
    :pyobject: ProtocolAscii.parse_packet
    :dedent:

The parse packet method takes the raw data as input and removes the end of line character from it.

Validate response
-----------------

.. literalinclude:: ../../../instruments/protocol/protocol_ascii.py
    :pyobject: ProtocolAscii.validate_response
    :dedent:

A packet is valid if it ends with the end of line character defined in the protocol settings.
