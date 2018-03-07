import asyncore
import socket

from SignalValidator import SignalValidator
from logger import Logger


class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            data.decode("utf-8")
            message = str(data)
            print("Message: ", message)
            sig.collect_signals(message)
            if str(data) == "close":
                print("disconnected")
                self.close()

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("Listening on: ", host, port)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

logger = Logger()
server = EchoServer('192.168.1.27', 5000)
sig = SignalValidator(logger)
asyncore.loop()
