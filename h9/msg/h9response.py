import lxml.etree
from .h9msg import H9msg


class H9Response(H9msg):
    def __init__(self, method):
        super(H9Response, self).__init__()
        lxml.etree.SubElement(self._xml, 'response')
        self.method = method
        self.value = dict()

    @property
    def method(self) -> str:
        return str(self._xml[0].attrib.get("method"))

    @method.setter
    def method(self, value: str):
        self._xml[0].attrib['method'] = str(value)

    def _dump(self, node, res):
        for n in node:
            if n.tag == 'value':
                res[n.attrib['name']] = n.text
            elif n.tag == 'array':
                tmp = {}
                self._dump(n, tmp)
                res[n.attrib['name']] = tmp
        return res

    @property
    def value(self) -> dict:
        res = {}
        self._dump(self._xml[0], res)
        return res

    @value.setter
    def value(self, value: dict):
        self._xml[0].attrib['method'] = str(value)

    def to_dict(self):
        res = dict(method=self.method, value=self.value)
        return res

