from . import game_engine

""" Base class for the players view of the galaxy """
class PlayerReport(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if 'date' not in kwargs:
            self.date = game_engine.get('Game/')[0].date
