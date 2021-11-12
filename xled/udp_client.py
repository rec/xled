from dataclasses import dataclass
from functools import cached_property
from xled.exceptions import ReceiveTimeout
import socket

DEFAULT_BROADCAST = '255.255.255.255'


@dataclass
class UDPClient:
    port: int
    host: str = ''
    timeout: float = 0
    broadcast: bool = False

    def __post_init__(self):
        if not (self.host or self.broadcast):
            raise ValueError('One of host or broadcast must be set')
        self.host = self.host or DEFAULT_BROADCAST

    @cached_property
    def _handle(self):
        handle = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        if self.broadcast:
            _handle.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        handle.bind(('', self.port))
        if self.timeout:
            handle.settimeout(self.timeout)
        return handle

    @cached_property
    def _own_addresses(self):
        addr = socket.gethostbyname_ex(socket.gethostname())[-1]
        return [a for a in addr if not a.startswith('127.')]

    def close(self):
        self.handle.close()

    def send(self, message):
        return self.handle.sendto(message, 0, (self.host, self.port))

    def recv(self, bufsize):
        """
        Blocks until message is received

        Skips messages received from any address stored in
        :py:attr:`own_addresses`.

        :param int bufsize: the maximum amount of data to be received at once
        :return: received message, sender address
        :rtype: tuple
        """
        while True:
            try:
                buf, (host, port) = self.handle.recvfrom(bufsize)
            except socket.timeout:
                raise ReceiveTimeout from None
            else:
                if host not in self._own_addresses:
                    return buf, host
