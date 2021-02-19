import sys
from . import stars_math
from .defaults import Defaults
from . import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': (0.0, 0.0, sys.maxsize),
    'penetrating': (0.0, 0.0, sys.maxsize),
    'normal': (0.0, 0.0, sys.maxsize),
}


""" Represent 'scanner' """
class Scanner(Defaults):
    """ Calculate the range an apparent mass is visible at """
    def range_visible(self, apparent_mass):
        visible_at = 0
        if apparent_mass > 0:
            visible_at = max(visible_at, self.penetrating)
            ly_per_kt = self.normal / 100.0
            visible_at = max(visible_at, apparent_mass * ly_per_kt)
        return visible_at

    """ Addition operator """
    def __add__(self, other):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, other.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, other.penetrating)
        s.normal = stars_math.volume_add(self.normal, other.normal) 
        return s

    """ Add scan reports to the player from a location """
    def scan(self, player, location):
        for ship in game_engine.get('Ship'):
            report = self.scan_ship(location, ship)
            if report:
                player.add_intel(ship, **report)
        for planet in game_engine.get('Planet'):
            report = self.scan_planet(location, planet)
            if report:
                player.add_intel(planet, **report)

    """ Report about a ship """
    def scan_ship(self, location, ship):
        return {} #TODO fix for ships inside a system
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
        report['player'] = ship.player
        report['location'] = ship.location
        return report

    """ Report about a planet """
    def scan_planet(self, location, planet):
        distance = planet.location - location
        if distance <= self.penetrating:
            return {
                'location': planet.location,
                'color': planet.get_color(),
                'gravity': planet.gravity, 
                'temperature': planet.temperature, 
                'radiation': planet.radiation,
                'player': planet.player,
                'population': planet.on_surface.people,
                'lithium availability': planet.mineral_availability('lithium'),
                'silicon availability': planet.mineral_availability('silicon'),
                'titanium availability': planet.mineral_availability('titanium'),
            }
        return None
        

Scanner.set_defaults(Scanner, __defaults)
