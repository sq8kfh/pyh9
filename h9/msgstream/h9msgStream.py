import socket
import struct


class H9msgStream(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        pass

    def writemsg(self, msg):
        self._sock.send(struct.pack("!I", len(msg)))
        self._sock.sent(msg)

    def readmsg(self):
        tmp = self._recv(4)
        length = struct.unpack("!I", tmp)[0]

        data = self._recv(length)
        return data

    def close(self):
        self._sock.close()

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
