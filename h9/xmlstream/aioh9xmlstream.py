import asyncio
import struct
from ..xmlmsg import h9XMLmsg


class aioh9XMLStream:
    def __init__(self, host, port, loop):
        self._host = host
        self._port = port
        self._loop = loop or asyncio.get_event_loop()
        self._reader = None
        self._writer = None

    def send_message(self, h9msg):
        self._send(h9msg.to_string())

    def connection_made(self):
        pass

    async def message_received(self, h9msg):
        raise NotImplementedError(
            "message_received must be overriden"
        )

    def _send(self, data):
        self._writer.write(struct.pack("!I", len(data)))
        self._writer.write(data)

    async def run(self):
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port, loop=self._loop)
        self.connection_made()

        while True:
            tmp = await self._reader.readexactly(4)
            length = struct.unpack("!I", tmp)[0]

            data = await self._reader.readexactly(length)
            msg = h9XMLmsg.parse_xml(data)
            await self.message_received(msg)
