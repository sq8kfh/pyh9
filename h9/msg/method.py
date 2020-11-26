import lxml.etree
from .common import Common


class CommonMethod(Common):
    @property
    def method(self) -> str:
        return str(self._xml[0].attrib.get("method"))

    @method.setter
    def method(self, value: str):
        self._xml[0].attrib['method'] = str(value)

    def to_dict(self):
        res = super().to_dict()
        res['method'] = self.method
        return res


class H9ExecuteMethod(CommonMethod):
    def __init__(self, method, parameters=None):
        super(H9ExecuteMethod, self).__init__()
        lxml.etree.SubElement(self._xml, 'execute')
        self.method = method
        if isinstance(parameters, dict):
            self.value = parameters
        else:
            self.value = dict()


class H9MethodResponse(CommonMethod):
    def __init__(self, method):
        super(H9MethodResponse, self).__init__()
        lxml.etree.SubElement(self._xml, 'response')
        self.method = method
        self.value = dict()
