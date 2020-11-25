import sys
import math
from .playerui import PlayerUI
from .. import game_engine
from .. import stars_math
from ..race import Race
from ..scanner import Scanner
from ..tech import Tech as StarsTech
from ..tech_level import TechLevel

__defaults = {
    'overview': [{}],
#    'repair': [0, 0, sys.maxsize],
#    'fuel_generation': [0, 0, sys.maxsize],
#    'special_type': [''],
#    'colonizer': [False],

    'combat': [{}], # power over range (computed for 0..99)
    'sensor': [{}], # visability over range (standard, penetrating, anti-cloak, self-cloak)
    'engine': [{}], # tacometer over hyper (computed for 1..10)
    'guts': [{}],
#    'engine_siphon': [0, 0, sys.maxsize],

#    'ecm': [0, 0, 100],
#    'weapon_power': [0, 0, sys.maxsize],
#    'weapon_range': [0.0, 0.0, 1.0],
#    'weapon_accuracy': [0, 0, 100],
#    'scanner_normal': [0, 0, sys.maxsize],
#    'scanner_penetrating': [0, 0, sys.maxsize],
#    'scanner_anticloak': [0, 0, sys.maxsize],
#    'cloak': [0, 0, 100],
#    'apparent_mass': [0, 0, sys.maxsize],
#    'engine_kt_exp': [0.0, 0.0, sys.maxsize],
#    'engine_speed_div': [0.0, 0.0001, sys.maxsize],
#    'engine_speed_exp': [0.0, 0.0, sys.maxsize],
}

