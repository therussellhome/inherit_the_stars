import sys
from random import randint
from . import game_engine
from .defaults import Defaults
from .fleet import Fleet
from .location import Location
from .star_system import StarSystem
from .reference import Reference
from . import stars_math


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID', # ID defaulted to a UUID if not provided from the new game screen
    'hundreth': (0, 0, sys.maxsize),
    'players': [], # all players for the game, these are updated/overwritten when the players are loaded from file
    'systems': [], # all systems - suns and planets are part of systems
    'wormholes': [], # all wormholes
    'asteroids': [], # all comets/mineral packets/salvage
    'mystery_traders': [], # myster trader ships
    'public_player_scores': (30, 0, 200), # years till public player scores
    'victory_after': (50, 10, 200), # minimum years till game can be won
    'victory_conditions': (1, 1, 10), # minimum number of conditions to win
    'victory_enemies_left': (0, -1, 15), 
    'victory_score_number': (1000, -1, 10000), 
    'victory_tech': True,
    'victory_tech_levels': (100, 10, 300), 
    'victory_planets': True,
    'victory_planets_number': (200, 50, 1000), 
    'victory_energy': True,
    'victory_energy_number': (10000, 1000, 100000), 
    'victory_minerals': True,
    'victory_minerals_number': (10000, 1000, 100000), 
    'victory_production': True,
    'victory_production_number': (10000, 1000, 100000), 
    'victory_ships': True,
    'victory_ships_number': (1000, 100, 10000), 
    'victory_shipsofthewall': True,
    'victory_shipsofthewall_number': (150, 50, 1000), 
    'victory_starbases': True,
    'victory_starbases_number': (25, 10, 100), 
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults and register self """
    def __init__(self, x=500, y=500, z=500, num_systems=1000, system_names=None, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
        if 'systems' not in kwargs:
            num_systems = max(len(self.players), num_systems)
            if not system_names:
                system_names = []
                for i in range(0, num_systems):
                    system_names.append('System ' + str(i))
            num_systems = min(num_systems, len(system_names))
            # create systems
            min_distance = 3 * stars_math.TERAMETER_2_LIGHTYEAR
            x = max(x, 2)
            y = max(y, 2)
            z = max(z, 2)
            while len(self.systems) < num_systems:
                l = Location(random=True, scale_x=x / 2, scale_y=y / 2, scale_z=z / 2)
                for s in self.systems:
                    if s.location - l < min_distance:
                        break
                else:
                    system_name = system_names.pop(randint(0, len(system_names) - 1))
                    self.systems.append(StarSystem(ID=system_name, location=l))
            # pick home systems
            min_distance = max(x, y, z) * 0.8
            homes = []
            while len(homes) < min(len(self.players), len(self.systems)):
                for s in self.systems:
                    for h in homes:
                        if s.location - h.location < min_distance:
                            break
                    else:
                        s.create_system(Reference(self.players[len(homes)]))
                        homes.append(s)
                        if len(homes) == len(self.players):
                            break
                else:
                    min_distance *= 0.8
            # create planets
            for s in self.systems:
                if len(s.planets) == 0:
                    s.create_system()
            # initial intel
            for s in self.systems:
                for p in self.players:
                    p.add_intel(s, location=s.location, color=s.sun().get_color(), size=s.sun().gravity)
            self._call(self.get_planets(), 'scan')
            self._call(self.asteroids, 'scan')
            self._call(self.players, 'calc_score')
                
    """ Save host and players to file """
    def save(self):
        for p in self.players:
            if not p.computer_player:
                p.ready_to_generate = False
                p.save()
        game_engine.save('Game', self.ID, self)

    """ Load updates from player files """
    def update_players(self):
        for p in self.players:
            if not p.computer_player:
                p.update_from_file()

    """ Check if all players are ready """
    def is_ready_to_generate(self):
        for p in self.players:
            if not p.computer_player and not p.ready_to_generate:
                return False
        return True

    """ Generate and save """
    def new_turn(self):
        self.update_players()
        for i in range(0, 100):
            self.generate_hundreth()
        self.save()

    """ Get all populated planets """
    def get_planets(self):
        planets = []
        for system in self.systems:
            for planet in system.planets:
                if planet.on_surface.people > 0:
                    planets.append(planet)
        return planets

    """ Generate hundreth """
    def generate_hundreth(self):
        # players in lowest to highest score
        players = list(self.players)
        players.sort(key=lambda x: x.score.rank, reverse=False)
        # planets in lowest to highest population
        # planets call actions on their starbase
        planets = self.get_planets()
        planets.sort(key=lambda x: x.on_surface.people, reverse=False)
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
            self._call(planets, 'scan')
            self._call(self.asteroids, 'scan')
            self._call(fleets, 'scan')
            self._call(players, 'calc_score')
            self._check_for_winner()

    """ Call a method on a list of classes """
    def _call(self, objs, method, reverse=False):
        import time
        if reverse:
            for obj in reversed(objs):
                s = time.time()
                eval('obj.' + method + '()')
                t = (time.time() - s)
                if t > 0.1:
                    print(obj.__uuid__, method, t)
        else:
            for obj in objs:
                s = time.time()
                eval('obj.' + method + '()')
                t = (time.time() - s)
                if t > 0.1:
                    print(obj.__uuid__, method, t)

    """ Execute combat after determining where combat will occur """
    def _combat(self):
        pass #TODO

    """ Check against the win conditions """
    def _check_for_winner(self):
        if self.hundreth >= self.victory_after * 100:
            pass #TODO


Game.set_defaults(Game, __defaults)
