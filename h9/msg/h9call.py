import lxml.etree
from .h9msg import H9msg


class H9Call(H9msg):
    def __init__(self, method):
        super(H9Call, self).__init__()
        lxml.etree.SubElement(self._xml, 'call')
        self.method = method
        self.value = {}

    @property
    def method(self) -> str:
        return str(self._xml[0].attrib.get("method"))

    @method.setter
    def method(self, value: str):
        self._xml[0].attrib['method'] = str(value)