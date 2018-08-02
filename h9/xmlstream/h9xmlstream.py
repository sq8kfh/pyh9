import struct
import socket
from ..xmlmsg import h9XMLmsg


class h9XMLStream:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))

    def send_message(self, h9msg):
        self._send(h9msg.to_string())

    def _send(self, data):
        self._sock.send(struct.pack("!I", len(data)))
        self._sock.send(data)

    def read_message(self):
        tmp = self._recv(4)
        length = struct.unpack("!I", tmp)[0]

        data = self._recv(length)
        msg = h9XMLmsg.parse_xml(data)
        return msg

    def _recv(self, length):
        chunks = []
        bytes_recd = 0
        while bytes_recd < length:
            chunk = self._sock.recv(min(length - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)