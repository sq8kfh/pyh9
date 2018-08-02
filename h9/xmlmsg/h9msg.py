from .h9xmlmsg import h9XMLmsg


class h9msg(h9XMLmsg):
    @staticmethod
    def create_from_xml_node(xml):
        if xml.tag == "h9sendmsg":
            return h9msg(**xml.attrib, send=True)
        elif xml.tag == "h9msg":
            return h9msg(**xml.attrib)

    def __init__(self, type, source, destination, dlc=0, data=None, priority='L', endpoint=None, send=False):
        super().__init__()
        if send:
            self.type = h9XMLmsg.H9_XMLMSG_SENDMSG
        else:
            self.type = h9XMLmsg.H9_XMLMSG_MSG

        self._endpoint = endpoint
        self._priority = priority
        self._type = int(type)
        self._source = int(source)
        self._destination = int(destination)
        self._dlc = int(dlc)
        self._data = data

    def __str__(self):
        return "%d -> %d priority: %c; type: %d; dlc: %d; endpoint '%s'" % (self._source, self._destination, self._priority, self._type, self._dlc, self._endpoint)
