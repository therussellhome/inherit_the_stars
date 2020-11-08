import sys
from . import stars_math
from .defaults import Defaults
from . import game_engine
from .location import LocationReference


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': [0.0, 0.0, sys.maxsize],
    'penetrating': [0.0, 0.0, sys.maxsize],
    'normal': [0.0, 0.0, sys.maxsize]
}


""" Represent 'scanner' """
class Scanner(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Calculate the range an apparent mass is visible at """
    def range_visible(self, apparent_mass):
        visible_at = 0
        if apparent_mass > 0:
            visible_at = max(visible_at, self.penetrating)
            ly_per_kt = self.normal / 100.0
            visible_at = max(visible_at, apparent_mass * ly_per_kt)
        return visible_at

    def __add__(self, other):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, other.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, other.penetrating)
        s.normal = stars_math.volume_add(self.normal, other.normal) 
        return s

    def scan_ships(self, player, location):
        for ship in game_engine.get('Ship'):
            report = self.scan_ship(location, ship)
            if report:
                player.addReport(ship, **report)

    def scan_ship(self, location, ship):
        report = {}
        mass = ship.calc_mass()
        apparent = ship.calc_apparent_mass()
        distance = ship.location - location
        if ship.cloak.percent > 0 and distance <= self.anti_cloak:
            report['mass'] = mass
        if isinstance(ship.location, LocationReference):
            if distance <= self.penetrating:
                report['apparant_mass'] = apparent
        elif distance <= self.range_visible(apparent):
            report['apparant_mass'] = apparent
        if len(report) == 0:
            return None
        report['player'] = ship.player.name
        report['location'] = ship.location
        return report

    def scan_planets(self, player, location):
        for planet in game_engine.get('Planet'):
            report = self.scan_planet(location, planet)
            if report:
                player.addReport(planet, **report)

    def scan_planet(self, location, planet):
        distance = planet.location - location
        if distance <= self.penatrating:
            return {
                'location': planet.location,
                'gravity': planet.gravity, 
                'temperature': planet.temperature, 
                'radiation': planet.radiation,
                'player': planet.player.name,
                'population': planet.population,
            }
        return None
        

Scanner.set_defaults(Scanner, __defaults)
