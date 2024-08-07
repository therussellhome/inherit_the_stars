import copy
import math
import sys
from . import game_engine
from . import stars_math
from .cloak import Cloak
from .cost import Cost
from .defaults import Defaults, get_default
from .hyperdenial import HyperDenial
from .stargate import Stargate
from .minerals import Minerals
from .race import Race
from .scanner import Scanner
from .tech_level import TechLevel, TECH_FIELDS


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'category': '',
    'description': 'I\'m a horrible scanner, a zero range weapon, and an engine that only works on Saturday',
    'cost': Cost(),
    'race_requirements': '',
    'level': TechLevel(),
    'mass': (0, 0, sys.maxsize),
    'cargo_max': (0, 0, sys.maxsize),
    'fuel_max': (0, 0, sys.maxsize),
    'shield': (0, 0, sys.maxsize),
    'armor': (0, 0, sys.maxsize),
    'ecm': (0, 0, 100),
    'weapons': [], # weapon.Weapon()
    'bombs': [], # bomb.Bomb()
    'scanner': Scanner(),
    'cloak': Cloak(),
    'engines': [], # engine.Engine()
    'shipyard': (0, 0, sys.maxsize),
    'repair': (0, 0, sys.maxsize),
    'mines_laid': (0, 0, sys.maxsize),
    'fuel_generation': (0, 0, sys.maxsize),
    'hyperdenial': HyperDenial(),
    'stargate': Stargate(),
    'is_colonizer': False,
    'is_trading_post': False,
    'is_piracy_cargo': False,
    'is_piracy_fuel': False,
    'facility_output': (0.0, 0.0, sys.maxsize),
    'extraction_rate': (0.0, 0.0, sys.maxsize),
    'mineral_depletion_factor': (0.0, 0.0, 100),
    'mat_trans_energy': (0, 0, sys.maxsize),
    'slots_general': (-1, -sys.maxsize, sys.maxsize),
    'slots_depot': (0, -sys.maxsize, sys.maxsize),
    'slots_orbital': (0, -sys.maxsize, sys.maxsize),
    'image': '',
}


""" Grouping of tech items """
TECH_GROUPS = ['Weapons', 'Defense', 'Electronics', 'Engines', 'Hulls & Mechanicals', 'Heavy Equipment', 'Other']


