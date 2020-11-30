import lxml.etree
from .common import Common


class CommonDevice(Common):
    @property
    def device_id(self) -> int:
        return int(self._xml[0].attrib.get("device-id"))

    @device_id.setter
    def device_id(self, value: int):
        self._xml[0].attrib['device-id'] = str(value)

    def to_dict(self):
        res = super(CommonDevice, self).to_dict()
        res['device_id'] = self.device_id
        return res


class CommonDeviceMethod(CommonDevice):
    @property
    def method(self) -> str:
        return str(self._xml[0].attrib.get("method"))

    @method.setter
    def method(self, value: str):
        self._xml[0].attrib['method'] = str(value)

    def to_dict(self):
        res = super(CommonDeviceMethod, self).to_dict()
        res['method'] = self.method
        return res


class H9ExecuteDeviceMethod(CommonDeviceMethod):
    def __init__(self, device_id, method):
        super(H9ExecuteDeviceMethod, self).__init__()
        lxml.etree.SubElement(self._xml, 'execute')
        self.device_id = device_id
        self.method = method
        self.value = dict()


class H9DeviceMethodResponse(CommonDeviceMethod):
    def __init__(self, device_id, method):
        super(H9DeviceMethodResponse, self).__init__()
        lxml.etree.SubElement(self._xml, 'response')
        self.device_id = device_id
        self.method = method
        self.value = dict()

    @property
    def execute_status(self) -> bool:
        return str(self._xml[0].attrib.get('execute-status')) == 'OK'

    @execute_status.setter
    def execute_status(self, value: bool):
        if value:
            self._xml[0].attrib['execute-status'] = 'OK'
        else:
            self._xml[0].attrib['execute-status'] = 'FAIL'

    def to_dict(self):
        res = super().to_dict()
        res['execute_status'] = self.execute_status
        return res


class H9DeviceEvent(CommonDevice):
    def __init__(self, device_id, event):
        super(H9DeviceEvent, self).__init__()
        lxml.etree.SubElement(self._xml, 'event')
        self.device_id = device_id
        self.event = event
        self.value = dict()

    @property
    def event(self) -> str:
        return str(self._xml[0].attrib.get("event"))

    @event.setter
    def event(self, value: str):
        self._xml[0].attrib['event'] = str(value)

    def to_dict(self):
        res = super().to_dict()
        res['event'] = self.event
        return res
