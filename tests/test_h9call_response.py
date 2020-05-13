import urllib.request

import pytest
from lxml import etree

from h9.msg import H9Call, H9Response


@pytest.fixture
def h9msg_schema():
    response = urllib.request.urlopen('https://raw.githubusercontent.com/sq8kfh/h9/master/protocol/h9msg.xsd')
    return response.read()


def test_H9Call_to_dict():
    exp_dict = dict(method='test', value={'a': '1', 'b': ['1', '2']})
    frame = H9Call('test')
    frame.value = {'a': 1, 'b': [1, 2]}
    assert frame.to_dict() == exp_dict


def test_H9Call_schema(h9msg_schema):
    frame = H9Call('test')
    frame.value = {'a': 1, 'b': [1, 2]}
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9Response_to_dict():
    exp_dict = dict(method='test', value={'a': '1', 'b': ['1', '2']})
    frame = H9Response('test')
    frame.value = {'a': 1, 'b': [1, 2]}
    assert frame.to_dict() == exp_dict


def test_H9Response_delete_value():
    exp_dict = dict(method='test')
    frame = H9Response('test')
    frame.value = {'a': 1, 'b': [1, 2]}
    frame.value = {}
    assert frame.to_dict() == exp_dict


def test_H9Response_schema(h9msg_schema):
    frame = H9Response('test')
    frame.value = {'a': 1, 'b': [1, 2]}
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message
