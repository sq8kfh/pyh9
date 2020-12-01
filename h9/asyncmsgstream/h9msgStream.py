import logging
import asyncio
import struct

from ..msg import H9msg, xml_to_h9msg, H9Identification


class H9msgStream(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    async def connect(self, entity="pyh9"):
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
        self.writemsg(H9Identification(entity))

    def writemsg(self, msg: H9msg):
        data = msg.to_bytes()
        if not self._writer:
            logging.warning("NOT")
        self._writer.write(struct.pack("!I", len(data)))
        self._writer.write(data)

    async def readmsg(self) -> H9msg:
        tmp = await self._reader.readexactly(4)
        length = struct.unpack("!I", tmp)[0]

        data = await self._reader.readexactly(length)
        msg = xml_to_h9msg(data)
        return msg

    def close(self):
        self._writer.close()
