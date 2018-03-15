from echoClient import EchoClient
from logger import Logger
import asyncore
import sys

message = sys.argv[1]



if __name__ == '__main__':
    try:
        logger = Logger()
        log = logger.get_logger()
        client = EchoClient("localhost", 5000, message, log)
        asyncore.loop()

    except KeyboardInterrupt:
        print '    Interrupted'
        client.close()
        try:
            sys.exit(0)
            client.close()
        except SystemExit:
            os._exit(0)
