from socket import *
import logging
import codecs
import traceback

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 8001
ORIGIN_PORT = 8000

ADDRESS = (SERVER_NAME, SERVER_PORT)
ORIGIN_SERVER_ADDRESS = (SERVER_NAME, ORIGIN_PORT)

MAX_PACKET = 32768
HTTP = 'HTTP'

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

logger.info = print
logger.error = print
logger.debug = print


class BSocket(object):
    def __init__(self, sock_addr: tuple):
        self.address = sock_addr

        self._sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

    def recv_all(self) -> str:
        prev_timeout = self._sock.gettimeout()
        try:
            self._sock.settimeout(1)
            rdata = []

            while True:
                try:
                    received = self._sock.recv(MAX_PACKET)
                    logger.info('Received Packet -- ', received)
                    try:
                        rdata.append(received.decode())
                    except UnicodeDecodeError:
                        rdata.append(codecs.decode(received, 'hex'))
                except UnicodeDecodeError:
                    logger.info('Cannot Decode the Packet - UnicodeDecodeError')
                    return ''
                except timeout:
                    return ''.join(rdata)
        finally:
            self._sock.settimeout(prev_timeout)

    def normalize_message(self, msg: str) -> str:
        '''Convert string containing various line endings like \n, \r or \r\n,
        to uniform \n.'''
        return ''.join((line + '\n') for line in msg.splitlines())

    def send(self, message: str):
        self._sock.send(message.encode())

    def close_connection(self):
        self._sock.close()

    def accept_tcp_connection(self):
        sock, addr = self._sock.accept()
        logger.info('Accepting Connection result ===>', sock, addr)

        self._sock = sock
        self.address = addr

    def listen(self, n: int):
        self._sock.listen(n)

    def connect(self, addr: tuple):
        self._sock.connect(addr)


class ProxySocket(BSocket):

    def bind(self, addr: tuple):
        self._sock.bind(addr)

    def __repr__(self):
        return 'ProxyClass' + self._sock.__repr__()


class WebProxy:
    def __init__(self):
        self.proxy_sock = ProxySocket(sock_addr=ADDRESS)
        self.proxy_sock.bind(addr=ADDRESS)
        logger.info('Proxy server ready to accept connections at ', ADDRESS)

        self.origin_sock = ProxySocket(sock_addr=ORIGIN_SERVER_ADDRESS)
        self.origin_sock.connect(ORIGIN_SERVER_ADDRESS)
        logger.info('Connected to Origin Server!!!')

    def receive_web_calls(self):
        self.proxy_sock.listen(1)
        while True:
            logger.info('Server ready to receive messages!!')
            self.proxy_sock.accept_tcp_connection()

            message = self.proxy_sock.recv_all()
            logger.info('Received message ===>', message)
            request = self.proxy_sock.normalize_message(message)

            if self.__is_http_request(request):
                self._forward_http_request(message=message)

    def _forward_http_request(self, message: str):
        logger.info('forwarding http request to origin')
        logger.info(message)
        while True:
            self.origin_sock.send(message=message)
            recv_message = self.origin_sock.recv_all()
            self.proxy_sock.send(message=recv_message)

    @staticmethod
    def __is_http_request(request):
        if HTTP in request:
            return True
        return False


if __name__ == '__main__':
    proxy = WebProxy()
    try:
        proxy.receive_web_calls()
    except:
        error = traceback.format_exc()
        logger.error(error)
        logger.error('Error occured while running main function, Closing all socket connections')
        proxy.proxy_sock.close_connection()
        proxy.origin_sock.close_connection()