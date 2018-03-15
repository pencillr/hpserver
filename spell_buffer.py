

class SpellBuffer:

    def __init__(self, name):
        self.name = name
        self.recent_spell = ""
        self.timestamp = 0

    def store_spell(self, spell, timestamp):
        self.recent_spell = spell
        self.timestamp = timestamp

    def get_name(self):
        return self.name

    def get_spell(self):
        s = self.recent_spell
        t = self.timestamp
        #store_spell("",0)
        return s, t
