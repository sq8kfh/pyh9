import asyncio

import h9.asyncmsgstream
from h9.msg import H9Subscribe


async def run():
    conn = h9.asyncmsgstream.H9msgStream("127.0.0.1", 7878)
    await conn.connect()
    msg = H9Subscribe(H9Subscribe.Content.FRAME)
    conn.writemsg(msg)
    while True:
        recv_msg = await conn.readmsg()
        print(recv_msg)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
finally:
    loop.close()
