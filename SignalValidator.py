

class SignalValidator:

    def __init__(self, logger):
        self.__signal_queue = []
        self.logger = logger


    def collect_signals(self, signal):
        #validate signal
        self.__signal_queue.append(signal)
        self.logger.log.info("Appended: %s", signal)
        print(self.__signal_queue)

    def get_signal_queue(self):
        return self.__signal_queue
