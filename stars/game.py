import sys
from . import game_engine
from .defaults import Defaults
from .fleet import Fleet


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'hundreth': [0, 0, sys.maxsize],
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
                p.ready_to_generate = False
                game_engine.save('games', self.name + ' - ' + p.name, p)

    """ Load updates from player files """
    def update_players(self):
        for p in self.players:
            if not p.computer_player:
                p.update_from_file()

    """ Generate hundreth """
    def generate_hundreth(self):
        # players in lowest to highest score
        players = list(self.players)
        players.sort(key=lambda x: x.score.rank, reverse=False)
        # planets in lowest to highest population
        # planets call actions on their starbase
        planets = []
        for system in self.systems:
            for planet in system.planets:
                if planet.on_surface.people > 0:
                    planets.append(planet)
        planets.sort(key=lambda x: x.on_planet.people, reverse=False)
        # fleets in lowest to highest initiative
        fleets = []
        for player in players:
            for fleet in player.fleets:
                fleets.append(fleet)
        fleets.sort(key=lambda x: x.initiative, reverse=False)
        #
        # actions only done at the beginning of a year
        if self.hundreth % 100 == 0:
            self._call(players, 'treaty_negotiations')
            self._call(players, 'treaty_finalization')
        self.hundreth += 1
        #
        # actions in order
        self._call(players, 'next_hundreth')
        self._call(planets, 'have_babies')
        self._call(planets, 'generate_energy')
        self._call(planets, 'mine_minerals')
        self._call(planets, 'operate_factories')
        self._call(players, 'allocate_budget')
        self._call(players, 'build_from_queue')
        self._call(planets, 'build_planetary')
        self._call(planets, 'baryogenesis', reverse=True)
        self._call(self.wormholes, 'move')
        self._call(self.asteroids, 'move')
        self._call(self.mystery_traders, 'move')
        self._call(fleets, 'move')
        self._call(planets, 'scan')
        self._call(self.asteroids, 'scan')
        self._call(fleets, 'scan')
        self._combat()
        self._call(fleets, 'move_in_system')
        self._call(planets, 'generate_fuel')
        self._call(fleets, 'merge')
        self._call(fleets, 'self_repair')
        self._call(fleets, 'repair')
        self._call(fleets, 'orbital_mining')
        self._call(fleets, 'lay_mines')
        self._call(fleets, 'bomb')
        self._call(fleets, 'colonize')
        self._call(fleets, 'piracy')
        self._call(fleets, 'sell')
        self._call(fleets, 'unload')
        self._call(fleets, 'scrap')
        self._call(fleets, 'buy')
        self._call(fleets, 'load')
        self._call(fleets, 'transfer')
        self._call(fleets, 'patrol')
        self._call(planets, 'mattrans', reverse=True)
        self._call(players, 'research')
        #
        # actions only done at the end of a year
        if self.hundreth % 100 == 0:
            self._call(planets, 'deallocate_build_queue')
            self._call(planets, 'scan')
            self._call(self.asteroids, 'scan')
            self._call(fleets, 'scan')
            self._call(players, 'calc_score')
            self._check_for_winner()

    """ Call a method on a list of classes """
    def _call(self, objs, method, reverse=False):
        if reverse:
            for obj in reversed(objs):
                eval('obj.' + method + '()')
        else:
            for obj in objs:
                eval('obj.' + method + '()')

    """ Execute combat after determining where combat will occur """
    def _combat(self):
        pass #TODO

    """ Check against the win conditions """
    def _check_for_winner(self):
        pass #TODO

Game.set_defaults(Game, __defaults)
