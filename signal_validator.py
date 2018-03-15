import db_manager
import string
import time
import datetime
from spell_buffer import SpellBuffer

class SignalValidator:

    def __init__(self, logger):
        self._signal_queue = {}
        self.logger = logger
        #create hitlogger too


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

    def get_most_recent_spell(self, wand):
        id = str(wand)
        return self._signal_queue[id].get_spell()

    def set_most_recent_spell(self, wand, spell, timeframe):
        id = str(wand)
        self._signal_queue[id].store_spell(spell, timeframe)

    def add_signal_queue(self, element, wand):
        id = str(wand)
        self._signal_queue[id] = element

    def store_cast(self, signal):
        base = signal
        wand_id, spell =  base.split('_')
        id = int(wand_id)
        if self.validate_cast(id, spell):
            ts = time.time()
            time_base = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
            timeframe =int(time_base)
            self.set_most_recent_spell(id, spell, timeframe)
            db_manager.store_cast(wand_id, spell, timeframe)
            self.logger.log.info("Spell: %s stored with ID: %d", spell, id)
            self.responder.data_to_write.insert(0, "Stored")
        else:
            self.responder.data_to_write.insert(0, "Spell not Owned")

    def validate_cast(self, wand_id, spell):
        if db_manager.auth_cast(wand_id, spell) == 0:
            return False
        else:
            return True


    def fetch_effect(self, wand_id):
        #effect = db_manager.fetch_cast(wand_id)
        time.sleep(1) # in case cast and wand happened simmultaneously
        effect, timeframe = self.get_most_recent_spell(wand_id)
        # handle if older spell - enough to handle time diffs
        if effect == "":
            self.logger.log.info("No Spell Detected from wand: %d", wand_id)
            self.responder.data_to_write.insert(0, "no_spell")
            return
        tf = str(timeframe)
        current_time = datetime.datetime.now()
        effect_time = datetime.datetime.strptime(tf, "%Y%m%d%H%M%S")
        diff = current_time - effect_time
        if diff.seconds >= 5:
            self.logger.log.info("Detected spell was out of range from wand: %d", wand_id)
            self.responder.data_to_write.insert(0, "Spell out of range")
            return
        #handle spell effect on user?
        self.logger.log.info("Spell Detected: %s", effect)
        warning = "hitby_" + effect
        self.responder.data_to_write.insert(0, warning)


    def register_user(self, reg_string):
        base = reg_string
        name, id, spells = base.split('_')
        #name = base[4:-4]
        spell_collection = []
        # Register a spellbuffer object
        spell_buffer = SpellBuffer(name)
        self.add_signal_queue(spell_buffer, id)
        #---
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
        self.responder.data_to_write.insert(0, "Registered")

    def validate_hit(self, signal):
        #whoami ID is needed too from id
        wand_id = int(signal)
        wiz = db_manager.fetch_wiz(wand_id)
        self.logger.log.info("Hit Detected with wand ID %d WIZ %s", wand_id, wiz)
        self.fetch_effect(wand_id)

    #maintenance_db class!!
