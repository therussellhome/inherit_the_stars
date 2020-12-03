import sys
from . import game_engine
from .defaults import Defaults
from .fleet import Fleet


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'turn': [0, 0, sys.maxsize],
    'players': [[]], # all players for the game, these are updated/overwritten when the players are loaded from file
    'systems': [[]], # all systems - suns and planets are part of systems
    'wormholes': [[]], # all wormholes
    'asteroids': [[]], # all comets/mineral packets/salvage
    'mystery_traders': [[]], # myster trader ships
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults and register self """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

    """ Save host and players to file """
    def save(self):
        game_engine.save('host', self.name, self)
        for p in self.players:
            if not p.computer_player:
                game_engine.save('games', self.name + ' - ' + p.name, p)

    """ Load updates from player files """
    def update_players(self):
        for p in self.players:
            if not p.computer_player:
                p.update_from_file()

    """ Generate a turn """
    def generate_turn(self):
        self.turn += 1
        # All actions are in hundredths of a turn
        for hundreth in range(100):
            # players in lowest to highest score
            players = list(self.players)
            players.sort(key=lambda x: x.score.rank, reverse=False)
            # fleets in lowest to highest initiative
            fleets = []
            for player in players:
                for fleet in player.fleets:
                    fleets.append((fleet, player))
            fleets.sort(key=lambda x: x[0].initiative, reverse=False)
            # player turn
            for player in players:
                player.generate_turn()
            # fleet actions
            for action in Fleet.actions:
                for fleet in fleets:
                    fleet[0].execute(action, fleet[1])
            # generate new anomalies
            #TODO
            # anomalies
            for wormhole in self.wormholes:
                wormhole.move()
            # asteroid movement
            for asteroid in self.asteroids:
                asteroid.move()
            # mystery trader
            for trader in self.mystery_traders:
                trader.move()
            # fleet move
            for fleet in fleets:
                fleet[0].move(fleet[1])
            # scanning
            self._scanning()
            # combat
            #TODO calculate where combat will occur and execute combat
            # in-system move
            for fleet in fleets:
                fleet[0].move_in_system(fleet[1])
            # score
            for player in players:
                player.calc_score()
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
        for asteroid in self.asteroids:
            asteroid.scan()

Game.set_defaults(Game, __defaults)