""" Represent a tech component """
class Tech(Defaults):
    """ Register with game engine """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game_engine.register(self)

    """ Add a tech to self using the current miniaturization_level """
    def merge(self, other, max_not_merge=False):
        for key in Tech.defaults:
            # Skip strings
            if isinstance(self[key], str):
                pass
            elif isinstance(self[key], list):
                self[key].extend(other[key])
            elif max_not_merge and key == 'scanner':
                self[key].anti_cloak = max(self[key].anti_cloak, other[key].anti_cloak)
                self[key].penetrating = max(self[key].penetrating, other[key].penetrating)
                self[key].normal = max(self[key].normal, other[key].normal)
            elif max_not_merge and key == 'hyperdenial':
                self[key].radius = max(self[key].radius, other[key].radius)
            elif key == 'mineral_depletion_factor':
                self[key] = max(self[key], other[key])
            else:
                self[key] += other[key]

    """ Get tech group """
    def tech_group(self):
        if self.category.endswith('Hull') or self.category in ['Mechanical']:
            return 'Hulls & Mechanicals'
        elif self.category in ['Beam Weapon', 'Bomb', 'Missile']:
            return 'Weapons'
        elif self.category in ['Shield', 'Armor']:
            return 'Defense'
        elif self.category in ['Cloak', 'ECM', 'Scanner']:
            return 'Electronics'
        elif self.category in ['Engine']:
            return 'Engines'
        elif self.category in ['Depot', 'Orbital']:
            return 'Heavy Equipment'
        else:
            return 'Other'
        
    """ Determine if the item is available for a given tech level and race """
    def is_available(self, level=None, race=None):
        if level and not self.level.is_available(level):
            return False
        if race and len(self.race_requirements) > 0:
            traits = race.list_traits()
            for requirement in self.race_requirements.split(' '):
                if requirement[0] == '-':
                    if requirement[1:] in traits:
                        return False
                elif requirement not in traits:
                    return False
        return True

    """ Is this a hull tech item """
    def is_hull(self):
        if self.slots_general > 0 or self.slots_depot > 0 or self.slots_orbital > 0:
            return True
        return False

    """ Calculate the scrap value """
    def scrap_value(self, race, miniaturization_level=None):
        # Force scrap to be just minerals
        m = Minerals(self.cost * self.miniaturization(miniaturization_level))
        return m * (race.scrap_rate / 100)

    """ How much past the base is the miniaturization """
    def miniaturization(self, miniaturization_level=None):
        if not miniaturization_level:
            return 1
        base = self.level.total_levels()
        levels_over = 0
        if base == 0:
            levels_over = miniaturization_level.total_levels()
        else:
            for f in TECH_FIELDS:
                if miniaturization_level[f] < self.level[f]:
                    return 1
                levels_over += (miniaturization_level[f] - self.level[f]) * self.level[f] / base
        return 1 / (0.1 * levels_over ** 0.5 + 1)

    """ Compute the miniaturization cost """
    def build_cost(self, miniaturization_level=None):
        return self.cost * self.miniaturization(miniaturization_level)

    """ Compute the cost to overhaul this component to a new miniaturization level """
    def overhaul_cost(self, current_level, overhaul_level, race):
        current_miniaturization = self.miniaturization(current_level)
        overhaul_miniaturization = self.miniaturization(overhaul_level)
        # overhaul efficency is affected by scrap efficency
        return self.cost * (current_miniaturization - overhaul_miniaturization) * (200 - race.scrap_rate) / 100

    """ Build the overview table """
    def html_overview(self, player_race=Race(), player_level=TechLevel(), player_partial=TechLevel()):
        # overview
        research = self.level.calc_cost(player_race, player_level, player_partial)
        if research > 0:
            research = 'Research: <i class="fa-bolt" title="Energy">' + str(research) + '</i>'
        else:
            research = ''
        requirements = ''
        if type(self) == Tech:
            requirements = self.race_requirements + ' ' + self.level.to_html()
        quick_stats = ''
        if self.mass > 0:
            quick_stats += '<i class="fa-weight-hanging"> ' + str(self.mass) + '</i>'
        if self.cargo_max > 0:
            quick_stats += '<i class="fa-luggage-cart"> ' + str(self.cargo_max) + '</i>'
        if self.fuel_max > 0:
            quick_stats += '<i class="fa-free-code-camp"> ' + str(self.fuel_max) + '</i>'
        # Don't show images if we don't have one
        image = self.image
        if self.image == '':
            image = self.ID + '.png'
        if (game_engine.user_file('img/' + image, is_www=True) / 'img' / image).exists():
            image = '<img class="hfill" src="/img/' + image + '"/>'
        else:
            image = ''
        return ['<td class="hfill">' \
            + '<div style="font-size: 180%; position: relative">' + self.ID \
            + '<div style="font-size: 50%; position: absolute; top: 0; right: 0">' + requirements + '</div>' \
            + '<div style="font-size: 50%; position: absolute; bottom: 0; right: 0">' + research + '</div>' \
            + '</div>' \
            + '<div style="font-size: 90%; position: relative">[' + self.category + ']' \
            + '<div style="position: absolute; top: 0; right: 0">' + self.cost.to_html() + '</div>' \
            + '</div></td>',
            '<td>' + image + '</td>',
            '<td>' + quick_stats + '</td>',
            '<td style="white-space: normal">' + self.description + '</td>' ]

    """ Build the combat chart """
    def html_combat(self, always=False):
        if self.shield > 0 or self.armor > 0 or self.ecm > 0 or len(self.weapons) > 0 or always:
            chart = {'firepower': [], 'armor': [], 'shield': [], 'ecm': []}
            for i in range(0, 100):
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                chart['armor'].append(self.armor)
                chart['shield'].append(self.shield + self.armor)
                chart['ecm'].append(max(1.0, self.shield + self.armor) * self.ecm * math.sqrt(range_ly))
                chart['firepower'].append(0)
                for weapon in self.weapons:
                    power = weapon.get_power(range_ly, sys.maxsize, 0)
                    chart['firepower'][i] += (power[0] + power[1]) * weapon.get_accuracy(range_ly) / 100
            return chart
        return None
    
    """ Build the sensor chart """
    def html_sensor(self, always=False):
        if self.scanner.normal > 0 or self.scanner.penetrating > 0 or self.scanner.anti_cloak > 0 or self.hyperdenial.radius > 0 or always:
            return [
                self.scanner.normal,
                self.scanner.penetrating,
                self.scanner.anti_cloak,
                self.hyperdenial.radius
            ]
        return None

    """ Build the engine chart """
    def html_engine(self, always=False):
        if len(self.engines) > 0 or always:
            chart = {'tachometer': [], 'siphon': []}
            mass_per_engine = 100
            if self.category != 'Engine' and len(self.engines) > 0:
                mass_per_engine = (self.mass + self.cargo_max) / len(self.engines)
            for i in range(0, 10):
                fuel_per_ly = 0
                siphon = 0
                for engine in self.engines:
                    fuel_per_ly += engine.tachometer(i + 1, mass_per_engine) * mass_per_engine
                    siphon += engine.antimatter_siphon
                chart['tachometer'].append(fuel_per_ly / mass_per_engine)
                if siphon == 0:
                    chart['siphon'].append(0)
                elif fuel_per_ly == 0:
                    chart['siphon'].append(100)
                else:
                    chart['siphon'].append(round(min(100, siphon / fuel_per_ly * 100), 0))
            return chart
        return None

    """ Build guts table """
    def html_guts(self):
        html = []
        # Weapon group
        for bomb in self.bombs:
            self._html_filter(html, bomb.percent_pop_kill + bomb.minimum_pop_kill, 'Bomb', 'Population killed', '{0} + {1}%/y'.format(bomb.minimum_pop_kill, bomb.percent_pop_kill))
            self._html_filter(html, bomb.shield_kill, 'Bomb', 'Shield generators destroyed', '{0}/y')
            self._html_filter(html, True, 'Bomb', 'Minimum shield penetration', '{0}%'.format(max(0, 100 - bomb.max_defense)))
        for weapon in self.weapons:
            category = 'Missile'
            if weapon.is_beam:
                category = 'Beam'
            self._html_filter(html, weapon.power, category, 'Power', '{0}GJ/m<sup>2</sup>')
            self._html_filter(html, weapon.range_tm, category, 'Range', '{0}Tm')
            self._html_filter(html, weapon.accuracy, category, 'Accuracy', '{0}%')
            self._html_filter(html, weapon.armor_multiplier - 1, category, 'Armor multiplier', '{0}%'.format(weapon.armor_multiplier))
            self._html_filter(html, weapon.is_multishot, category, 'Multishot')
        # Shields & Armor group
        self._html_filter(html, self.shield, 'Shield', 'Strength', '{0}GJ/m<sup>2</sup>')
        self._html_filter(html, self.armor, 'Armor', 'Strength', '{0}GJ/m<sup>2</sup>')
        # Electronics group
        self._html_filter(html, self.ecm, 'ECM', 'Effectiveness', '{0}%')
        self._html_filter(html, self.cloak.percent, 'Cloak', 'Percent of KE', '{0}%')
        #Does built-in Kender cloaking or another cloaking category need to be included here?
        self._html_filter(html, self.scanner.normal, 'Scanner', 'Normal', '{0} KE/100ly')
        self._html_filter(html, self.scanner.penetrating, 'Scanner', 'Penetrating Range', '{0}ly')
        self._html_filter(html, self.scanner.anti_cloak, 'Scanner', 'Anti-cloak', '{0}ly')
        # Engine group
        for engine in self.engines:
            self._html_filter(html, engine.kt_exponent, 'Engine', 'kT exponent', '{0}')
            self._html_filter(html, engine.speed_divisor, 'Engine', 'Speed divisor', '{0}')
            self._html_filter(html, engine.speed_exponent, 'Engine', 'Speed exponent', '{0}')
            self._html_filter(html, engine.antimatter_siphon, 'Engine', 'Forages', '<i class="fa-free-code-camp">{0}/ly</i>')
        # Hulls & Mechanicals group
        self._html_filter(html, self.repair, 'Repair', 'Damage points', '{0}/y')
        self._html_filter(html, self.is_colonizer, 'Special', 'Colonizer')
        self._html_filter(html, self.is_trading_post, 'Special', 'Trading post')
        # Heavy Equipment group
        self._html_filter(html, self.fuel_generation, 'Heavy Equipment', 'Fuel generation', '<i class="fa-free-code-camp">{0}/y</i>')
        self._html_filter(html, self.shipyard, 'Heavy Equipment', 'Shipyard capacity', '{0} kT/y')
        self._html_filter(html, self.mines_laid, 'Heavy Equipment', 'Mines laid', '{0}/y')
        self._html_filter(html, self.hyperdenial.radius, 'Heavy Equipment', 'Hyper denial', '{0}ly')
        self._html_filter(html, self.extraction_rate, 'Heavy Equipment', 'Mineral extraction rate', '{0}/y')
        self._html_filter(html, self.mineral_depletion_factor, 'Heavy Equipment', 'Mineral depletion', '{0}/kT mined')
        self._html_filter(html, self.mat_trans_energy, 'Heavy Equipment', 'Mat-trans energy', '{0}/kT')
        # Slots
        if type(self) == Tech:
            self._html_filter(html, self.slots_general, 'Slots', 'General')
            self._html_filter(html, self.slots_depot, 'Slots', 'Depot')
            self._html_filter(html, self.slots_orbital, 'Slots', 'Orbital')
        return html

    """ Filter for appending to guts table """
    def _html_filter(self, html, value, category, name, formatter=None):
        # Use early exit paradigm
        if type(value) == int or type(value) == float:
            if value == 0:
                return
            if not formatter:
                formatter = '{0}'
        if type(value) == bool:
            if value == False:
                return
            if not formatter:
                formatter = '<i class="fa-check"></i>'
        html.append('<td>[' + category + ']</td><td class="hfill">' + name + '</td><td class="tech_value">' + formatter.format(value) + '</td>')


Tech.set_defaults(Tech, __defaults)
