Protocol ASCII
--------------

The ASCII protocol class can be used for all instruments that use communication based on ASCII
characters. All packets have the following format: :code:`<data><EOL>`.
The data is followed by an end of line character. Usually LF, CR or CRLF.
The end of line character is defined in the protocol settings.
If the end of line character is not defined, the protocol will use LF as default.

.. literalinclude:: ../../../instruments/protocol/protocol_ascii.py
    :pyobject: ProtocolAscii
