import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'game_key': [''], # used to validate the player file
    'autogen_turn': [True],
    'date': [0.0, 0.0, sys.maxsize],
    'players': [[]], # all players for the game, these are updated/overwritten when the players are loaded from file
    'systems': [[]], # all systems - suns and planets are part of systems
    'wormholes': [[]], # all wormholes
    'asteroids': [[]], # all comets/mineral packets/salvage
    'myster_traders': [[]], # myster trader ships
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults and register self """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'game_key' not in kwargs:
            self.game_key = str(id(self))
        game_engine.register(self)


    """ Generate a turn """
    def generate_turn(self):
        # All actions are in hundredths of a turn
        for time_in in range(100):
            # fleets in lowest to highest initiative
            fleets = game_engine.get('Fleet')
            fleets.sort(key=lambda x: x.initiative, reverse=False)
            # players in lowest to highest score
            players = game_engine.get('Players')
            players.sort(key=lambda x: x.score.rank, reverse=False)
            # fleet actions
            for action in Fleet.actions:
                for fleet in fleets:
                    fleet.execute(action)
            # generate new anomolies
            #TODO
            # anomolies
            for wormhole in self.wormholes:
                wormhole.move()
            # asteroid movement
            for asteroid in self.asteroids:
                asteroid.move()
            # mystery trader
            for trader in mystery_trader:
                trader.move()
            # fleet move
            for fleet in fleets:
                fleet.move()
            # scanning
            self._scanning()
            # combat
            #TODO calculate where combat will occur and execute combat
            # in-system move
            for fleet in fleets:
                fleet.move_in_system()
            # player actions: reseach, score calc, pop growth
            for fleet in fleets:
                fleet.execute(preaction)
            # update scanning
            self._scanning()

    """ Update all scanning """
    def _scanning(self):
        for ship in game_engine.get('Ship'):
            ship.scan()
        for starbase in game_engine.get('Starbase'):
            starbase.scan()
        for planet in game_engine.get('Planet'):
            planet.scan()
        for asteroid in self.asteroids
            asteroid.scan()

Game.set_defaults(Game, __defaults)