""" Display information about a tech item or ship design """
class Tech(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        tech_tree = game_engine.get('Tech')
        if self.player:
            player_race = self.player.race
            player_level = self.player.tech_level
            player_partial = self.player.research_partial
        else:
            if len(tech_tree) < 10:
                tech_tree = game_engine.load_defaults('Tech')
            player_race = Race()
            player_level = TechLevel()
            player_partial = TechLevel()
        for tech in tech_tree:
            self._build_overview(tech, player_race, player_level, player_partial)
            self._build_combat(tech)
            self._build_sensor(tech)
            self._build_engine(tech)
            self._build_guts(tech)
    
    """ Build the overview table """
    def _build_overview(self, tech, player_race, player_level, player_partial):
        # overview
        self.overview[tech.name] = ['<td><img style="width: 50px; height: 50px" src="tech_browser.png"/></td>' \
            + '<td class="hfill"><div style="font-size: 150%">' + tech.name + '</div>' \
            + '<div style="font-size: 75%">[' + tech.category + ']</div></td>' \
            + '<td style="text-align: right"><div>Requirements: ' + tech.race_requirements + ' ' + tech.level.to_html() + '</div>' \
            + '<div>Research: <i class="fa-bolt" title="Energy">' + str(tech.level.calc_cost(player_race, player_level, player_partial)) + '</i></div></td>']
        desc = tech.description + ' '
        # Mass / Cargo
        if tech.mass > 0:
            desc += '<i class="fa-weight-hanging"> ' + str(tech.mass) + '</i>'
        if tech.cargo_max > 0:
            desc += '<i class="fa-luggage-cart"> ' + str(tech.cargo_max) + '</i>'
        if tech.fuel_max > 0:
            desc += '<i class="fa-free-code-camp"> ' + str(tech.fuel_max) + '</i>'
        desc += tech.cost.to_html()
        self.overview[tech.name].append('<td colspan="3" style="white-space: normal">' + desc + '</td>')

    """ Build the combat chart """
    def _build_combat(self, tech):
        if tech.shield > 0 or tech.armor > 0 or tech.ecm > 0 or len(tech.weapons) > 0:
            self.combat[tech.name] = {'firepower': [], 'armor': [], 'shield': [], 'ecm': []}
            for i in range(0, 100):
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                self.combat[tech.name]['armor'].append(tech.armor)
                self.combat[tech.name]['shield'].append(tech.shield + tech.armor)
                self.combat[tech.name]['ecm'].append((tech.shield + tech.armor) * tech.ecm * math.sqrt(range_ly))
                self.combat[tech.name]['firepower'].append(0)
                for weapon in tech.weapons:
                    power = weapon.get_power(range_ly, sys.maxsize, 0)
                    self.combat[tech.name]['firepower'][i] += (power[0] + power[1]) * weapon.get_accuracy(range_ly) / 100
    
    """ Build the sensor chart """
    def _build_sensor(self, tech):
        if tech.scanner.normal > 0 or tech.scanner.penetrating > 0 or tech.scanner.anti_cloak > 0 or type(tech) != StarsTech:
            detect_scanner = Scanner(normal=250.0)
            apparent_mass = (tech.mass + tech.cargo_max) * (1 - tech.cloak.percent / 100)
            self.sensor[tech.name] = [
                tech.scanner.normal,
                tech.scanner.penetrating,
                tech.scanner.anti_cloak,
                detect_scanner.range_visible(apparent_mass)
            ]

    """ Build the engine chart """
    def _build_engine(self, tech):
        if len(tech.engines) > 0:
            self.engine[tech.name] = []
            mass_per_engine = (tech.mass + tech.cargo_max) / len(tech.engines)
            for i in range(0, 10):
                self.engine[tech.name].append(0)
                for engine in tech.engines:
                    self.engine[tech.name][i] += engine.tachometer(i, mass_per_engine, 0)

    """ Build guts table """
    def _build_guts(self, tech):
        self.guts[tech.name] = []
        # Weapon group
        for bomb in tech.bombs:
            self._filter(tech, bomb.percent_pop_kill + bomb.minimum_pop_kill, 'Bomb', 'Population killed', '{0} + {1}% / y'.format(bomb.minimum_pop_kill, bomb.percent_pop_kill))
            self._filter(tech, bomb.shield_kill, 'Bomb', 'Shield generators destroyed', '{0} / y')
            self._filter(tech, True, 'Bomb', 'Minimum shield penetration', '{0}%'.format(max(0, 100 - bomb.max_defense)))
        for weapon in tech.weapons:
            category = 'Missile'
            if weapon.is_beam:
                category = 'Beam'
            self._filter(tech, weapon.power, category, 'Power', '{0}GJ/m<sup>2</sup>')
            self._filter(tech, weapon.range_tm, category, 'Range', '{0}Tm')
            self._filter(tech, weapon.accuracy, category, 'Accuracy', '{0}%')
            self._filter(tech, weapon.armor_multiplier - 1, category, 'Armor multiplier', '{0}%'.format(weapon.armor_multiplier))
            self._filter(tech, weapon.is_multishot, category, 'Multishot')
        # Shields & Armor group
        self._filter(tech, tech.shield, 'Shield', 'Strength', '{0}GJ/m<sup>2</sup>')
        self._filter(tech, tech.armor, 'Armor', 'Strength', '{0}GJ/m<sup>2</sup>')
        # Electronics group
        # Engine group
        # Hulls & Mechanicals group
        self._filter(tech, tech.slots_general, 'Component Slots', 'General')
        self._filter(tech, tech.slots_depot, 'Component Slots', 'Depot')
        self._filter(tech, tech.slots_orbital, 'Component Slots', 'Orbital')
        self._filter(tech, tech.is_colonizer, 'Special', 'Colonizer')
        self._filter(tech, tech.is_trading_post, 'Special', 'Trading post')
        # Heavy Equipment group
        self._filter(tech, tech.fuel_generation, 'Heavy Equipment', 'Fuel generation', '<i class="fa-free-code-camp">{0} / y</i>')
        # Planetary group
        #TODO - differeniate between factories and power plants
        self._filter(tech, tech.facility_output, 'Planetary', 'Energy output', '<i class="fa-bolt">{0} / y</i>')

    """ Filter for appending to guts table """
    def _filter(self, tech, value, category, name, formatter=None):
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
        self.guts[tech.name].append('<td>[' + category + ']</td><td class="hfill">' + name + '</td><td class="tech_value">' + formatter.format(value) + '</td>')

"""
    <tr><td>Shields</td><td><input id="shield" style="text-align: right; width: 5em" disabled="true"/></td><td>GJ/m<sup>3</sup></td></tr>
    <tr><td>Armor</td><td><input id="armor" style="text-align: right; width: 5em" disabled="true"/></td><td>GJ/m<sup>3</sup></td></tr>
    <tr><td>ECM</td><td><input id="ecm" style="text-align: right; width: 5em" disabled="true"/></td><td>%</td></tr>
    <tr><td>Weapon Power</td><td><input id="weapon_power" style="text-align: right; width: 5em" disabled="true"/></td><td>GJ/m<sup>3</sup></td></tr>
    <tr><td>Weapon Range</td><td><input id="weapon_range" style="text-align: right; width: 5em" disabled="true"/></td><td>Tm</td></tr>
    <tr><td>Weapon Accuracy</td><td><input id="weapon_accuracy" style="text-align: right; width: 5em" disabled="true"/></td><td>%</td></tr>
    <tr><td>Normal Scanner</td><td><input id="scanner_normal" style="text-align: right; width: 5em" disabled="true"/></td><td>ly</td></tr>
    <tr><td>Penetrating Scanner</td><td><input id="scanner_penetrating" style="text-align: right; width: 5em" disabled="true"/></td><td>ly</td></tr>
    <tr><td>Anti-Cloak Scanner</td><td><input id="scanner_anticloak" style="text-align: right; width: 5em" disabled="true"/></td><td>ly</td></tr>
    <tr><td>Cloak</td><td><input id="cloak" style="text-align: right; width: 5em" disabled="true"/></td><td>%</td></tr>
    <tr><td>Apparent Mass</td><td><input id="apparent_mass" style="text-align: right; width: 5em" disabled="true"/></td><td>kT</td></tr>
    <tr><td>Engine kT Exponent</td><td><input id="engine_kt_exp" style="text-align: right; width: 5em" disabled="true"/></td><td></td></tr>
    <tr><td>Engine Hyper Divisor</td><td><input id="engine_speed_div" style="text-align: right; width: 5em" disabled="true"/></td><td></td></tr>
    <tr><td>Engine Hyper Exponent</td><td><input id="engine_speed_exp" style="text-align: right; width: 5em" disabled="true"/></td><td></td></tr>
    <tr><td>Engine Siphon</td><td><input id="engine_siphon" style="text-align: right; width: 5em" disabled="true"/></td><td><span style="border-top: 1px solid white">₥</span>/ly</td></tr>
"""

Tech.set_defaults(Tech, __defaults)
