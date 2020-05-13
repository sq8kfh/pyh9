import urllib.request

import pytest
from lxml import etree

from h9.msg import H9Error


@pytest.fixture
def h9msg_schema():
    response = urllib.request.urlopen('https://raw.githubusercontent.com/sq8kfh/h9/master/protocol/h9msg.xsd')
    return response.read()


def test_H9Error_with_msg_schema(h9msg_schema):
    frame = H9Error(1, 'test', 'test desc')
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9Error_schema(h9msg_schema):
    frame = H9Error(1, 'test')
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message
