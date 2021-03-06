import asyncore
import random
import string
import socket
import os
import sys

from logger import Logger
from signal_validator import SignalValidator
import db_manager

class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """

    def __init__(self, address, logger, sig):
        self.logger = logger
        self.sig = sig
        asyncore.dispatcher.__init__(self)
        self.database = ''
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(5)
        self._set_db()
        print("Listening on: ", self.address)
        return

    def _set_db(self):
        self.logger.info('Creating Database: %s', self.database)
        dbname_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        dbname_postfix = '_test.db'
        self.database = dbname_prefix + dbname_postfix
        db_manager.init_db(self.database)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        self.logger.debug('handle_accept() -> %s', client_info[1])
        EchoHandler(sock=client_info[0], logger=self.logger, sig=self.sig)
        # We only want to deal with one client at a time,
        # so close as soon as we set up the handler.
        # Normally you would not do this and the server
        # would run forever or until it received instructions
        # to stop.
        #self.handle_close()
        return

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        return

class EchoHandler(asyncore.dispatcher):
    """Handles echoing messages from a single client.
    """

    def __init__(self, sock, logger, sig, chunk_size=256):
        self.chunk_size = chunk_size
        self.logger = logger
        self.sig = sig
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_write = []
        self.sig.set_responder(self)
        return

    def writable(self):
        """We want to write if we have received data."""
        response = bool(self.data_to_write)
        self.logger.debug('writable() -> %s', response)
        return response

    def handle_write(self):
        """Write as much as possible of the most recent message we have received."""
        data = self.data_to_write.pop()
        sent = self.send(data[:self.chunk_size])
        if sent < len(data):
            remaining = data[sent:]
            self.data.to_write.append(remaining)
        self.logger.debug('handle_write() -> (%d) "%s"', sent, data[:sent])
        if not self.writable():
            self.handle_close()

    def handle_read(self):
        data = self.recv(self.chunk_size)
        if data:
            self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
            #self.data_to_write.insert(0, data)
            data.decode("utf-8")
            message = str(data)
            print("Message: ", message)
            self.sig.examine_signals(message)
            #self.data_to_write.insert(0, message)

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()


class EchoClient(asyncore.dispatcher):
    """Sends messages to the server and receives responses.
    """

    def __init__(self, host, port, message, logger, chunk_size=512):
        self.message = message
        self.to_send = message
        self.received_data = []
        self.chunk_size = chunk_size
        self.logger = logger
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.connect((host, port))
        return

    def handle_connect(self):
        self.logger.debug('handle_connect()')

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY OF MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED "%s"', self.message)
            self.logger.debug('RECEIVED "%s"', received_message)
        return

    def writable(self):
        self.logger.debug('writable() -> %s', bool(self.to_send))
        return bool(self.to_send)

    def handle_write(self):
        sent = self.send(self.to_send[:self.chunk_size])
        self.logger.debug('handle_write() -> (%d) "%s"', sent, self.to_send[:sent])
        self.to_send = self.to_send[sent:]

    def handle_read(self):
        data = self.recv(self.chunk_size)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
        self.received_data.append(data)
        print(data)


if __name__ == '__main__':
    try:
        logger = Logger()
        log = logger.get_logger()
        sig = SignalValidator(logger)

        address = ('localhost', 5000) # let the kernel give us a port
        server = EchoServer(address, log, sig)
        ip, port = server.address # find out what port we were given

        #client = EchoClient(ip, port, message, log)

        asyncore.loop()
    except KeyboardInterrupt:
        print '    Interrupted'
        db_manager.close_all()
        try:
            sys.exit(0)
            db_manager.close_all()
        except SystemExit:
            os._exit(0)
