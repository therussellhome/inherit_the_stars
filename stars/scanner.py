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
        visible_at = self.anti_cloak
        if apparent_mass > 0:
            visible_at = min(visible_at, self.penetrating)
            ly_per_kt = self.normal / 100.0
            visible_at = min(visible_at, apparent_mass * ly_per_kt)
        return visible_at

    def __add__(self, other):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, other.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, other.penetrating)
        s.normal = stars_math.volume_add(self.normal, other.normal) 
        return s

    def scan_ships(self, player, location):
        for ship in game_engine.get('Ship/'):
            distance = ship.location - location
            m = ship.calc_mass()
            if distance <= self.anticloak:
                player.addReport(ship, actual_mass = m)
            m = ship.calc_apparent_mass()
            if m > 0:
                if distance <= self.penatrating:
                    player.addReport(ship, apparent_mass = m)
                else:
                    if not isinstance(ship.location, LocationReference): 
                        ly_per_kt = (self.normal - self.penetrating)/100
                        if distance <= self.penatrating + ly_per_kt * m:
                            player.addReport(ship, apparent_mass = m)

    def scan_ship(self, location, ship):
        distance = ship.location - location
        if distance <= self.penatrating:
            return {}
        return None

    def scan_planets(self, player, location):
        for planet in game_engine.get('Planet/'):
            report = self.scan_planet(location, planet)
            if report:
                player.addReport(planet, **report)

    def scan_planet(self, location, planet):
        distance = planet.location - location
        if distance <= self.penatrating:
            return {'gravity': planet.gravity, 'temperature': planet.temperature, 'radiation': planet.radiation, 'population': planet.population}
        return None
        

Scanner.set_defaults(Scanner, __defaults)
