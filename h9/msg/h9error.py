import lxml.etree
from .h9msg import H9msg


class H9Error(H9msg):
    def __init__(self, errnum: int, name: str = None, msg: str = None):
        super(H9Error, self).__init__()
        lxml.etree.SubElement(self._xml, 'error')
        self.errnum = errnum
        self.name = name
        self.msg = msg

    @property
    def errnum(self) -> int:
        return int(self._xml[0].attrib.get("errnum"))

    @property
    def name(self) -> str:
        return str(self._xml[0].attrib.get("name"))

    @property
    def msg(self) -> str:
        return str(self._xml[0].attrib.get("msg"))

    @errnum.setter
    def errnum(self, value: int):
        self._xml[0].attrib['errnum'] = str(value)

    @name.setter
    def name(self, value: str):
        if not value:
            if 'name' in self._xml[0].attrib:
                del self._xml[0].attrib['name']
        else:
            self._xml[0].attrib['name'] = str(value)

    @msg.setter
    def msg(self, value: str):
        if not value:
            if 'msg' in self._xml[0].attrib:
                del self._xml[0].attrib['msg']
        else:
            self._xml[0].attrib['msg'] = str(value)
