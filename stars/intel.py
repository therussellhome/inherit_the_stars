from . import game_engine
from . import reference

""" Base class for the players view of the galaxy """
class Intel(game_engine.BaseClass):
    def __init__(self, reference, **kwargs):
        self.__dict__.update(kwargs)
        if 'date' not in kwargs:
            self.date = game_engine.get('Game/')[0].date
        self.reference = Reference(reference)
