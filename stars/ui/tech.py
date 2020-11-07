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
    'tech_general': [[]],
    'repair': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'special_type': [''],
    'colonizer': [False],

    'weapon_chart_data': [[]], # power over range (computed for 0..99)
    'shield': [0, 0, sys.maxsize], # pre-calc if race has regenerating shields
    'armor': [0, 0, sys.maxsize], # pre-calc if race has regenerating shields
    'ecm_chart_data': [[]], # defense over range (computed for 0..99)
    'scanner_chart_data': [[]], # visability over range (standard, penetrating, anti-cloak, self-cloak)
    'engine_chart_data': [[]], # tacometer over hyper (computed for 1..10)
    'engine_siphon': [0, 0, sys.maxsize],

    'ecm': [0, 0, 100],
    'weapon_power': [0, 0, sys.maxsize],
    'weapon_range': [0.0, 0.0, 1.0],
    'weapon_accuracy': [0, 0, 100],
    'scanner_normal': [0, 0, sys.maxsize],
    'scanner_penetrating': [0, 0, sys.maxsize],
    'scanner_anticloak': [0, 0, sys.maxsize],
    'cloak': [0, 0, 100],
    'apparent_mass': [0, 0, sys.maxsize],
    'engine_kt_exp': [0.0, 0.0, sys.maxsize],
    'engine_speed_div': [0.0, 0.0001, sys.maxsize],
    'engine_speed_exp': [0.0, 0.0, sys.maxsize],
}

""" Display information about a tech item or ship design """
class Tech(PlayerUI):
    def __init__(self, action, **kwargs):
        params = (action + '&').split('&')
        super().__init__(**kwargs, player_token=params[1])
        if self.player:
            if '/' not in params[0]:
                params[0] = 'Tech/' + params[0]
            tech = game_engine.get(params[0])
            race = self.player.race
            player_level = self.player.tech_level
            player_partial = self.player.research_partial
        else:
            params[0] = 'Tech/' + ('/' + params[0]).split('/')[-1]
            tech = game_engine.get(params[0])
            if not tech:
                game_engine.load_defaults('Tech')
                tech = game_engine.get(params[0])
            race = Race()
            player_level = TechLevel()
            player_partial = TechLevel()
        if not isinstance(tech, StarsTech):
            return
        # General
        self.tech_general.append('<td><img style="width: 50px; height: 50px" src="tech_browser.png"/></td>' \
            + '<td class="hfill"><div style="font-size: 150%">' + tech.name + '</div>' \
            + '<div style="font-size: 75%">' + tech.category + '</div></td>' \
            + '<td style="text-align: right"><div>Requirements: ' + tech.race_requirements + ' ' + tech.level.to_html() + '</div>' \
            + '<div>Research: <i class="fa-bolt" title="Energy">' + str(tech.level.calc_cost(race, player_level, player_partial)) + '</i></div></td>')
        desc = tech.description + ' '
        # Mass / Cargo
        chart_mass = 100
        if type(tech) != StarsTech:
            chart_mass = tech.mass + tech.cargo_max
            self.apparent_mass = chart_mass * (1 - tech.cloak.percent / 100)
        if tech.mass > 0:
            desc += '<i class="fa-weight-hanging"> ' + str(tech.mass) + '</i>'
        if tech.cargo_max > 0:
            desc += '<i class="fa-luggage-cart"> ' + str(tech.cargo_max) + '</i>'
        if tech.fuel_max > 0:
            desc += '<i class="fa-free-code-camp"> ' + str(tech.fuel_max) + '</i>'
        desc += tech.cost.to_html()
        self.tech_general.append('<td colspan="3" style="white-space: normal">' + desc + '</td>')
        # Shield, Armor, ECM
        if tech.shield > 0 or tech.armor > 0 or tech.ecm > 0:
            self.shield = tech.shield
            self.armor = tech.armor
            self.ecm = tech.ecm
            base = tech.shield + tech.armor
            for i in range(0, 100):
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                self.ecm_chart_data.append(base * tech.ecm * math.sqrt(range_ly))
        # Weapon
        for weapon in tech.weapons:
            # Only display the last one
            self.weapon_power = weapon.power
            self.weapon_range = weapon.range_tm
            self.weapon_accuracy = weapon.accuracy
            for i in range(0, 100):
                if len(self.weapon_chart_data) < i + 1:
                    self.weapon_chart_data.append(0)
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                power = weapon.get_power(range_ly, sys.maxsize, 0)
                self.weapon_chart_data[i] += power[0] * weapon.get_accuracy(range_ly) / 100
        # Scanner
        self.scanner_normal = tech.scanner.normal
        self.scanner_penetrating = tech.scanner.penetrating
        self.scanner_anticloak = tech.scanner.anti_cloak
        self.scanner_chart_data.append(tech.scanner.normal)
        self.scanner_chart_data.append(tech.scanner.penetrating)
        self.scanner_chart_data.append(tech.scanner.anti_cloak)
        self.cloak = tech.cloak.percent
        detect_scanner = Scanner(normal=250.0)
        self.scanner_chart_data.append(detect_scanner.range_visible(self.apparent_mass))
        # Engine
        for engine in tech.engines:
            # Only display the last one
            self.engine_kt_exp = engine.kt_exponent
            self.engine_speed_div = engine.speed_divisor
            self.engine_speed_exp = engine.speed_exponent
            self.engine_siphon += engine.antimatter_siphon
            for i in range(0, 10):
                if len(self.engine_chart_data) < i + 1:
                    self.engine_chart_data.append(0)
                self.engine_chart_data[i] += engine.tachometer(i, chart_mass / len(tech.engines), 0)
        
Tech.set_defaults(Tech, __defaults)
