import lxml.etree


class H9msg:
    H9MSG_UNKNOWN = 0
    H9MSG_FRAME = 1
    H9MSG_SEND_FRAME = 2
    H9MSG_SUBSCRIBE = 3
    H9MSG_ERROR = 4
    H9MSG_METHODCALL = 5
    H9MSG_METHODRESPONSE = 6

    def __init__(self, xml_node: lxml.etree):
        if xml_node is None:
            self._xml = lxml.etree.Element('h9', version='0.0')
        else:
            self._xml = xml_node

    @property
    def msg_type(self):
        if self._xml.tag != 'h9' and len(self._xml) != 1:
            return H9msg.H9MSG_UNKNOWN

        if self._xml[0].tag == 'frame_received':
            return H9msg.H9MSG_FRAME
        elif self._xml[0].tag == 'send_frame':
            return  H9msg.H9MSG_SEND_FRAME
        elif self._xml[0].tag == 'subscribe':
            return  H9msg.H9MSG_SUBSCRIBE
        elif self._xml[0].tag == 'error':
            return  H9msg.H9MSG_ERROR
        elif self._xml[0].tag == 'methodcall':
            return  H9msg.H9MSG_METHODCALL
        elif self._xml[0].tag == 'methodresponse':
            return  H9msg.H9MSG_METHODRESPONSE
        else:
            return H9msg.H9MSG_UNKNOWN

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

    if msg.msg_type == H9msg.H9MSG_FRAME:
        from .h9frame import H9frame
        msg.__class__ = H9frame
        return msg
    elif msg.msg_type == H9msg.H9MSG_SEND_FRAME:
        pass
    elif msg.msg_type == H9msg.H9MSG_SUBSCRIBE:
        from .h9subscribe import H9subscribe
        msg.__class__ = H9subscribe
        return msg
    elif msg.msg_type == H9msg.H9MSG_ERROR:
        pass
    elif msg.msg_type == H9msg.H9MSG_METHODCALL:
        pass
    elif msg.msg_type == H9msg.H9MSG_METHODRESPONSE:
        pass

    return None
