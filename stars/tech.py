import copy
import math
import sys
from . import game_engine
from . import stars_math
from .cloak import Cloak
from .cost import Cost
from .defaults import Defaults
from .hyperdenial import HyperDenial
from .race import Race
from .scanner import Scanner
from .tech_level import TechLevel


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
    'is_colonizer': False,
    'is_trading_post': False,
    'facility_output': (0.0, 0.0, sys.maxsize),
    'mining_rate': (0.0, 0.0, sys.maxsize),
    'mineral_depletion_factor': (0.0, 0.0, 100),
    'mat_trans_energy': (0, 0, sys.maxsize),
    'slots_general': (-1, -sys.maxsize, sys.maxsize),
    'slots_depot': (0, -sys.maxsize, sys.maxsize),
    'slots_orbital': (0, -sys.maxsize, sys.maxsize),
}


""" Grouping of tech items """
TECH_GROUPS = ['Weapons', 'Defense', 'Electronics', 'Engines', 'Hulls & Mechanicals', 'Heavy Equipment', 'Other']


""" Represent a tech component """
class Tech(Defaults):
    """ Register with game engine """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

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

    """ Get the minituarized value """
    def miniaturize(self, tech_level, field=None):
        if field == 'cost':
            return self.cost # TODO
        else:
            return self.mass # TODO

    """ Get the cost to reminituarize """
    def reminiatuarize(self, current_level, new_level):
        if new_level > current_level:
            return self.cost * 0.1 #TODO
        return Cost()

    """ Calculate the scrap value """
    def scrap_value(self, race, tech_level):
        c = self.minituarization(tech_level, 'cost')
        c.energy = 0
        return c * (race.scrap_rate() / 100)

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
        return ['<td><img style="width: 50px; height: 50px" src="tech_browser.png"/></td><td class="hfill">' \
            + '<div style="font-size: 180%; position: relative">' + self.ID \
            + '<div style="font-size: 50%; position: absolute; top: 0; right: 0">' + requirements + '</div>' \
            + '<div style="font-size: 50%; position: absolute; bottom: 0; right: 0">' + research + '</div>' \
            + '</div>' \
            + '<div style="font-size: 90%; position: relative">[' + self.category + ']' \
            + '<div style="position: absolute; top: 0; right: 0">' + self.cost.to_html() + '</div>' \
            + '</div></td>',
            '<td colspan="2">' + quick_stats + '</td>',
            '<td colspan="2" style="white-space: normal">' + self.description + '</td>' ]

    """ Build the combat chart """
    def html_combat(self, always=False):
        if self.shield > 0 or self.armor > 0 or self.ecm > 0 or len(self.weapons) > 0 or always:
            chart = {'firepower': [], 'armor': [], 'shield': [], 'ecm': []}
            for i in range(0, 100):
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                chart['armor'].append(self.armor)
                chart['shield'].append(self.shield + self.armor)
                chart['ecm'].append((self.shield + self.armor) * self.ecm * math.sqrt(range_ly))
                chart['firepower'].append(0)
                for weapon in self.weapons:
                    power = weapon.get_power(range_ly, sys.maxsize, 0)
                    chart['firepower'][i] += (power[0] + power[1]) * weapon.get_accuracy(range_ly) / 100
            return chart
        return None
    
    """ Build the sensor chart """
    def html_sensor(self, always=False):
        if self.scanner.normal > 0 or self.scanner.penetrating > 0 or self.scanner.anti_cloak > 0 or self.scanner.hyperdenial.range > 0 or always:
            return [
                self.scanner.normal,
                self.scanner.penetrating,
                self.scanner.anti_cloak,
                self.hyperdenial.range
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
                    fuel_per_ly += engine.tachometer(i + 1, mass_per_engine, 0) * mass_per_engine
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
            self._html_filter(html, bomb.percent_pop_kill + bomb.minimum_pop_kill, 'Bomb', 'Population killed', '{0} + {1}% / y'.format(bomb.minimum_pop_kill, bomb.percent_pop_kill))
            self._html_filter(html, bomb.shield_kill, 'Bomb', 'Shield generators destroyed', '{0} / y')
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
        #TODO
        # Engine group
        #TODO
        # Hulls & Mechanicals group
        self._html_filter(html, self.is_colonizer, 'Special', 'Colonizer')
        self._html_filter(html, self.is_trading_post, 'Special', 'Trading post')
        #TODO
        # Heavy Equipment group
        self._html_filter(html, self.fuel_generation, 'Heavy Equipment', 'Fuel generation', '<i class="fa-free-code-camp">{0} / y</i>')
        #TODO
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
