import sys
from random import randint
from . import game_engine
from . import hyperdenial
from . import multi_fleet
from . import scan
from . import stars_math
from .defaults import Defaults
from .fleet import Fleet
from .location import Location
from .player import Player
from .star_system import StarSystem
from .reference import Reference
from .intel import TRACK_ACCUMULATING

SCORE_FIELDS = TRACK_ACCUMULATING['Player']


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID', # ID defaulted to a UUID if not provided from the new game screen
    'hundreth': (0, 0, sys.maxsize),
    'players': [], # all players for the game, these are updated/overwritten when the players are loaded from file
    'systems': [], # all systems - suns and planets are part of systems
    'wormholes': [], # all wormholes
    'blackholes': [], # all blackholes
    'nebulae': [], # all nebulae
    'asteroids': [], # all comets/mineral packets/salvage
    'mystery_traders': [], # mystery trader ships
    'public_player_scores': (30, 0, 200), # years till public player scores
    'victory_after': (50, 10, 200), # minimum years till game can be won
    'victory_conditions': (1, 1, 10), # minimum number of conditions to win
    'victory_enemies': True,
    'victory_enemies_left': (0, -1, 15), 
    'victory_score': True,
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
    'x': (50, 0, sys.maxsize),
    'y': (50, 0, sys.maxsize),
    'z': (50, 0, sys.maxsize),
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults and register self """
    def __init__(self, x=50, y=50, z=50, num_systems=10, system_names=None, races=[], tech_file='Inherit the Stars!', **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
        if 'systems' not in kwargs:
            tech_tree = game_engine.load('Tech', tech_file)
            num_systems = max(len(races), num_systems)
            if not system_names:
                system_names = []
                for i in range(0, num_systems):
                    system_names.append('System ' + str(i))
            num_systems = min(num_systems, len(system_names))
            # create systems
            min_distance = 3 * stars_math.TERAMETER_2_LIGHTYEAR
            self.x = max(x, 2)
            self.y = max(y, 2)
            self.z = max(z, 2)
            while len(self.systems) < num_systems:
                l = Location(new_random=(self.x / 2, self.y / 2, self.z / 2), is_system=True)
                for s in self.systems:
                    if s.location - l < min_distance:
                        break
                else:
                    system_name = system_names.pop(randint(0, len(system_names) - 1))
                    self.systems.append(StarSystem(ID=system_name, location=l))
            # pick home systems
            min_distance = max(self.x, self.y, self.z) * 0.8
            homes = []
            while len(homes) < min(len(races), len(self.systems)):
                for s in self.systems:
                    for h in homes:
                        if s.location - h.location < min_distance:
                            break
                    else:
                        homeworld = s.create_system(races[len(homes)])
                        player = Player(race=races[len(homes)], tech=tech_tree, game_ID=self.ID, game=Reference(self), planets=[homeworld])
                        self.players.append(player)
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
                    p.add_intel(s, {'location': s.location})
                    p.add_intel(s.sun(), {'location': s.sun().location, 'color': s.sun().get_color(), 'size': s.sun().gravity})
            for b in self.blackholes:
                for p in self.players:
                    p.add_intel(b, {'location': b.location, 'size': b.radius})
            self._scan([])
            if self.hundreth == 0:
                self.calculate_score()
            else:
                self._call(self.players, 'update_stats')
                
    """ Save host and players to file """
    def save(self):
        game_engine.save('Game', self.ID, self)
        for p in self.players:
            if not p.computer_player:
                p.ready_to_generate = False
                p.save()
    
    """ Load updates from player files """
    def update_players(self):
        for p in self.players:
            if not p.computer_player:
                p.update_from_file()

    """ Handle public player scores """
    def calculate_score(self):
        score_balance = {
            'energy': 0.001,
            'minerals': 0.001,
            'tech_levels': 1.0,
            'planets': 1.0,
            'ships_unarmed': 0.1,
            'ships_escort': 0.2,
            'ships_of_the_wall': 0.5,
            'facilities': 0.001,
            'starbases': 1.0,
            'best': 10
        }
        best_by_field = {
            'energy': [0],
            'minerals': [0],
            'tech_levels': [0],
            'planets': [0],
            'ships_unarmed': [0],
            'ships_escort': [0],
            'ships_of_the_wall': [0],
            'facilities': [0],
            'starbases': [0]
        }
        data = []
        scores = {}
        placing = {}
        rank = {}
        self._call(self.players, 'update_stats')
        for player in self.players:
            data.append(player.get_intel(reference=player))
            print(game_engine.to_json(data))
        """ Get best in the field """
        for field in SCORE_FIELDS:
            value = 0
            if 'score' not in field:
                for i in range(len(self.players)):
                    scores[i] = 0
                    if data[i][field]['{:.2f}'.format(self.hundreth/100 + 3000)] > value:
                        value = data[i][field]['{:.2f}'.format(self.hundreth/100 + 3000)]
                        best_by_field[field] = [i]
                    elif data[i][field]['{:.2f}'.format(self.hundreth/100 + 3000)] == value:
                        best_by_field[field].append(i)
        for i in range(len(self.players)):
            for field in SCORE_FIELDS:
                if 'score' not in field:
                    scores[i] += data[i][field]['{:.2f}'.format(self.hundreth/100 + 3000)] * score_balance[field]
                    if i in best_by_field[field]:
                        scores[i] += score_balance['best']
            scores[i] = int(round(scores[i]))
            if scores[i] not in placing:
                placing[scores[i]] = []
            placing[scores[i]].append(i)
        place = 1
        for k in sorted(placing.keys(), reverse=True):
            place = 1 + len(rank.keys())
            for v in placing[k]:
                rank[v] = place
        for i in range(len(self.players)):
            self.players[i].add_intel(self.players[i], {'score': scores[i], 'score_rank': rank[i]})
        if self.hundreth / 100 >= self.public_player_scores:
            for p1 in self.players:
                for i in range(len(self.players)):
                    if p1.ID != self.players[i].ID:
                        report = self.players[i].update_stats(True)
                        report['score'] = scores[i]
                        report['score_rank'] = rank[i]
                        p1.add_intel(self.players[i], report)

    """ Check if all players are ready """
    def is_ready_to_generate(self):
        for p in self.players:
            if not p.computer_player and not p.ready_to_generate:
                return False
        return True

    """ Generate and save """
    def new_turn(self):
        self.update_players()
        print('Turn={:.0f}'.format(self.hundreth / 100), end='')
        for i in range(0, 100):
            self.generate_hundreth()
            print('.', end='', flush=True)
        print('{:.0f}'.format(self.hundreth / 100))
        self.save()

    """ Get all populated planets """
    def populated_planets(self):
        planets = []
        for system in self.systems:
            for planet in system.planets:
                if planet.on_surface.people > 0:
                    planets.append(planet)
        return planets

    """ Haddle player to player messages """
    def mail_carrier(self):
        for player in self.players:
            for msg in player.outbox:
                msg.sender = Reference(player)
                msg.receiver.add_message(msg)
            player.outbox = []

    """ Generate hundreth """
    def generate_hundreth(self):
        # players in lowest to highest score
        players = list(self.players)
        # player actions only done at the beginning of a year
        if self.hundreth % 100 == 0:
            self._call(players, 'reconcile_fleets')
            self._call(players, 'reconcile_buships')
            self._call(players, 'treaty_negotiations')
            self._call(players, 'treaty_finalization')
            self._call(players, 'cleanup_messages')
            self.mail_carrier()
        self._call(players, 'next_hundreth')
        players.sort(key=lambda x: x.get_intel(reference=x).get('score_rank'), reverse=False)
        # planets in lowest to highest population
        planets = self.populated_planets()
        self._call(planets, 'orbit')
        planets.sort(key=lambda x: x.on_surface.people, reverse=False)
        # fleets in lowest to highest initiative
        fleets = []
        for player in players:
            for fleet in player.fleets:
                fleets.append(fleet)
        multi_fleet.reset()
        # fleet actions only done at the beginning of a year
        if self.hundreth % 100 == 0:
            self._scan(fleets) # scanning is needed to support fleet patroling
        self._call(fleets, 'next_hundreth')
        fleets.sort(key=lambda x: x.stats.initiative, reverse=False)
        #
        # actions in order
        self._call(planets, 'have_babies')
        self._call(planets, 'generate_energy')
        self._call(planets, 'extract_minerals')
        self._call(planets, 'operate_factories')
        self._call(players, 'allocate_budget')
        self._call(players, 'build_from_queue')
        self._call(planets, 'build_planetary')
        self._call(planets, 'baryogenesis', reverse=True)
        self._call(fleets, 'read_orders')
        self._call(fleets, 'colonize') # occurs before move because the fleet does not need to wait around for the colonizer but does not occur in the same hundreth as the colonizer moved
        hyperdenial.reset()
        self._call(self.blackholes, 'activate')
        self._call(fleets, 'activate_hyperdenial')
        hyperdenial.calc(fleets)
        self._call(self.wormholes, 'move')
        self._call(self.asteroids, 'move')
        self._call(self.mystery_traders, 'move')
        self._call(fleets, 'move')
        self._scan(fleets)
        self._call(multi_fleet.get(), 'round1_fight')
        self._call(fleets, 'move_in_system')
        self._call(multi_fleet.get(), 'share_repair')
        self._call(fleets, 'orbital_extraction')
        self._call(fleets, 'lay_mines')
        self._call(planets, 'raise_shields')
        self._call(fleets, 'bomb')
        self._call(planets, 'bomb_impact')
        self._call(fleets, 'piracy')
        self._call(fleets, 'scrap')
        self._call(fleets, 'load_unload')
        self._call(fleets, 'buy')
        self._call(multi_fleet.get(), 'share_fuel')
        # redistribute cached values then process fleet changes
        self._call(fleets, 'fuel_distribution')
        self._call(fleets, 'cargo_distribution')
        self._call(fleets, 'transfer')
        self._call(fleets, 'merge')
        self._call(planets, 'mattrans', reverse=True)
        self._call(players, 'research')
        self._call(players, 'design_miniaturization')
        #
        # actions only done at the end of a year
        self.hundreth += 1
        if self.hundreth % 100 == 0:
            self._scan(fleets)
            self.calculate_score()
            #self._call(self.players, 'update_stats')
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
                    print('    ', obj.ID, method, t)
        else:
            for obj in objs:
                s = time.time()
                eval('obj.' + method + '()')
                t = (time.time() - s)
                if t > 0.1:
                    print('    ', obj.ID, method, t)

    """ Update binning then call scanning """
    def _scan(self, fleets):
        all_planets = []
        for system in self.systems:
            all_planets.extend(system.planets)
        scan.reset(self.players, fleets, all_planets, self.asteroids, self.wormholes, self.nebulae, self.mystery_traders)
        planets = self.populated_planets()
        self._call(fleets, 'scan_anticloak')
        self._call(planets, 'scan_penetrating')
        self._call(self.asteroids, 'scan_penetrating')
        self._call(fleets, 'scan_penetrating')
        self._call(planets, 'scan_normal')
        self._call(fleets, 'scan_normal')
        self._call(planets, 'scan_self')
        self._call(fleets, 'scan_self')

    """ Execute combat after determining where combat will occur """
    def _combat(self):
        pass #TODO

    """ Check against the win conditions """
    def _check_for_winner(self):
        # TODO store score ranking into players
        if self.hundreth >= self.victory_after * 100:
            pass #TODO


Game.set_defaults(Game, __defaults)
