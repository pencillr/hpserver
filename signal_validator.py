import db_manager
import string
import time
import datetime

class SignalValidator:

    def __init__(self, logger):
        self.__signal_queue = []
        self.logger = logger


    def examine_signals(self, signal):
        #validate signal
        #self.__signal_queue.append(signal)
        spell_list = ['lumos', 'stupor', 'alohomora']
        self.logger.log.info("Examining: %s", signal)
        #print(self.__signal_queue)
        if "reg_" in signal:
            self.logger.log.info("Registration Signal detected.")
            signal = signal[4:]
            self.register_user(signal)
        elif signal.isdigit():
            self.logger.log.info("Hit Detected.")
            self.validate_hit(signal)
        elif "spell_" in signal:
            self.logger.log.info("Spell Casted.")
            signal = signal[6:]
            self.store_cast(signal)

    def set_responder(self, handler):
        self.responder = handler

    def get_signal_queue(self):
        return self.__signal_queue

    def store_cast(self, signal):
        base = signal
        wand_id, spell =  base.split('_')
        id = int(wand_id)
        ts = time.time()
        time_base = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        timeframe =int(time_base)
        db_manager.store_cast(wand_id, spell, timeframe)
        self.logger.log.info("Spell: %s stored with ID: %d", spell, id)


    def fetch_effect(self, wand_id):
        effect = db_manager.fetch_cast(wand_id)
        self.logger.log.info("Spell Detected: %s", effect)
        warning = "hitby_" + effect
        self.responder.data_to_write.insert(0, warning)

    def register_user(self, reg_string):
        base = reg_string
        name, id, spells = base.split('_')
        #name = base[4:-4]
        spell_collection = []
        self.logger.log.info("    Name: %s", name)
        self.logger.log.info("    ID: %s", id)
        self.logger.log.info("    Spells: %s", spells)
        if 'l' in spells:
            spell_collection.append(1)
        else:
            spell_collection.append(0)
        if 's' in spells:
            spell_collection.append(1)
        else:
            spell_collection.append(0)
        if 'a' in spells:
            spell_collection.append(1)
        else:
            spell_collection.append(0)

        db_manager.register_wiz(id, name, 20, spell_collection[0], spell_collection[1], spell_collection[2])
        self.logger.log.info("Registered %s %d %d %d", name, spell_collection[0], spell_collection[1], spell_collection[2])

    def validate_hit(self, signal):
        wand_id = int(signal)
        wiz = db_manager.fetch_wiz(wand_id)
        self.logger.log.info("Hit Detected with wand ID %d WIZ %s", wand_id, wiz)
        self.fetch_effect(wand_id)

    #maintenance_db class!!
