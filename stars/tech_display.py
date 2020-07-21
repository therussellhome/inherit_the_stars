import sys
import math
from .defaults import Defaults
from . import game_engine
from . import stars_math
# testing
from .bomb import Bomb
from .weapon import Weapon
from .engine import Engine

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
}

""" Display information about a tech item or ship design """
class TechDisplay(Defaults):
    def post(self, action):
        print(action)
        kt = self.chart_kt
        scanner_ly = self.chart_scanning
        player = None

        if '&' in action:
            action, token = action.split('&')
        tech = game_engine.get(action, False)
        if tech == None:
            self.reset_to_default()
        #kt = self.chart_kt
        # Test values
        self.chart_kt = kt
        self.chart_scanning = scanner_ly
        tech = game_engine.get('Tech/Test Component', True)
        tech.name = 'Test Component'
        tech.cost.energy = 100
        tech.cost.titanium = 100
        tech.cost.lithium = 100
        tech.cost.silicon = 100
        tech.level.energy = 3
        tech.level.weapons = 0
        tech.level.propulsion = 0
        tech.level.construction = 10
        tech.level.electronics = 5
        tech.level.biotechnology = 0
        tech.category = 'Ship Yard'
        tech.slot_type = 'orbital'
        tech.mass = 100
        tech.cargo_max = 200
        tech.fuel_max = 1000
        tech.description = 'a component\nstuff'
        tech.race_requirements = '-Aku\'Ultan'
        tech.shield = 100
        tech.armor = 200
        tech.ecm = 20
        tech.cloak = 50
        tech.weapons.append(Weapon(power=100, range=0.3))
        tech.engines.append(Engine(kt_exponent=1.5, speed_divisor=10.0, speed_exponent=5.0))
        tech.scanner = Scanner(anti_cloak=50, penetrating=100, normal=200)
        tech.bombs.append(Bomb())
        game_engine.save('test', 'tech_display', [tech])
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
            self.weapon_range = weapon.range
            self.weapon_accuracy = weapon.accuracy
            for i in range(0, 100):
                if len(self.weapon_chart_data) < i + 1:
                    self.weapon_chart_data.append(0)
                range_ly = i / 100 * stars_math.TERAMETER_2_LIGHTYEAR
                self.weapon_chart_data[i] += weapon.get_power(range_ly, sys.maxsize, 0) * weapon.get_accuracy(range_ly) / 100
        # Scanner
        self.scanner_normal = tech.scanner.normal
        self.scanner_penetrating = tech.scanner.penetrating
        self.scanner_anticloak = tech.scanner.anti_cloak
        self.cloak = tech.cloak
        self.scanner_chart_data.append(tech.scanner.normal)
        self.scanner_chart_data.append(tech.scanner.penetrating)
        self.scanner_chart_data.append(tech.scanner.anti_cloak)
        self.scanner_chart_data.append(tech.scanner.visable_range(kt * (1 - tech.cloak / 100)))
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
                self.engine_chart_data[i] += engine.tachometer(i, kt / len(tech.engines))
        
TechDisplay.set_defaults(TechDisplay, __defaults)
