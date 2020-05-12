import lxml.etree
from enum import Enum


class H9msg:
    class MsgType(Enum):
        UNKNOWN = 0
        FRAME = 1
        SEND_FRAME = 2
        SUBSCRIBE = 3
        ERROR = 4
        CALL = 5
        RESPONSE = 6

    def __init__(self, xml_node: lxml.etree = None):
        if xml_node is None:
            self._xml = lxml.etree.Element('h9', version='0.0')
        else:
            self._xml = xml_node

    @property
    def msg_type(self):
        if self._xml.tag != 'h9' and len(self._xml) != 1:
            return H9msg.MsgType.UNKNOWN

        if self._xml[0].tag == 'frame':
            return H9msg.MsgType.FRAME
        elif self._xml[0].tag == 'send_frame':
            return H9msg.MsgType.SEND_FRAME
        elif self._xml[0].tag == 'subscribe':
            return H9msg.MsgType.SUBSCRIBE
        elif self._xml[0].tag == 'error':
            return H9msg.MsgType.ERROR
        elif self._xml[0].tag == 'call':
            return H9msg.MsgType.CALL
        elif self._xml[0].tag == 'response':
            return H9msg.MsgType.RESPONSE
        else:
            return H9msg.MsgType.UNKNOWN

    @property
    def msg_version(self):
        return self._xml.attrib.get('version')

    def __str__(self):
        return lxml.etree.tostring(self._xml, method='c14n2', strip_text=True).decode()

    def to_bytes(self) -> bytes:
        return lxml.etree.tostring(self._xml)


def xml_to_h9msg(xml: str):
    root = lxml.etree.fromstring(xml)
    msg = H9msg(root)

    if msg.msg_type == H9msg.MsgType.FRAME:
        from .h9frame import H9Frame
        msg.__class__ = H9Frame
        return msg
    elif msg.msg_type == H9msg.MsgType.SEND_FRAME:
        from .h9frame import H9SendFrame
        msg.__class__ = H9SendFrame
        return msg
    elif msg.msg_type == H9msg.MsgType.SUBSCRIBE:
        from .h9subscribe import H9Subscribe
        msg.__class__ = H9Subscribe
        return msg
    elif msg.msg_type == H9msg.MsgType.ERROR:
        from .h9error import H9Error
        msg.__class__ = H9Error
        return msg
    elif msg.msg_type == H9msg.MsgType.CALL:
        from .h9call_response import H9Call
        msg.__class__ = H9Call
        return msg
    elif msg.msg_type == H9msg.MsgType.RESPONSE:
        from .h9call_response import H9Response
        msg.__class__ = H9Response
        return msg
    return None
