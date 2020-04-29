import struct
from .h9msg import H9msg

class H9frame(H9msg):
    def __init__(self):
        pass

    @property
    def priority(self) -> str:
        return self._xml[0].attrib.get("priority")

    @property
    def type(self) -> int:
        return int(self._xml[0].attrib.get("type"))

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
        hexstring = self._xml[0].attrib.get("data")
        return struct.unpack('<%dB' % self.dlc, bytes.fromhex(hexstring))

    def to_dict(self):
        return dict(priority = self.priority, type=self.type, seqnum=self.seqnum, source=self.source, destination=self.destination, dlc=self.dlc, data=self.data)
