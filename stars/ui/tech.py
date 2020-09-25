import sys
import math
from ..defaults import Defaults
from .. import game_engine
from .. import stars_math

__defaults = {
    'tech_name': ['UNKNOWN'],
    'category': ['UNKNOWN'], 
    'tech_level': [''],
    'cost': [''],
    'mass_cargo': [''],
    'description': [''],
    'race_requirements': [''],
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
    'chart_kt': [100, 1, sys.maxsize],
    'chart_scanning': [200, 1, sys.maxsize],

    'ecm': [0, 0, 100],
    'weapon_power': [0, 0, sys.maxsize],
    'weapon_range': [0.0, 0.0, 1.0],
    'weapon_accuracy': [0, 0, 100],
    'scanner_normal': [0, 0, sys.maxsize],
    'scanner_penetrating': [0, 0, sys.maxsize],
    'scanner_anticloak': [0, 0, sys.maxsize],
    'cloak': [0, 0, 100],
    'engine_kt_exp': [0.0, 0.0, sys.maxsize],
    'engine_speed_div': [0.0, 0.0001, sys.maxsize],
    'engine_speed_exp': [0.0, 0.0, sys.maxsize],

    # Shared with other forms and used to identify player
    'player_token': [''],
}

""" Display information about a tech item or ship design """
class Tech(Defaults):
    def post(self, action):
        tech = game_engine.get('Tech/' + action, False)
        if tech == None:
            self.reset_to_default()
            return
        kt = self.chart_kt
        # General
        self.tech_name = tech.name
        self.category = tech.category
        self.description = tech.description
        self.race_requirements = tech.race_requirements
        # Tech Level
        tmp_level = []
        if tech.level.energy > 0:
            tmp_level.append('Energy ' + str(tech.level.energy))
        if tech.level.weapons > 0:
            tmp_level.append('Weapons ' + str(tech.level.weapons))
        if tech.level.propulsion > 0:
            tmp_level.append('Propulsion ' + str(tech.level.propulsion))
        if tech.level.construction > 0:
            tmp_level.append('Construction ' + str(tech.level.construction))
        if tech.level.electronics > 0:
            tmp_level.append('Electronics ' + str(tech.level.electronics))
        if tech.level.biotechnology > 0:
            tmp_level.append('Biotechnology ' + str(tech.level.biotechnology))
        self.tech_level = ' | '.join(tmp_level)
        # Cost
        self.cost = str(tech.cost.energy) + 'YJ | ' \
            + str(tech.cost.titanium) + 'kT Ti | ' \
            + str(tech.cost.lithium) + 'kT Li | ' \
            + str(tech.cost.silicon) + 'kT Si'
        # Mass / Cargo
        self.mass_cargo = str(tech.mass) + 'kT'
        if tech.cargo_max > 0:
            self.mass_cargo += ' | ' + str(tech.cargo_max) + 'kT Cargo'
        if tech.fuel_max > 0:
            self.mass_cargo += ' | ' + str(tech.fuel_max) + '₥ Fuel'
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
        self.cloak = tech.cloak
        self.scanner_chart_data.append(tech.scanner.normal)
        self.scanner_chart_data.append(tech.scanner.penetrating)
        self.scanner_chart_data.append(tech.scanner.anti_cloak)
        self.scanner_chart_data.append(tech.scanner.range_visible(kt * (1 - tech.cloak.percent / 100)))
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
                self.engine_chart_data[i] += engine.tachometer(i, kt / len(tech.engines), 0)
        
Tech.set_defaults(Tech, __defaults)