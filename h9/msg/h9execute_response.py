import lxml.etree

from .h9msg import H9msg


class _Common(H9msg):
    def _dump(self, node, res):
        if isinstance(res, dict):
            for n in node:
                if n.tag == 'value':
                    res[n.attrib['name']] = n.text
                elif n.tag == 'dict':
                    tmp = {}
                    self._dump(n, tmp)
                    res[n.attrib['name']] = tmp
                elif n.tag == 'array':
                    tmp = []
                    self._dump(n, tmp)
                    res[n.attrib['name']] = tmp
        elif isinstance(res, list):
            for n in node:
                if n.tag == 'value':
                    res.append(n.text)
                elif n.tag == 'dict':
                    tmp = {}
                    self._dump(n, tmp)
                    res.append(tmp)
                elif n.tag == 'array':
                    tmp = []
                    self._dump(n, tmp)
                    res.append(tmp)
        return res

    def _to_xml(self, value, name=None):
        res = None
        if isinstance(value, list):
            if name:
                res = lxml.etree.Element("array", name=name)
            else:
                res = lxml.etree.Element("array")
            for v in value:
                res.append(self._to_xml(v))
        elif isinstance(value, dict):
            if name:
                res = lxml.etree.Element("dict", name=name)
            else:
                res = lxml.etree.Element("dict")
            for k, v in value.items():
                res.append(self._to_xml(v, k))
        elif name:
            res = lxml.etree.Element("value", name=name)
            res.text = str(value)
        else:
            res = lxml.etree.Element("value")
            res.text = str(value)
        return res

    @property
    def method(self) -> str:
        return str(self._xml[0].attrib.get("method"))

    @method.setter
    def method(self, value: str):
        self._xml[0].attrib['method'] = str(value)

    @property
    def value(self) -> dict:
        res = {}
        self._dump(self._xml[0], res)
        return res

    @value.setter
    def value(self, value: dict):
        if not value:
            for child in self._xml[0]:
                self._xml[0].remove(child)
        else:
            for k, v in value.items():
                self._xml[0].append(self._to_xml(v, k))

    def to_dict(self):
        res = dict(method=self.method)
        if self.value:
            res['value'] = self.value
        return res


class H9ExecuteMethod(_Common):
    def __init__(self, method, parameters=None):
        super(H9ExecuteMethod, self).__init__()
        lxml.etree.SubElement(self._xml, 'execute')
        self.method = method
        if isinstance(parameters, dict):
            self.value = parameters
        else:
            self.value = dict()


class H9MethodResponse(_Common):
    def __init__(self, method):
        super(H9MethodResponse, self).__init__()
        lxml.etree.SubElement(self._xml, 'response')
        self.method = method
        self.value = dict()


class H9ExecuteDeviceMethod(_Common):
    def __init__(self, id, method):
        super(H9ExecuteDeviceMethod, self).__init__()
        lxml.etree.SubElement(self._xml, 'execute')
        self.id = id
        self.method = method
        self.value = dict()

    @property
    def id(self) -> int:
        return int(self._xml[0].attrib.get("id"))

    @id.setter
    def id(self, value: int):
        self._xml[0].attrib['id'] = str(value)


class H9DeviceMethodResponse(_Common):
    def __init__(self, id, method):
        super(H9DeviceMethodResponse, self).__init__()
        lxml.etree.SubElement(self._xml, 'response')
        self.id = id
        self.method = method
        self.value = dict()

    @property
    def id(self) -> int:
        return int(self._xml[0].attrib.get("id"))

    @id.setter
    def id(self, value: int):
        self._xml[0].attrib['id'] = str(value)
