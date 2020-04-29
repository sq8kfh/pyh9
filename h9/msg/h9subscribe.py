from enum import Enum
import lxml.etree
from .h9msg import H9msg

class H9subscribe(H9msg):
    class Content(Enum):
        FRAME = 1
    CONTENT_FRAME = 1
    def __init__(self, content: Content):
        super(H9subscribe, self).__init__(None)

        content_str = content.name
        self._xml.append(lxml.etree.Element('subscribe', content=content_str))

    @property
    def content(self) -> str:
        return self._xml[0].attrib.get("content")

    #def to_bytes(self) -> bytes:
    #    return '<h9 version="0.0"><subscribe content="FRAME"/></h9>'.encode()
