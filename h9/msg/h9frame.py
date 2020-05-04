import struct
import lxml.etree
from enum import Enum
from .h9msg import H9msg


class H9frame(H9msg):
    class Priority(Enum):
        H = 0
        L = 1


    class Type(Enum):
        NOP = 0
        PAGE_START = 1
        QUIT_BOOTLOADER = 2
        PAGE_FILL = 3
        BOOTLOADER_TURNED_ON = 4
        PAGE_FILL_NEXT = 5
        PAGE_WRITED = 6
        PAGE_FILL_BREAK = 7
        REG_EXTERNALLY_CHANGED = 8
        REG_INTERNALLY_CHANGED = 9
        REG_VALUE_BROADCAST = 10
        REG_VALUE = 11
        NODE_HEARTBEAT = 12
        ERROR = 13
        NODE_TURNED_ON = 14
        U15 = 15
        SET_REG = 16
        GET_REG = 17
        NODE_INFO = 18
        U19 = 19
        NODE_UPGRADE = 20
        U21 = 21
        U22 = 22
        U23 = 23
        DISCOVERY = 24
        NODE_RESET = 25
        U26 = 26
        U27 = 27
        U28 = 28
        U29 = 29
        U30 = 30
        U31 = 31


    def __init__(self, priority: Priority, type: Type, seqnum: int, source: int, destination: int, data: []):
        super(H9frame, self).__init__()
        lxml.etree.SubElement(self._xml, 'send_frame')
        self.priority = priority
        self.type = type
        self.seqnum = seqnum
        self.source = source
        self.destination = destination
        self.data = data


    @property
    def priority(self) -> Priority:
        return H9frame.Priority[self._xml[0].attrib.get("priority")]


    @property
    def type(self) -> Type:
        return H9frame.Type(int(self._xml[0].attrib.get("type")))


    @property
    def seqnum(self) -> int:
        return int(self._xml[0].attrib.get("seqnum"))


    @property
    def source(self) -> int:
        return int(self._xml[0].attrib.get("source"))


    @property
    def destination(self) -> int:
        return int(self._xml[0].attrib.get("destination"))


    @property
    def dlc(self) -> int:
        return int(self._xml[0].attrib.get("dlc"))


    @property
    def data(self) -> []:
        dlc = self.dlc
        hexstring = self._xml[0].attrib.get("data")
        if dlc < 1 or not hexstring:
            return []
        return struct.unpack('<%dB' % self.dlc, bytes.fromhex(hexstring))


    @priority.setter
    def priority(self, value: Priority):
        self._xml[0].attrib['priority'] = str(value.name)


    @type.setter
    def type(self, value: Type):
        self._xml[0].attrib['type'] = str(value.value)


    @seqnum.setter
    def seqnum(self, value: int):
        if value < 0 or value >31:
            raise ValueError('Seqnum value out of range')
        self._xml[0].attrib['seqnum'] = str(value)


    @source.setter
    def source(self, value: int):
        if value < 0 or value >511:
            raise ValueError('Source value out of range')
        self._xml[0].attrib['source'] = str(value)


    @destination.setter
    def destination(self, value: int):
        if value < 0 or value >511:
            raise ValueError('Destination value out of range')
        self._xml[0].attrib['destination'] = str(value)


    @data.setter
    def data(self, value: []):
        tmpdlc = 0
        tmpdata = ''

        for b in value:
            if b is None or b == '':
                break
            tmpdata = tmpdata + "%0.2X" % int(b, 16)
            tmpdlc = tmpdlc + 1
        self._xml[0].attrib['dlc'] = str(tmpdlc)
        if tmpdlc:
            self._xml[0].attrib['data'] = tmpdata
        else:
            try:
                del self._xml[0].attrib['data']
            except KeyError:
                pass


    def to_dict(self):
        return dict(priority = self.priority.name, type=self.type.value, seqnum=self.seqnum, source=self.source, destination=self.destination, dlc=self.dlc, data=self.data)
