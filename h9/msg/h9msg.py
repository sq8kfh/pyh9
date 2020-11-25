from enum import Enum

import lxml.etree


class H9msg:
    next_id = 1
    class MsgType(Enum):
        UNKNOWN = 0
        IDENTIFICATION = 1
        FRAME = 2
        SEND_FRAME = 3
        SUBSCRIBE = 4
        ERROR = 5
        EXECUTEMETHOD = 6
        METHODRESPONSE = 7
        EXECUTEDEVICEMETHOD = 8
        DEVICEMETHODRESPONSE = 9


    def __init__(self, xml_node: lxml.etree = None):
        if xml_node is None:
            self._xml = lxml.etree.Element('h9', version='0.0', id=str(H9msg.next_id))
            H9msg.next_id = H9msg.next_id + 1
        else:
            self._xml = xml_node

    @property
    def msg_type(self):
        if self._xml.tag != 'h9' and len(self._xml) != 1:
            return H9msg.MsgType.UNKNOWN

        if self._xml[0].tag == 'identification':
            return H9msg.MsgType.IDENTIFICATION
        elif self._xml[0].tag == 'frame':
            return H9msg.MsgType.FRAME
        elif self._xml[0].tag == 'send_frame':
            return H9msg.MsgType.SEND_FRAME
        elif self._xml[0].tag == 'subscribe':
            return H9msg.MsgType.SUBSCRIBE
        elif self._xml[0].tag == 'error':
            return H9msg.MsgType.ERROR
        elif self._xml[0].tag == 'execute':
            if self._xml[0].attrib.get('id'):
                return H9msg.MsgType.EXECUTEDEVICEMETHOD
            else:
                return H9msg.MsgType.EXECUTEMETHOD
        elif self._xml[0].tag == 'response':
            if self._xml[0].attrib.get('id'):
                return H9msg.MsgType.DEVICEMETHODRESPONSE
            else:
                return H9msg.MsgType.METHODRESPONSE
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

    if msg.msg_type == H9msg.MsgType.IDENTIFICATION:
        from .h9frame import H9Identification
        msg.__class__ = H9Identification
        return msg
    elif msg.msg_type == H9msg.MsgType.FRAME:
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
    elif msg.msg_type == H9msg.MsgType.EXECUTEMETHOD:
        from .h9execute_response import H9ExecuteMethod
        msg.__class__ = H9ExecuteMethod
        return msg
    elif msg.msg_type == H9msg.MsgType.METHODRESPONSE:
        from .h9execute_response import H9MethodResponse
        msg.__class__ = H9MethodResponse
        return msg
    return None
