from serializable import Serializable

""" Represent 'cargo' that can be held """
""" A cargo_max of -1 is used to indicate no maximum """
class Cargo(Serializable):
    def __init__(self, people=0, titanium=0, lithium=0, silicon=0, cargo_max=-1):
        self.people = people
        self.titanium = titanium
        self.lithium = lithium
        self.silicon = silicon
        self.cargo_max = cargo_max
