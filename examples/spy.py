from h9.xmlmsg import h9XMLmsg
import h9.xmlstream
import asyncio


class aioh9xml_example (h9.xmlstream.aioh9XMLStream):
    def connection_made(self):
        msg = h9XMLmsg.create_h9subscribe("msg")
        self.send_message(msg)

    def message_received(self, h9msg):
        print(h9msg)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(aioh9xml_example("127.0.0.1", 7878, loop).run())
finally:
    loop.close()
