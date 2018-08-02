from . import h9XMLmsg
from lxml import etree


class h9subscribe(h9XMLmsg):
    @staticmethod
    def create_from_xml_node(xml):
        if xml.tag == "h9unsubscribe":
            return h9subscribe(xml.attrib["event"], unsubscribe=True)
        elif xml.tag == "h9subscribe":
            return h9subscribe(xml.attrib["event"])

    def __init__(self, event_name, unsubscribe=False):
        super().__init__()
        self._unsubscribe = unsubscribe
        self._event_name = event_name
        if unsubscribe:
            self.type = h9XMLmsg.H9_XMLMSG_UNSUBSCRIBE
        else:
            self.type = h9XMLmsg.H9_XMLMSG_SUBSCRIBE

    def to_string(self):
        if self._unsubscribe:
            root = etree.Element("h9unsubscribe", event=self._event_name)
        else:
            root = etree.Element("h9subscribe", event=self._event_name)
        return etree.tostring(root)
