
class Expirence:
    def __init__(self, base_expirence, date):
        self.comishoning_date = date
        self.base_expirence = base_expirence
        self.battle_expirence = 0
    def calc(self, date):
        return self.base_expirence + self.comishoning_date - date + self.battle_expirence
