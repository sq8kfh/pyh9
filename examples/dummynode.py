import asyncio

import h9.asyncmsgstream
from h9.msg import H9Subscribe, H9msg, H9SendFrame, H9Frame

node_id = 32

seqnum = -1
reg_10 = 0

def get_next_seqnum():
    global seqnum
    seqnum = seqnum + 1
    seqnum = seqnum % 32
    return seqnum


def procces_frame(conn, frame):
    global reg_10
    print(frame.frametype)
    if frame.frametype == H9Frame.FrameType.GET_REG:
        if frame.data[0] == 10:
            res = H9SendFrame(priority=H9SendFrame.Priority.L,
                                frametype=H9SendFrame.FrameType.REG_VALUE, seqnum=frame.seqnum,
                                source=node_id,
                                destination=frame.source, data=[frame.data[0], reg_10])
            conn.writemsg(res)
    elif frame.frametype == H9Frame.FrameType.SET_REG:
        if frame.data[0] == 10:
            reg_10 = frame.data[1]
            reg_10 = reg_10 % 9
            res = H9SendFrame(priority=H9SendFrame.Priority.L,
                              frametype=H9SendFrame.FrameType.REG_EXTERNALLY_CHANGED, seqnum=frame.seqnum,
                              source=node_id,
                              destination=frame.source, data=[frame.data[0], reg_10])
            conn.writemsg(res)


async def run():
    conn = h9.asyncmsgstream.H9msgStream("127.0.0.1", 7878)
    await conn.connect()
    msg = H9Subscribe(H9Subscribe.Content.FRAME)
    conn.writemsg(msg)

    frame = H9SendFrame(priority=H9SendFrame.Priority.L,
                        frametype=H9SendFrame.FrameType.NODE_TURNED_ON, seqnum=get_next_seqnum(),
                        source=node_id,
                        destination=511, data=['0', '3', '0', '1'])
    conn.writemsg(frame)
    while True:
        recv_msg = await conn.readmsg()
        if isinstance(recv_msg, H9Frame) and (recv_msg.destination == node_id or recv_msg.destination == 511):
            procces_frame(conn, recv_msg)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
finally:
    loop.close()
