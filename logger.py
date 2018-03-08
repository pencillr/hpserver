import datetime
import time
import random
import string
import logging

class Logger:

    def __init__(self):
        logging.basicConfig(filename=self.generate_logfilename(), format="%(asctime)s - %(levelname)s - %(message)s")
        self.log = logging.getLogger("CORE_LOGGER")
        self.log.setLevel(logging.DEBUG)


    def generate_logfilename(self):
        ts = time.time()
        time_postfix = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
        log_postfix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        return '/tmp/gamelog/log.' + time_postfix + "." + log_postfix

    def get_logger(self):
        return self.log




#logger = Logger()
#logger.logger.debug("debug message")
#logger.logger.info("info message")
#logger.logger.warn("warn message")
#logger.logger.error("error message")
#logger.logger.critical("critical message")
