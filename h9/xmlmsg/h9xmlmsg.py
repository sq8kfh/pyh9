from lxml import etree


class h9XMLmsg:
    H9_XMLMSG_UNKNOWN = 0
    H9_XMLMSG_METHODCALL = 1
    H9_XMLMSG_METHODRESPONSE = 2
    H9_XMLMSG_SENDMSG = 3
    H9_XMLMSG_MSG = 4
    H9_XMLMSG_SUBSCRIBE = 5
    H9_XMLMSG_UNSUBSCRIBE = 6

    type = H9_XMLMSG_UNKNOWN

    @staticmethod
    def create_h9methodCall():
        pass

    @staticmethod
    def create_h9methodResponse():
        pass

    @staticmethod
    def create_h9subscribe(event_name):
        from .h9subscribe import h9subscribe
        return h9subscribe(event_name)

    @staticmethod
    def create_h9unsubscribe(event_name):
        from .h9subscribe import h9subscribe
        return h9subscribe(event_name, unsubscribe=True)

    @staticmethod
    def create_h9sendmsg():
        from .h9msg import h9msg
        return h9msg('a', send=True)

    @staticmethod
    def create_h9msg():
        from .h9msg import h9msg
        return h9msg('a')

    @staticmethod
    def parse_xml(xml):
        root = etree.fromstring(xml)
        if root.tag == "h9methodCall":
            pass
        elif root.tag == "h9methodResponse":
            pass
        elif root.tag == "h9subscribe":
            pass
        elif root.tag == "h9unsubscribe":
            pass
        elif root.tag == "h9sendmsg":
            from .h9msg import h9msg
            return h9msg.create_from_xml_node(root)
        elif root.tag == "h9msg":
            from .h9msg import h9msg
            return h9msg.create_from_xml_node(root)
