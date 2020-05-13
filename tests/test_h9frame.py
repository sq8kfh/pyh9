import urllib.request

import pytest
from lxml import etree

from h9.msg import H9Frame, H9SendFrame


@pytest.fixture
def h9msg_schema():
    response = urllib.request.urlopen('https://raw.githubusercontent.com/sq8kfh/h9/master/protocol/h9msg.xsd')
    return response.read()


def test_H9frame_to_dict():
    exp_dict = {'priority': 'H', 'type': 17, 'source': 1, 'seqnum': 12, 'destination': 7,
                'dlc': 1, 'data': (10, ), 'origin': 'can0'}
    frame = H9Frame('can0', H9Frame.Priority.H, H9Frame.FrameType.GET_REG, 12, 1, 7, ['0a'])
    assert frame.to_dict() == exp_dict


def test_H9frame_with_endpoint_to_dict():
    exp_dict = {'priority': 'H', 'type': 17, 'source': 1, 'seqnum': 12, 'destination': 7,
                'dlc': 1, 'data': (10, ), 'endpoint': 'can2', 'origin': 'can0'}
    frame = H9Frame('can0', H9Frame.Priority.H, H9Frame.FrameType.GET_REG, 12, 1, 7, ['0a'], 'can2')
    assert frame.to_dict() == exp_dict


def test_H9frame_schema(h9msg_schema):
    frame = H9Frame('can0', H9Frame.Priority.H, H9Frame.FrameType.GET_REG, 12, 1, 7, ['0a'])
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9frame_with_endpoint_schema(h9msg_schema):
    frame = H9Frame('can0', H9Frame.Priority.H, H9Frame.FrameType.GET_REG, 12, 1, 7, ['0a'], 'can2')
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9frame_with_empty_data_schema(h9msg_schema):
    frame = H9Frame('can0', H9Frame.Priority.H, H9Frame.FrameType.GET_REG, 12, 1, 7, [])
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9SendFrame_to_dict():
    exp_dict = {'priority': 'H', 'type': 17, 'source': 1, 'seqnum': 12, 'destination': 7,
                'dlc': 1, 'data': (10, )}
    frame = H9SendFrame(H9SendFrame.Priority.H, H9SendFrame.FrameType.GET_REG, 12, 1, 7, ['0a'])
    assert frame.to_dict() == exp_dict


def test_H9SendFrame_with_endpoint_to_dict():
    exp_dict = {'priority': 'H', 'type': 17, 'source': 1, 'seqnum': 12, 'destination': 7,
                'dlc': 1, 'endpoint': 'can1', 'data': (10, )}
    frame = H9SendFrame(H9SendFrame.Priority.H, H9SendFrame.FrameType.GET_REG, 12, 1, 7, ['0a'], 'can1')
    assert frame.to_dict() == exp_dict


def test_H9SendFrame_schema(h9msg_schema):
    frame = H9SendFrame(H9SendFrame.Priority.H, H9SendFrame.FrameType.GET_REG, 12, 1, 7, ['0a'])
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9SendFrame_with_endpoint_schema(h9msg_schema):
    frame = H9SendFrame(H9SendFrame.Priority.H, H9SendFrame.FrameType.GET_REG, 12, 1, 7, ['0a'], 'can1')
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message


def test_H9SendFrame_with_empty_data_schema(h9msg_schema):
    frame = H9SendFrame(H9SendFrame.Priority.H, H9SendFrame.FrameType.GET_REG, 12, 1, 7, ['0a'])
    xmlschema_doc = etree.fromstring(h9msg_schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.fromstring(frame.to_bytes())
    assert xmlschema.validate(xml_doc), xmlschema.error_log.last_error.message
